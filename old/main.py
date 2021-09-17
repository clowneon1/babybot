import discord
from discord.errors import Forbidden
from discord.ext import commands, tasks
from discord import Intents
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from youtubesearchpython import SearchVideos
from django.core.validators import URLValidator
import os
import asyncio
from datetime import datetime
from keep_alive import keep_alive
from random import randint, choice
from itertools import cycle

validate = URLValidator()

client = commands.Bot(command_prefix='.', intents = Intents.all(), help_command=None)
client.remove_command('help')
statusName = 'The best bot.'

loop = False
queue = {}
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

statusesCycle = cycle(['Quinmon best streamer','Your mum','The best bot','Eddie Mac C','Not a fridge'])
statuses = ['Quinmon best streamer','Your mum','The best bot','Eddie Mac C','Not a fridge']

guessing = False

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Streaming(name=statusName, url='https://www.twitch.tv/xephirehd'))
    statusLooper.start()
    memberCount.start()
    onlineMemberCount.start()
    print('Bot ready')


@tasks.loop(seconds=30)
async def statusLooper():
    opt = randint(1,4)
    if opt == 1:
      await client.change_presence(activity=discord.Streaming(name=choice(statuses), url='https://www.twitch.tv/xephirehd'))
    elif opt == 2:
      await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=choice(statuses)))
    elif opt == 3:
      await client.change_presence(activity=discord.Game(name=choice(statuses)))
    elif opt == 4:
      await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=choice(statuses)))



@client.event
async def on_message(message):
    global guessing
    if guessing:
          if message.channel.id == 860593332510392370:
              if message.content.strip().lower() == name.lower() and message.author.id != master.id:
                  await message.channel.send(f"**{message.author.name}** has won the round.")
                  guessing = False
                  queue[message.guild.id] = []
                  voice.stop()
              if message.content.startswith('.') and message.author.id == master.id:
                    if message.content == ".end":
                        await message.channel.send(f"Nobody won the round.")
                        guessing = False
                        queue[message.guild.id] = []
                        voice.stop()
                    if message.content.startswith(".winner "):
                        winner = message.content.strip().replace(".winner ","")
                        await message.channel.send(f"**{winner}** has won the round.")
                        guessing = False
                        queue[message.guild.id] = []
                        voice.stop()
                
    await client.process_commands(message)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        pass


@client.command(name='help')
async def help(ctx):
    em = discord.Embed(title='Help', description='A discord.py multi-use bot, with many useful and fun features.', colour=discord.Color.purple())
    em.add_field(name='Join', value='Join the vc that the current user is in')
    em.add_field(name='Leave', value='Leave the vc that the current user is in')
    em.add_field(name='Play', value='Play a song, given either a url or a search term')
    em.add_field(name='Pause', value='Pauses current song')
    em.add_field(name='Loop', value = 'Loops through the current or next song until disabled.')
    em.add_field(name='Skip', value='Skips current song')
    em.add_field(name='Stop', value='Stops playing and clears queue')
    em.add_field(name='ClearQueue', value='Clears the queue')
    em.add_field(name="GayRate",value="Rates a user's 'gayness'")
    await ctx.send(embed = em)
    

# music

@client.command(name='join')
async def join(ctx):
    if ctx.message.author.voice is None:
        return await ctx.send('**You need to be in a voice channel to use this command**')
    for vc in client.voice_clients:
        if vc.guild.id == ctx.message.guild.id:
            return await ctx.send('**I am already in a voice channel**')
    vc = ctx.message.author.voice.channel
    await vc.connect()
    await ctx.send(f'**Joined** :musical_note: **{vc}** :musical_note:')


@client.command(name='leave')
async def leave(ctx):
    global queue, loop
    if ctx.message.author.voice is None:
        return await ctx.send('**You need to be in a voice channel to use this command**')

    loop = False
    server = ctx.message.guild.voice_client
    if server is not None:
        if str(ctx.message.author.voice.channel) != str(ctx.voice_client.channel):
            return await ctx.send('**You need to be in the same voice channel as me to use this command**')
        queue[ctx.guild.id] = []
        await server.disconnect()
        return await ctx.send(f'**Left** :musical_note: **{ctx.message.author.voice.channel}** :musical_note:')

    return await ctx.send('**I need to be in a voice channel for this command to be used**')



def play_next(ctx):
    try:
        voice = get(client.voice_clients, guild=ctx.guild)

        if not loop:
            del queue[ctx.guild.id][0]
            voice.play(FFmpegPCMAudio(getVideo(queue[ctx.guild.id][0])[0], **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
            voice.is_playing()
        else:
            voice.play(FFmpegPCMAudio(getVideo(previousURL)[0]), after=lambda e: play_next(ctx))
            voice.is_playing()

    except IndexError:
        pass
    except AttributeError:
        pass


def getVideo(url):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        videoTitle = info.get('title', None)
        url = info['formats'][0]['url']
    return [url, videoTitle]


@client.command(name='play',aliases=['p'])
async def play(ctx, *, url : str = None):
    global voice, previousURL
    if ctx.message.author.voice is None:
        return await ctx.send('**You need to be in a voice channel to use this command**')  

    voice = get(client.voice_clients, guild=ctx.guild)
    try:
        if url is None and voice.is_paused():
            voice.resume()
            return await ctx.send(':musical_note: **Song resumed** :musical_note:')
        elif url is None and not voice.is_paused():
            return await ctx.send('**Please enter either a search term or a url**')
    except AttributeError:
        return await ctx.send('**Please enter either a search term or a url**')

    # in case user doesn't enter valid url, searches YouTube instead

    try:
        validate(url)
    except:
        search = SearchVideos(url, offset = 1, mode = "dict", max_results = 1)
        url = search.result()['search_result'][0]['link']
    try:
        queue[ctx.guild.id].append(url)
    except:
        queue[ctx.guild.id] = [url]

    for vc in client.voice_clients:
        if vc.guild.id == ctx.guild.id:
            if str(ctx.message.author.voice.channel) != str(ctx.voice_client.channel):
                return await ctx.send('**You need to be in the same voice channel as me to use this command**')
            voice = get(client.voice_clients, guild=ctx.guild)

            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            
            if not voice.is_playing() and not voice.is_paused():
                try: 
                    previousURL = url
                    voice.play(FFmpegPCMAudio(getVideo(url)[0], **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
                    voice.is_playing()
                    return await ctx.send(f':musical_note: **{getVideo(url)[1]}** :musical_note: is now playing in :musical_note: **{ctx.message.author.voice.channel}** :musical_note:')
                except Exception as e:
                    print(e)
                    return await ctx.send('**There was an error playing your song**')

            else:
                return await ctx.send(f':musical_note: **{getVideo(url)[1]}** :musical_note: **was added to the queue**')

    
    vc = ctx.message.author.voice.channel
    await vc.connect()
    voice = get(client.voice_clients, guild=ctx.guild)
    await ctx.send(f'Joined :musical_note: **{vc}** :musical_note:')

    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if not voice.is_playing() and not voice.is_paused():
        try: 
            previousURL = url
            voice.play(FFmpegPCMAudio(getVideo(url)[0], **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
            voice.is_playing()
            return await ctx.send(f':musical_note: **{getVideo(url)[1]}** :musical_note: is now playing in :musical_note: **{ctx.message.author.voice.channel}** :musical_note:')
        except Exception as e:
            print(e)
            return await ctx.send('**There was an error playing your song**')

    else:
        return await ctx.send(f':musical_note: **{getVideo(url)[1]}** :musical_note: **was added to the queue**')


@client.command(name="loop")
async def loop(ctx):
    global loop
    if ctx.message.author.voice is None:
        return await ctx.send('**You need to be in a voice channel to use this command**')
    if str(ctx.message.author.voice.channel) != str(ctx.voice_client.channel):
        return await ctx.send('**You need to be in the same voice channel as me to use this command**')

    loop = not loop
    await ctx.send(f":musical_note: Looping set to **{str(loop)}** :musical_note:")


@client.command(name='skip',aliases=['s'])
async def skip(ctx):
    global loop
    if ctx.message.author.voice is None:
        return await ctx.send('**You need to be in a voice channel to use this command**')
    if str(ctx.message.author.voice.channel) != str(ctx.voice_client.channel):
        return await ctx.send('**You need to be in the same voice channel as me to use this command**')

    loop = False
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        if len(queue[ctx.guild.id]) > 0:
            voice.stop()   # not necessary to use the next_song function here, because it is told that when sound stops playing, it must automatically go to the next song.
            return await ctx.send(':musical_note: **Song skipped** :musical_note:')
        else:
            voice.stop()
            return await ctx.send(':musical_note: **Song skipped** :musical_note:')
    else:
        return await ctx.send('**There is no song playing to skip**')


@client.command(name='clearqueue',aliases=['cq'])
async def clearqueue(ctx):
    global queue
    if ctx.message.author.voice is None:
        return await ctx.send('**You need to be in a voice channel to use this command**')
    if str(ctx.message.author.voice.channel) != str(ctx.voice_client.channel):
        return await ctx.send('**You need to be in the same voice channel as me to use this command**')
    if len(queue[ctx.guild.id]) > 0:
        queue[ctx.guild.id] = []
        await ctx.send(':musical_note: **Queue cleared** :musical_note:')
    else:
        await ctx.send('**Queue is empty**')


@client.command(name='pause')
async def pause(ctx):
    global voice
    if ctx.message.author is None:
        return await ctx.send('**You need to be in a voice channel to use this command**')
    if str(ctx.message.author.voice.channel) != str(ctx.voice_client.channel):
        return await ctx.send('**You need to be in the same voice channel as me to use this command**')
    if voice.is_playing():
        voice.pause()
        return await ctx.send(':musical_note: **Song Paused** :musical_note:')
    if voice.is_paused():
        voice.resume()
        return await ctx.send(':musical_note: **Song resumed** :musical_note:')
    return await ctx.send('**There is no song in the queue**')


@client.command(name='stop')
async def stop(ctx):
    global voice, queue, loop
    if ctx.message.author is None:
        return await ctx.send('**You need to be in a voice channel to use this command**')
    if str(ctx.message.author.voice.channel) != str(ctx.voice_client.channel):
        return await ctx.send('**You need to be in the same voice channel as me to use this command**')

    loop = False
    queue[ctx.guild.id] = []
    voice.stop()
    await ctx.send('**:musical_note: Sound stopped playing :musical_note:**')


# join / leave / stats

@tasks.loop(seconds=20)
async def memberCount():
    for guild in client.guilds:
        for vc in guild.voice_channels:
            if vc.id == 815611737767149580:
                if vc.name != f'{guild.member_count} members':
                    await vc.edit(name = f'{guild.member_count} members')
                    break

@tasks.loop(seconds=10)
async def onlineMemberCount():
    for guild in client.guilds:
        for vc in guild.voice_channels:
            if vc.id == 817468882221531217:
                members = guild.members
                onlineMembers = [member for member in members if member.status in [discord.Status.online, discord.Status.idle, discord.Status.do_not_disturb]]
                if vc.name != f'{len(onlineMembers)} online members':
                    await vc.edit(name = f'{len(onlineMembers)} online members')

@client.event
async def on_member_join(self, member):
    # member
    welcomeChannel = discord.utils.get(member.guild.channels, name='welcome')
    await welcomeChannel.send(f'Welcome to **{member.guild.name}**, {member.mention}, enjoy your stay!')
    await member.add_roles(discord.utils.get(member.guild.roles, name="Noob"))
    #stats
    for vc in member.guild.voice_channels:
        if vc.id == 815611737767149580:
            if vc.name != f'{member.guild.member_count} members':
                await vc.edit(name = f'{member.guild.member_count} members')
                break

@client.event
async def on_member_remove(self, member):
    # member
    leaveChannel = discord.utils.get(member.guild.channels, name='leave')
    await leaveChannel.send(f'{member.mention} just left **{member.guild.name}**, what a shame.')
    #stats
    for vc in member.guild.voice_channels:
        if vc.id == 815611737767149580:
            if vc.name != f'{member.guild.member_count} members':
                await vc.edit(name = f'{member.guild.member_count} members')
                break  


# useful

# get reaction for the clear command
@client.event
async def on_reaction_add(reaction, user):
    try: confirmMsgID
    except NameError: return
    if reaction.message.id == confirmMsgID and reaction.emoji == '\N{NO ENTRY SIGN}' and user.id != client.user.id and user.id == confirmMsgUserID:
        await reaction.message.channel.purge(limit=None)
        await asyncio.sleep(0.5)
        delMsg = await reaction.message.channel.send('This channel was cleared')
        await asyncio.sleep(1)
        return await delMsg.delete()


# clear
@client.command(name='clear',aliases=['c'],help='Clears the current text channel')
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount : int = None):
  global confirmMsgID, confirmMsgUserID

  if ctx.author.guild_permissions.manage_messages:
    if amount is None:
      confirmMsg = await ctx.send('React to this message with :no_entry_sign: to confirm clearing the whole text channel. (This message automatically deletes after 5 seconds)', delete_after=5)
      await confirmMsg.add_reaction('\N{NO ENTRY SIGN}')
      confirmMsgID = confirmMsg.id
      confirmMsgUserID = ctx.author.id
      await asyncio.sleep(0.5)
      return
      
    if isinstance(amount, int) and amount > 0:
      await client.change_presence(status=discord.Status.online, activity=discord.Streaming(name=statusName, url='https://www.twitch.tv/xephire____'))
      await ctx.channel.purge(limit=amount+1)
      delMsg = await ctx.send(f'**{amount}** messages were deleted')
      await asyncio.sleep(2)
      await delMsg.delete()
      await asyncio.sleep(0.5)
    else:
      return await ctx.send('Please specify a valid number of messages to delete')
  else:
    permErrorMsg = await ctx.send('You do not have permission to use this command')
    await asyncio.sleep(2)
    await permErrorMsg.delete()

# ban
@client.command(name='ban',help='Ban a given user with a given reason')
@commands.has_permissions(ban_members = True)
async def ban(ctx, user : discord.Member = None, *, reason = None):

    if user is None:
        return await ctx.send('**Please specify a user to ban.**')
    if user.id == ctx.author.id:
        return await ctx.send('**You cannot ban yourself.**')
    if reason is None: reason = 'None'

    try:
        await user.ban(reason=reason)
    except:
        return await ctx.send(f'**{user.display_name}** could not be banned.')

    # for channel
    channelEmbed = discord.Embed(title=f'{user.display_name} has been banned from **{ctx.guild.name}**', colour=discord.Color.purple())
    channelEmbed.add_field(name='Reason', value=reason)
    channelEmbed.add_field(name='Date', value=str(datetime.now()))
    await ctx.send(embed=channelEmbed)

    # for user
    userEmbed = discord.Embed(title=f'You have been banned from **{ctx.guild.name}**', colour=discord.Color.purple())
    userEmbed.add_field(name='Reason', value=reason)
    userEmbed.add_field(name='Date', value=str(datetime.now()))

    try:
        await user.send(embed=userEmbed)
    except Forbidden:
        pass

@client.command(name='unban',help='Unbans a given user followed by their discriminator (hashtag number)')
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):

    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name.lower(), user.discriminator.lower()) == (member_name.lower(), member_discriminator.lower()):
            await ctx.guild.unban(user)
            return await ctx.send(f'Unbanned {user.mention}')
    await ctx.send("**The given user either doesn't exist or is not banned.**")

@client.command(name='kick',help='Kick a given user with a given reason')
@commands.has_permissions(kick_members = True)
async def kick(ctx, user : discord.Member = None, *, reason = None):
    if user is None:
        return await ctx.send('**Please specify a user to kick.**')
    if user.id == ctx.author.id:
        return await ctx.send('**You cannot kick yourself.**')
    if reason is None: reason = 'None'

    try:
        await user.kick(reason=reason)
    except Forbidden:
        return ctx.send(f'**{user.mention}** could not be kicked.')

    # for user
    userEmbed = discord.Embed(title=f'You have been kicked from **{ctx.guild.name}**', colour=discord.Color.purple())
    userEmbed.add_field(name='Reason', value=reason)
    userEmbed.add_field(name='Date', value=str(datetime.now()))

    # for channel
    channelEmbed = discord.Embed(title=f'{user.display_name} has been kicked from **{ctx.guild.name}**', colour=discord.Color.purple())
    channelEmbed.add_field(name='Reason', value=reason)
    channelEmbed.add_field(name='Date', value=str(datetime.now()))
    await ctx.send(embed=channelEmbed)

    try:
        await user.send(embed=userEmbed)
    except Forbidden:
        pass

@client.command(name="gayrate", help="Rates a user's 'gayness'")
async def gayrate(ctx, user : discord.Member = None):
    if user == None:
        user = ctx.message.author
    if user.id in [757991078296027238, 476384449362264074]:
        with open('gaygif.gif','rb') as f:
            em = discord.Embed(title='How Gay Are They', description=f'{user.mention} is mega gay!', colour=discord.Color.purple())
            picture = discord.File(f)
            return await ctx.send(embed=em,file=picture)

    gayLevel = randint(0,100)
    em = discord.Embed(title='How Gay Are They', description=f'{user.mention} is {gayLevel}% gay.', colour=discord.Color.purple())
    return await ctx.send(embed=em)


@client.command(name="guesssong", help="Enter a link to a song to guess what it's called", aliases=["gs"])
async def guesssong(ctx, *, name_and_search_term):
    global guessing, name, voice, master
    master = ctx.author
    name, search_term = [i.strip() for i in name_and_search_term.split(':')]
    guessing = True

    if ctx.message.author.voice is None:
        return await ctx.send('**You need to be in a voice channel to use this command**')  

    voice = get(client.voice_clients, guild=ctx.guild)
    try:
        if search_term is None and voice.is_paused():
            voice.resume()
            return await ctx.send(':musical_note: **Song resumed** :musical_note:')
        elif search_term is None and not voice.is_paused():
            return await ctx.send('**Please enter either a search term or a url**')
    except AttributeError:
        return await ctx.send('**Please enter either a search term or a url**')

    # in case user doesn't enter valid url, searches YouTube instead

    try:
        validate(search_term)
    except:
        search = SearchVideos(search_term, offset = 1, mode = "dict", max_results = 1)
        search_term = search.result()['search_result'][0]['link']
    try:
        queue[ctx.guild.id].append(search_term)
    except:
        queue[ctx.guild.id] = [search_term]

    for vc in client.voice_clients:
        if vc.guild.id == ctx.guild.id:
            if str(ctx.message.author.voice.channel) != str(ctx.voice_client.channel):
                return await ctx.send('**You need to be in the same voice channel as me to use this command**')
            voice = get(client.voice_clients, guild=ctx.guild)

            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            
            if not voice.is_playing() and not voice.is_paused():
                try: 
                    voice.play(FFmpegPCMAudio(getVideo(search_term)[0], **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
                    voice.is_playing()
                    return await ctx.send(f':musical_note: **{getVideo(search_term)[1]}** :musical_note: is now playing in :musical_note: **{ctx.message.author.voice.channel}** :musical_note:')
                except Exception as e:
                    print(e)
                    return await ctx.send('**There was an error playing your song**')

            else:
                return await ctx.send(f':musical_note: **{getVideo(search_term)[1]}** :musical_note: **was added to the queue**')

    
    vc = ctx.message.author.voice.channel
    await vc.connect()
    voice = get(client.voice_clients, guild=ctx.guild)
    await ctx.send(f'Joined :musical_note: **{vc}** :musical_note:')

    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if not voice.is_playing() and not voice.is_paused():
        try: 
            voice.play(FFmpegPCMAudio(getVideo(search_term)[0], **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
            voice.is_playing()
            return await ctx.send(f':musical_note: **{getVideo(search_term)[1]}** :musical_note: is now playing in :musical_note: **{ctx.message.author.voice.channel}** :musical_note:')
        except Exception as e:
            print(e)
            return await ctx.send('**There was an error playing your song**')

    else:
        return await ctx.send(f':musical_note: **{getVideo(search_term)[1]}** :musical_note: **was added to the queue**')


keep_alive()
token = os.environ.get('Token')
client.run(token)
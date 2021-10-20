from discord.ext import commands
import discord
from utils import get_source

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.loop = {}
        self.queue = {}

    def play_next(self, ctx, old_video):
        if not ctx.guild.id in self.loop.keys():
            self.loop[ctx.guild.id] = False

        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        try:
            if not self.loop[ctx.guild.id]:
                self.queue[ctx.guild.id].pop(0)
                if len(self.queue[ctx.guild.id]) > 0:
                    video = self.queue[ctx.guild.id][0]
                    voice_client.play(video[0], after=lambda e: self.play_next(ctx, video))
                    em = discord.Embed(title=f":musical_note: **{video[1]}** :musical_note: is now playing in :musical_note: **{ctx.message.author.voice.channel}** :musical_note:",
                        colour=discord.Color.purple())
                    em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)

                    self.bot.loop.create_task(ctx.send(embed=em))
            else:
                voice_client.play(old_video[0], after=lambda e: self.play_next(ctx, old_video))
                em = discord.Embed(title=f":musical_note: **{old_video[1]}** :musical_note: is now playing in :musical_note: **{ctx.message.author.voice.channel}** :musical_note:",
                    colour=discord.Color.purple())
                em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)

                self.bot.loop.create_task(ctx.send(embed=em))
        except Exception:
            pass

    @commands.command(name="play", aliases=["p","P"], help="Either plays or adds to queue the given YouTube link or search term.")
    async def play(self, ctx, *, arg : str = None):
        joined = False
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if ctx.message.author.voice is None:
            em = discord.Embed(title="**You need to be in a voice channel to use this command**", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            
            return await ctx.send(embed=em)

        if voice_client and voice_client.channel.id is not ctx.author.voice.channel.id:
            em = discord.Embed(title="**You need to be in the same voice channel as me to use this command**", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)

            return await ctx.send(embed=em)

        if arg is None and voice_client.is_paused():
            voice_client.resume()
            em = discord.Embed(title=":musical_note: **Song resumed** :musical_note:", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)

            return await ctx.send(embed=em)

        if arg is None and voice_client.is_playing():
            voice_client.pause()
            em = discord.Embed(title=":musical_note: **Song paused** :musical_note:", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)

            return await ctx.send(embed=em)

        if not voice_client:
            joined = True
            self.loop[ctx.guild.id] = False
            vc = ctx.author.voice.channel
            await vc.connect()
            voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        
        video = get_source.get_source(arg)
        if ctx.guild.id not in self.queue.keys():
            self.queue[ctx.guild.id] = [video]
        else:
            self.queue[ctx.guild.id].append(video)

        if not voice_client.is_playing() and not voice_client.is_paused():
            try:
                voice_client.play(video[0], after=lambda e: self.play_next(ctx, video))

                if joined:
                    em = discord.Embed(title=f"Joined :musical_note: **{vc}** :musical_note:",
                        description=f":musical_note: **{video[1]}** :musical_note: is now playing in :musical_note: **{ctx.message.author.voice.channel}** :musical_note:",
                        colour=discord.Color.purple())
                    em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)

                    return await ctx.send(embed=em)

                else:
                    em = discord.Embed(title=f":musical_note: **{video[1]}** :musical_note: is now playing in :musical_note: **{ctx.message.author.voice.channel}** :musical_note:", 
                        colour=discord.Color.purple())
                    em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)

                    return await ctx.send(embed=em)

            except Exception as e:
                print(e)
                em = discord.Embed(title="**There was an error playing your song**", colour=discord.Color.purple())
                em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)

                return await ctx.send(embed=em)
        else:
            em = discord.Embed(title=f":musical_note: **{video[1]}** :musical_note: **was added to the queue**", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=em)

    @commands.command(name="join", aliases=["j","J"], help="Joins the user's VC")
    async def join(self, ctx):
        user = ctx.author
        vc = user.voice.channel
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice_client is None:
            self.loop[ctx.guild.id] = False
            await vc.connect()

            em = discord.Embed(title=f":musical_note: Joined **{vc}**", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)

            return await ctx.send(embed=em)
        else:
            em = discord.Embed(title="I'm already in a VC!", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=em)

    @commands.command(name="leave", aliases=["l","L"], help="Leaves the user's VC")
    async def leave(self, ctx):
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if ctx.message.author.voice is None:
            em = discord.Embed(title="**You need to be in a voice channel to use this command**", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            
            return await ctx.send(embed=em)

        if ctx.message.author.voice.channel.id != ctx.voice_client.channel.id:
            em = discord.Embed(title="**You need to be in the same voice channel as me to use this command**", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            
            return await ctx.send(embed=em)

        if voice_client is None:
            em = discord.Embed(title="**I'm not in a VC!**", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)

            return await ctx.send(embed=em)

        if voice_client.channel.id is ctx.message.author.voice.channel.id:
            await voice_client.disconnect()
            self.queue[ctx.guild.id] = []
            em = discord.Embed(title=f":musical_note: **Left** **{ctx.message.author.voice.channel}**", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            
            return await ctx.send(embed=em)

    @commands.command(name="loop", aliases=["lp"], help="Toggles looping songs on and off.")
    async def loop(self, ctx, arg : str=None):
        if ctx.message.author.voice is None:
            em = discord.Embed(title="**You need to be in a voice channel to use this command**", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            
            return await ctx.send(embed=em)

        if ctx.message.author.voice.channel.id != ctx.voice_client.channel.id:
            em = discord.Embed(title="**You need to be in the same voice channel as me to use this command**", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            
            return await ctx.send(embed=em)
            
        if arg is None and ctx.guild.id in self.loop.keys():
            self.loop[ctx.guild.id] = not self.loop[ctx.guild.id]

        elif arg is None and ctx.guild.id not in self.loop.keys():
            self.loop[ctx.guild.id] = True

        elif arg in ["true","TRUE","True", "1"]:
            self.loop[ctx.guild.id] = True

        elif arg in ["false","FALSE","False","0"]:
            self.loop[ctx.guild.id] = False

        em = discord.Embed(title=f"**Looping set to {self.loop[ctx.guild.id]}**", colour=discord.Color.purple())
        em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            
        return await ctx.send(embed=em)


    @commands.command(name="skip", aliases=["s","S"], help="Skips the currently playing song")
    async def skip(self, ctx):
        if ctx.message.author.voice is None:
            em = discord.Embed(title="**You need to be in a voice channel to use this command**", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            
            return await ctx.send(embed=em)
        if ctx.message.author.voice.channel.id != ctx.voice_client.channel.id:
            em = discord.Embed(title="**You need to be in the same voice channel as me to use this command**", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            
            return await ctx.send(embed=em)

        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client.is_playing():
            self.loop[ctx.guild.id] = False
            voice_client.stop()
            em = discord.Embed(title=":musical_note: **Song skipped, looping is OFF** :musical_note:", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            
            return await ctx.send(embed=em)
        else:
            em = discord.Embed(title="**There is no song playing to skip**", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            
            return await ctx.send(embed=em)

    @commands.command(name="stop", aliases=["st"], help="Stops song and clears queue")
    async def stop(self, ctx):
        if ctx.message.author.voice is None:
            em = discord.Embed(title="**You need to be in a voice channel to use this command**", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            
            return await ctx.send(embed=em)
        if ctx.message.author.voice.channel.id != ctx.voice_client.channel.id:
            em = discord.Embed(title="**You need to be in the same voice channel as me to use this command**", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            
            return await ctx.send(embed=em)
            
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if not voice_client.is_playing():
            self.queue[ctx.guild.id] = []

            em = discord.Embed(title=":musical_note: **No sound is playing!** :musical_note:", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=em)

        voice_client.stop()
        self.queue[ctx.guild.id] = []

        em = discord.Embed(title=":musical_note: **Music stopped and queue cleared** :musical_note:", colour=discord.Color.purple())
        em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command(name="clearqueue", aliases=["cq"], help="Clears the song queue.")
    async def clearqueue(self, ctx):
        if ctx.message.author.voice is None:
            em = discord.Embed(title="**You need to be in a voice channel to use this command**", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)

            return await ctx.send(embed=em)
        if ctx.message.author.voice.channel.id != ctx.voice_client.channel.id:
            em = discord.Embed(title="**You need to be in the same voice channel as me to use this command**", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            
            return await ctx.send(embed=em)
        
        if len(self.queue[ctx.guild.id]) > 0:
            self.queue[ctx.guild.id] = []
            em = discord.Embed(title=":musical_note: **Queue cleared** :musical_note:", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)

            return await ctx.send(embed=em)
        else:
            em = discord.Embed(title="**Queue is empty**", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            
            return await ctx.send(embed=em)

    @commands.command(name="queue", aliases=["q","Q"], help="Shows the current.")
    async def queue(self, ctx):
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client is None:
            em = discord.Embed(title="**I'm not in a VC!**", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)

            return await ctx.send(embed=em)
        
        if ctx.guild.id not in self.queue.keys() or len(self.queue[ctx.guild.id]) < 2:
            em = discord.Embed(title="Queue is empty", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)

            return await ctx.send(embed=em)

        if len(self.queue[ctx.guild.id]) > 1:
            em = discord.Embed(title="Queue", colour=discord.Color.purple())
            [em.add_field(name=item[1], value="\u200b", inline=False) for item in self.queue[ctx.guild.id][1:]]
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)

            return await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Music(bot))
from discord.ext import commands
import discord
from utils import get_source

class GuessSong(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="playanswer", aliases=["pa","PA"], help="Plays given YouTube link or search term and starts a guess the song game.")
    async def play_answer(self, ctx, arg : str = None):
        ctx.message.delete() # deletes the user's message so peeking is not possible

        data = arg.split("::")
        self.game_playing = False
        self.current_song = data[1]
        self.game_master = ctx.author.id

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
            vc = ctx.author.voice.channel
            await vc.connect()
            voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        
        video = get_source.get_source(data[0])

        if not voice_client.is_playing() and not voice_client.is_paused() and not self.game_playing:

            try:
                voice_client.play(video[0], after=None)
                self.game_playing = True

                if joined:
                    em = discord.Embed(title=f"Joined :musical_note: **{vc}** :musical_note:",
                        description=f":musical_note: Song started! :musical_note: **{ctx.message.author.voice.channel}** :musical_note:",
                        colour=discord.Color.purple())
                    em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                    
                    return await ctx.send(embed=em)

                else:
                    em = discord.Embed(title=f":musical_note: Song started! :musical_note: **{ctx.message.author.voice.channel}** :musical_note:", 
                        colour=discord.Color.purple())
                    em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)

                    return await ctx.send(embed=em)

            except Exception as e:
                print(e)
                em = discord.Embed(title="**There was an error playing your song**", colour=discord.Color.purple())
                em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)

                return await ctx.send(embed=em)

    @commands.command(name="guesssong", aliases=["gs","GS"], help="Lets users guess the name of the currently playing song.")
    async def guess_song(self, ctx, arg : str = None):
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if ctx.message.author.voice is None:
            em = discord.Embed(title="**You need to be in a voice channel to use this command**", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            
            return await ctx.send(embed=em)

        if voice_client and voice_client.channel.id is not ctx.author.voice.channel.id:
            em = discord.Embed(title="**You need to be in the same voice channel as me to use this command**", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)

        if ctx.author.id == self.game_master:
            em = discord.Embed(title="**You can't guess your own song!**", colour=discord.Color.purple())
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=em)
        
        if arg.strip().lower() == self.current_song.strip().lower():
            voice_client.stop()
            self.game_playing = False

            em = discord.Embed(title=f"**{ctx.author.name} guessed the song! ({self.current_song})**", colour=discord.Color.purple())
            em.set_footer(text=f"Answered by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=em)
        else:
            em = discord.Embed(title=f"**{arg.strip()} is not the correct answer!**", colour=discord.Color.purple())
            em.set_footer(text=f"Answered incorrectly by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=em) 

def setup(bot):
    bot.add_cog(GuessSong(bot))
from discord.ext import commands
import discord
from utils import get_source

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.loop = False
        self.queue = {}

    def play_next(self, ctx, old_video):
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        try:
            if not self.loop:
                self.queue[ctx.guild.id].pop(0)
                if len(self.queue[ctx.guild.id]) > 0:
                    video = self.queue[ctx.guild.id][0]
                    voice_client.play(video[0], after=lambda e: self.play_next(ctx, video))
                    self.bot.loop.create_task(ctx.send(f":musical_note: **{video[1]}** :musical_note: is now playing in :musical_note: **{ctx.message.author.voice.channel}** :musical_note:"))
            else:
                voice_client.play(old_video[0], after=lambda e: self.play_next(ctx, old_video))
                self.bot.loop.create_task(ctx.send(f":musical_note: **{old_video[1]}** :musical_note: is now playing in **{ctx.message.author.voice.channel}**"))
        except Exception:
            pass

    @commands.command(name="play", aliases=["p","P"], help="Either plays or adds to queue the given YouTube link or search term.")
    async def play(self, ctx, *, arg : str = None):
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if ctx.message.author.voice is None:
            return await ctx.send("**You need to be in a voice channel to use this command**")

        if voice_client and voice_client.channel.id is not ctx.author.voice.channel.id:
            return await ctx.send("**You need to be in the same voice channel as me to use this command**")

        if arg is None and voice_client.is_paused():
            voice_client.resume()
            return await ctx.send(":musical_note: **Song resumed** :musical_note:")

        if arg is None and voice_client.is_playing():
            voice_client.pause()
            return await ctx.send(":musical_note: **Song paused** :musical_note:")

        if not voice_client:
            vc = ctx.author.voice.channel
            await vc.connect()
            voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            await ctx.send(f"Joined :musical_note: **{vc}** :musical_note:")
        
        video = get_source.get_source(arg)
        try: self.queue[ctx.guild.id].append(video)
        except Exception: self.queue[ctx.guild.id] = [video]

        if not voice_client.is_playing() and not voice_client.is_paused():
            try:
                voice_client.play(video[0], after=lambda e: self.play_next(ctx, video))
                return await ctx.send(f":musical_note: **{video[1]}** :musical_note: is now playing in :musical_note: **{ctx.message.author.voice.channel}** :musical_note:")
            except Exception:
                return await ctx.send("**There was an error playing your song**")
        else:
            return await ctx.send(f':musical_note: **{video[1]}** :musical_note: **was added to the queue**')

    @commands.command(name="join", aliases=["j","J"], help="Joins the user's VC")
    async def join(self, ctx):
        user = ctx.author
        vc = user.voice.channel
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice_client is None:
            await vc.connect()
            return await ctx.send(f"Joined :musical_note: **{vc}** :musical_note:")
        else:
            return await ctx.send("**I'm already in a VC!**")

    @commands.command(name="leave", aliases=["l","L"], help="Leaves the user's VC")
    async def leave(self, ctx):
        user = ctx.message.author
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        
        if user.voice is None:
            return await ctx.send("**You need to be in a voice channel to use this command**")
        if voice_client is None:
            return await ctx.send("**I'm not in a VC!**")
        if voice_client.channel.id is user.voice.channel.id:
            await voice_client.disconnect()
            self.queue[ctx.guild.id] = []
            return await ctx.send(f':musical_note: **Left** **{ctx.message.author.voice.channel}**')
        if voice_client.channel.id is not user.voice.channel.id:
            return await ctx.send("**You need to be in the same voice channel as me to use this command**")

    @commands.command(name="loop", aliases=["lp"], help="Toggles looping songs on and off.")
    async def loop(self, ctx, arg : str=None):
        if arg is None:
            self.loop = not self.loop
            return await ctx.send(f"**Looping set to {self.loop}**")
        if arg in ["true","TRUE","True", "1"]:
            self.loop = True
            return await ctx.send("**Looping set to True**")
        if arg in ["false","FALSE","False","0"]:
            self.loop = False
            return await ctx.send("**Looping set to False**")


    @commands.command(name="skip", aliases=["s","S"], help="Skips the currently playing song")
    async def skip(self, ctx):
        if ctx.message.author.voice is None:
            return await ctx.send('**You need to be in a voice channel to use this command**')
        if ctx.message.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send('**You need to be in the same voice channel as me to use this command**')
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client.is_playing():
            voice_client.stop()
            return await ctx.send(f':musical_note: **Song skipped, looping is {"ON" if self.loop else "OFF"}** :musical_note:')
        else:
            return await ctx.send('**There is no song playing to skip**')

    @commands.command(name="stop", aliases=["st"], help="Stops song and clears queue")
    async def stop(self, ctx):
        if ctx.message.author.voice is None:
            return await ctx.send('**You need to be in a voice channel to use this command**')
        if ctx.message.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send('**You need to be in the same voice channel as me to use this command**')

        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        voice_client.stop()
        self.queue[ctx.guild.id] = []
        await ctx.send(':musical_note: **Music stopped and queue cleared** :musical_note:')

    @commands.command(name="clearqueue", aliases=["cq"], help="Clears the song queue.")
    async def clearqueue(self, ctx):
        if ctx.message.author.voice is None:
            return await ctx.send('**You need to be in a voice channel to use this command**')
        if ctx.message.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send('**You need to be in the same voice channel as me to use this command**')
        
        if len(self.queue[ctx.guild.id]) > 0:
            self.queue[ctx.guild.id] = []
            await ctx.send(':musical_note: **Queue cleared** :musical_note:')
        else:
            await ctx.send('**Queue is empty**')

    @commands.command(name="queue", aliases=["q","Q"], help="Shows the current.")
    async def queue(self, ctx):
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client is None:
            return await ctx.send("**I'm not in a VC!**")

        if len(self.queue[ctx.guild.id]) > 0:
            em = discord.Embed(title='Queue', colour=discord.Color.purple())
            [em.add_field(name="\u200b", value=item[1], inline=False) for item in self.queue[ctx.guild.id]]
            await ctx.send(embed=em)
        else:
            await ctx.send('**Queue is empty**')

def setup(bot):
    bot.add_cog(Music(bot))
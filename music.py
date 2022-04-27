import discord
from discord.ext import commands
import youtube_dl

class music(commands.Cog):
    def __init__(self,client):
        self.client = client
        
    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.senc("You are not in a voice channel")
        voice_chanel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_chanel.connect()
        else:
            await ctx.voice_client.move_to(voice_chanel)
    
    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()
        
    @commands.command()
    async def play(self,ctx,url):

      if ctx.author.voice is None:
          await ctx.senc("You are not in a voice channel")
      voice_chanel = ctx.author.voice.channel
      if ctx.voice_client is None:
          await voice_chanel.connect()
      else:
          await ctx.voice_client.move_to(voice_chanel)
    
      if ctx.voice_client is not None:
        ctx.voice_client.stop()
      FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options' : '-vn'}
      YDL_OPTIONS = {'format' : 'bestaudio'}
      vc = ctx.voice_client
      
      with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
          info = ydl.extract_info(url,download=False)
          url2 = info['formats'][0]['url']
          source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
          vc.play(source)
        
    @commands.command()
    async def pause(self, ctx):
        voice = ctx.voice_client
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send('Currently no audio is playing.')
        
    @commands.command()
    async def resume(self, ctx):
        voice = ctx.voice_client
            
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send('The audio is not paused.')
            
    @commands.command()
    async def stop(self,ctx):
        voice = ctx.voice_client
        voice.stop()
        await ctx.send('Music stopped')
        
    @commands.command()
    async def leave(self,ctx):
        voice = ctx.voice_client
        if voice.is_connected():
            await voice.disconnect()
            await ctx.send('Disconnected.')  
        else:
            await ctx.send('The bot is not connected to a voice channel.')  
    
    
def setup(client):
    client.add_cog(music(client))
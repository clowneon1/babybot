from youtube_dl import YoutubeDL
import requests
import discord

def get_source(arg):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn"}
    try:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            try:
                requests.get(arg) 
            except Exception:
                video = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
            else:
                video = ydl.extract_info(arg, download=False)

            source = video['formats'][0]['url']
            title = video.get('title', None)
            
            video_obj = discord.FFmpegPCMAudio(source, **FFMPEG_OPTIONS)
            return [video_obj, title]
    except IndexError:
        pass
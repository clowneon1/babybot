from youtube_dl import YoutubeDL
import requests

def get_source(arg):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
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
            return [source, title]
    except IndexError:
        pass
"""
this will focus on downloading the video from dlive and returning its filepath


"""
import youtube_dl

class downloader:
    hookdata=None
    def __init__(self,url):
        ydl_opts = {
            'progress_hooks': [self.my_hook],
            'restrictfilenames': 1,
            'nocheckcertificate': 1,  # for bitchute compatibility
            'ignoreerrors' : True,
        }
        self.url=url
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])

    def my_hook(self,d):
        #global hookdata
        self.hookdata=d

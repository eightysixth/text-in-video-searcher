import re;
import youtube_dl

class Downloader:
    def __init__(self, video_url,options):
        # Youtube dl can start downloading from url
        print("requesting to download", video_url)
        self._opts = options;
        self._url = video_url
        self._downloader = youtube_dl.YoutubeDL(self._opts);
    
    def start_download(self):
        with youtube_dl.YoutubeDL(self._opts) as ydl:
            ydl.download([self._url])



if __name__ == "__main__": # only run when this .py file is executed
    # Look for video url as an argument.
    import sys;
    if len(sys.argv) < 1:
        print("Please provide a video url")
    else:
        # Sample video id:
        # https://www.youtube.com/watch?v=V9pgI0b7UD8
        video_url = sys.argv[1];
        if video_url is not None:
            options = {
                'format':'mp4',
                'fps':30,
                'outtmpl':'%(id)s.%(ext)s'
                # 'forcefilename':'temp.mp4'
            }

            downloader = Downloader(video_url, options)
            video = downloader.start_download();





from downloader import Downloader
import os;
import sys;
import opencv-python;

def changeVideoFPS(file_name, targetfps):
    command_string = "ffmpeg -i " + file_name + " -filter:v fps=fps=" + str(targetfps) + " out."+file_name;
    os.system(command_string)


def download_hook(d):
    if d['status'] == 'finished':
        file_name = d['filename']
        print(file_name)
        # File was downloaded.. now split into frames and stream to ocr
        changeVideoFPS(file_name, 1);

def main():
    finished = False;
    
    while not finished:
        video_url = input("Please enter video url ('stop' to exit):  ")
        if video_url == 'stop':
            finished = True;
            sys.exit();
        options = {
            'format':'mp4', #worst
            'fps':30,
            'outtmpl':'%(id)s.%(ext)s'
            # 'forcefilename':'temp.mp4'
        }
        options['progress_hooks'] = [download_hook]
        downloader = Downloader(video_url, options)
        downloader.start_download();

main();
# ffmpeg -i <input> -filter:v fps=fps=30 <output>

        

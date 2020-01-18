from downloader import Downloader
import os;
import sys;
import cv2;
import pytesseract;
import json;
import re;

word_list = []


def runOCR(video_file_name):
    cap = cv2.VideoCapture(video_file_name);
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # out = cv2.VideoWriter('output.avi',fourcc, 1, (int(cap.get(3)), int(cap.get(4))), 1)
    text_output = {}
    frame_id = 0;
    
    while (cap.isOpened()):
        ret, frame = cap.read();
        if ret == True:
            frame_id += 1;
            print(frame_id)
            # print("READING FRAME: ", ret, frame)
            # frame.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            medianBlur = cv2.medianBlur(gray, 3)
            data = pytesseract.image_to_string(gray)

            for word in data.split(' '):
                if not word in text_output:
                    text_output[word] = []
                text_output[word].append(frame_id)
            # cv2.imshow('frame',frame)
            print("frame #", frame_id, data)
            # cv2.imshow('frame', medianBlur)
            # out.write(gray)
        else:
            break;
    
    with open(video_file_name + '.json', 'w', encoding='utf8') as f:
        json.dump(text_output, f, indent=4)
    cv2.destroyAllWindows();
    cap.release();
    # out.release();

    # Funny text memes: https://www.youtube.com/watch?v=K1Jkrngi0R0


        # frame.mdeian

def changeVideoFPS(file_name, targetfps):
    output_file_name = "out."+file_name
    command_string = "ffmpeg -i " + file_name + " -filter:v fps=fps=" + str(targetfps) + " "+output_file_name;
    output = os.system(command_string)
    return output_file_name

def cleanup(output_file_name):
    os.system("rm -r " + output_file_name);

def download_hook(d):
    if d['status'] == 'finished':
        file_name = d['filename']
        print(file_name)
        # File was downloaded.. now split into frames and stream to ocr
        output_file_name = changeVideoFPS(file_name, 1);
        runOCR(output_file_name)
        cleanup(output_file_name)

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

# main();
# ffmpeg -i <input> -filter:v fps=fps=30 <output>

def test():
    runOCR("out.K1Jkrngi0R0.mp4")

main()
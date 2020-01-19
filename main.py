from downloader import Downloader
import os;
import sys;
import cv2;
import pytesseract;
import json;
import re;

word_list = []

def writeToJsonFile(fileName, data):
    with open(fileName, 'w', encoding='utf8') as f:
        json.dump(data, f, indent=4)




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
            data.split("\n")

            for word in re.split("\s+|\n", data):
                if not word in text_output:
                    text_output[word] = []
                print(word)
                text_output[word].append(frame_id)

            # for line in data.split("\n"):
            #     for word in line.split(" "):
            #         if not word in text_output:
            #             text_output[word] = []
            #         print(word)
            #         text_output[word].append(frame_id)
            # cv2.imshow('frame',frame)
            print("frame #", frame_id, data)
            # cv2.imshow('frame', medianBlur)
            # out.write(gray)
        else:
            break;

    writeToJsonFile(video_file_name + '.original.json', text_output)
    
    for word in text_output:
        # Iterate through the frames and determine if they order in sequence, if they do, remove sequence
        good_frames = []
        cur_frame = text_output[word][0]; # First element, eg. frame 104
        for group in list(groupSequence(text_output[word])):
            good_frames.append(group[0])
        
        text_output[word] = good_frames

    writeToJsonFile(video_file_name + '.trimmed.json', text_output)

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

def groupSequence(lst): 
    res = [[lst[0]]] 
  
    for i in range(1, len(lst)): 
        if lst[i-1]+1 == lst[i]: 
            res[-1].append(lst[i]) 
  
        else: 
            res.append([lst[i]]) 
    return res 

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

# Test video: https://www.youtube.com/watch?v=5paISomtdn4
# Hitler reddit: https://www.youtube.com/watch?v=eNW2y6DTwtw

def test():
    runOCR("out.K1Jkrngi0R0.mp4")

main()
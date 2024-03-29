from os.path import isfile, join
import cv2
import numpy as np
import os

import cv2
import os

# pathIn = '/home/sobey/Dataset/Material/Video/Material1/画质受损一般_output/Out/'
pathIn = r'\\192.168.31.10\AlgorithmData\Data\ZNJT\ZhongChe_ChengKeXingWei\train_images\Smoking_label\Smoking'
# pathIn='/home/sobey/Dataset/Material/Video/字幕区域修复/红色底板/'
# pathOut='/home/sobey/Dataset/Material/Video/字幕区域修复/红色底板.mp4'
pathOut= r'\\192.168.31.10\AlgorithmData\Data\ZNJT\ZhongChe_ChengKeXingWei\train_images/all_fire.mp4'
# pathOut = '/home/sobey/Dataset/Material/Video/Material1/video_output/a.avi'

def encoder():
    fps = 25
    frame_array = []
    img_postfix=['png','jpg']
    files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f)) and f.split('.')[-1] in img_postfix]
    # for sorting the file names properly
    # print(files[0][5:][:-4])

    # files.sort(key=lambda x: int(x[:-4]))       # Sort images to right order for video
    img=cv2.imread(os.path.join(pathIn , files[0]))
    height, width, layers = img.shape
    target_size = (width, height)

    for i in range(len(files)):
        filename = os.path.join(pathIn , files[i])
        # reading each files
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width, height)
        if size!=target_size:
            img=cv2.resize(img,target_size)
        # inserting the frames into an image array
        frame_array.append(img)
    # out = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    out = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(*"mp4v"), fps, target_size)
    for i in range(len(frame_array)):
        # writing to a image array
        for j in range(55):
            out.write(frame_array[i])
    out.release()


# in_video = '/home/sobey/Dataset/Material/Video/Material1/1.1画质受损一般.ts'

in_video = '/home/sobey/Dataset/Material/Video/Material1/中国新闻_0400_20180806035753_1_138_6500__011__high.mp4'

def create_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def read_video():
    vidcap = cv2.VideoCapture(in_video)
    if cap.isOpened():
        width  = vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float `width`
        height = vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`
        fps = vidcap.get(cv2.CAP_PROP_FPS) # float `fps`
    size=(int(width),int(height))
    # get size
    success, image = vidcap.read()
    count = 0
    # dir_name='./images/'
    dir_name=os.path.dirname(in_video)
    while success:
        folder = os.path.join(dir_name, os.path.basename(in_video).split('.')[0])
        create_dir(folder)
        file_path = os.path.join(folder, "frame%d.png" % count)
        cv2.imwrite(file_path, image)  # save frame as JPEG file
        success, image = vidcap.read()
        print('Read a new frame: ', success)
        count += 1

if __name__=='__main__':
    encoder()
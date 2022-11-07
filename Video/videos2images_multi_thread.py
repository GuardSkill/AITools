'''
Author: Siyuan Li
Date: 2022-08-01 16:13:53
LastEditors: Siyuan Li
LastEditTime: 2022-09-26 16:30:22
FilePath: \AITools\Video\videos2images_multi_thread.py
Description: 
Email: 497291093@qq.com
Copyright (c) 2022 by Siyuan Li - ZHONGCHAO XINDA, All Rights Reserved. 
'''
'''
Author: Siyuan Li
Date: 2022-08-01 16:13:53
LastEditors: Siyuan Li
LastEditTime: 2022-08-08 14:31:05
FilePath: \AITools\Video\step2-videos2images_multi_thread.py
Description: 
Email: 497291093@qq.com
Copyright (c) 2022 by Siyuan Li - ZHONGCHAO XINDA, All Rights Reserved. 
'''
#coding: utf-8

import random
import threading
from utils import *

video_path= r'\\192.168.31.10\AlgorithmData\Data\ZNJT\ZhongChe_ChengKeXingWei\20221025_Lean'
video_path= r'\\192.168.31.10\AlgorithmData\Data\ZNJT\ShangHai_jcp\LabelData\NeedDecodeVideo'
image_save_path = video_path+'_images'
sample_interval=int(25)         # x秒*25帧
postfix=['mp4', 'MP4','mov','mkv']
random_sample=False
# image_save_path='F:/Data/ActionDet/random_sample_images'
    
def process_videos(video_files, image_save_path, interval, start_frame):
    # for idx in tqdm.tqdm(range(len(video_files))):
    for video_file in video_files:
        try:
            # video_file = video_files[idx]
            print("{} process: {}".format(threading.currentThread, video_file))
            video_to_images_uniform_cv2(video_file, image_save_path, interval=interval, start_frame=start_frame)
            # video_to_images_middle_sample_ffmpeg(video_file, image_save_path)
            # classify_extract_video_ffmpeg(video_file, image_save_path,prefix_name=None,second_interval=50)
        except:
            continue


class myThread(threading.Thread):

    def __init__(self, thread_name, description, video_files, image_save_path, interval=50, start_frame=1):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.description = description
        self.video_files = video_files
        self.image_save_path = image_save_path
        self.interval = interval
        self.start_frame = 1

    def run(self):
        print("start thread: ", self.thread_name)
        process_videos(self.video_files, image_save_path=self.image_save_path, interval=self.interval, start_frame=self.start_frame)
        print("end thread: ", self.thread_name)



if __name__ == "__main__":
    files = get_file_list(video_path)
    video_files = files_filter(files, postfix)

    video_files.sort()

    if random_sample:
        random.shuffle(video_files,random=None)
        video_files=video_files[:300]
        len_each_video=10*25*60
        sample_interval=len_each_video/1.8

    print("video_files: ", video_files,"video num：",video_files)
    
    thread_count = 16                                       #16
    if len(video_files) < thread_count:
        thread_count = len(video_files)
    video_size = int(len(video_files)/thread_count + 0.5)
    print(video_size)
    videos_list = []
    jobs = []
    for i in range(thread_count):
        threadID = "Th"+str(i)
        start = i*video_size
        end = (i+1)*video_size
        if end > len(video_files):
            end = len(video_files)
        videos = video_files[start: end]
        th = myThread(threadID, "process videos", videos, image_save_path, interval=sample_interval)       # 正面800
        jobs.append(th)

    for job in jobs:
        job.start()

    for job in jobs:
        job.join()

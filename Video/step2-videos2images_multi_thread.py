'''
Author: Siyuan Li
Date: 2022-08-01 16:13:53
LastEditors: Siyuan Li
LastEditTime: 2022-08-01 17:36:49
FilePath: \AITools\Video\step2-videos2images_multi_thread.py
Description: 
Email: 497291093@qq.com
Copyright (c) 2022 by Siyuan Li - ZHONGCHAO XINDA, All Rights Reserved. 
'''
#coding: utf-8

import threading
from utils import *


def process_videos(video_files, image_save_path, interval, start_frame):
    # for idx in tqdm.tqdm(range(len(video_files))):
    for video_file in video_files:
        try:
            # video_file = video_files[idx]
            print("{} process: {}".format(threading.currentThread, video_file))
            video_to_images(video_file, image_save_path, interval=interval, start_frame=start_frame)
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
    video_path = r'F:/Data/ActionDet/train_data/FaceMask'
    video_path = r'F:/Data/ActionDet/按摄像头分类/通过台2'
    image_save_path = video_path+'_images'
    image_save_path='F:/Data/ActionDet/train_data/FaceMask_Connect2'+'_images'
    files = get_file_list(video_path)
    video_files = files_filter(files, ['mp4', 'MP4'])
    print("video_files: ", video_files)
    video_files.sort()
    print(len(video_files))

    thread_count = 16 #16
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
        th = myThread(threadID, "process videos", videos, image_save_path, interval=2400)       # 正面800
        jobs.append(th)

    for job in jobs:
        job.start()

    for job in jobs:
        job.join()

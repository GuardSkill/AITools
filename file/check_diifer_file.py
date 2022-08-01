'''
Author: Siyuan Li
Date: 2022-06-21 11:04:12
LastEditors: Siyuan Li
LastEditTime: 2022-08-01 14:54:15
FilePath: \AITools\file\check_diifer_file.py
Description: 将图像重名令为从1开始的图像
Email: 497291093@qq.com
Copyright (c) 2022 by Siyuan Li. 
'''
# 两个文件夹有一些相同的文件，寻找两个文件夹中，A文件夹缺失的文件

import os

def listDir(rootDir, image_list, endwith):
    files = os.listdir(rootDir)
    for filename in os.listdir(rootDir):
        pathname = os.path.join(rootDir, filename)
        if os.path.isfile(pathname):
            if pathname.split(".")[-1].lower() in endwith:
                image_list.append(pathname)
        else:
            listDir(pathname, image_list, endwith)

if __name__ == "__main__":  
    A=[]
    B=[]
    listDir("F:/Data/行为检测/raw_videos",A,'mp4')
    listDir("F:/Data/行为检测/摄像头分类",B,'mp4')
    A=[os.path.basename(x) for x in A ]
    B=[os.path.basename(x) for x in B ]
    print( [x for x in A if x not in B])
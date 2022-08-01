'''
Author: Siyuan Li
Date: 2022-06-21 11:04:12
LastEditors: Siyuan Li
LastEditTime: 2022-08-01 15:24:12
FilePath: \AITools\file\rename.py
Description: 将图像重名令为从1开始的图像
Email: 497291093@qq.com
Copyright (c) 2022 by Siyuan Li - ZHONGCHAO XINDA, All Rights Reserved. 
'''
# ubuntu重名令jpg图像命令
#  find . -name "*.jpg" -exec mogrify -format png {} \;

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

def rename_subfiles(path):
    filelist = os.listdir(path)
    count=0
    for file in filelist:
        print(file)
    for file in filelist:   
        oldname=os.path.join(path,file)  
        if os.path.isdir(oldname):  
            continue
        filename=os.path.splitext(file)[0]   
        filetype=os.path.splitext(file)[1]  
        newname=os.path.join(path,str(count).zfill(3)+filetype)  
        os.rename(oldname,newname)
        count+=1
def rename_allfiles(path,prefix=''):
    filelist=[]
    # listDir(path,filelist,["jpg", "png"])
    listDir(path,filelist,["mp4"])
    count=0
    for file in filelist:
        print(file)
    for file in filelist:   
        oldname=file
        if os.path.isdir(oldname):  
            continue
        filename=os.path.splitext(file)[0]   
        filetype=os.path.splitext(file)[1]  
        dir_name=os.path.dirname(file)
        newname=os.path.join(dir_name,str(count).zfill(3)+prefix+filetype)  
        os.rename(oldname,newname)
        count+=1

if __name__ == "__main__":  
    # path = "dataset/MVTec/jiancepen_origin/train/good"
    # path ="/data2/lisiyuan/datasets/AnormalDetProbe_v2/jiancepen_origin/train/good"

    path ="F:\Data\行为检测\摄像头分类\通过台1"
    rename_allfiles(path,'_Connector1')

    path ="F:\Data\行为检测\摄像头分类\通过台2"
    rename_allfiles(path,'_Connector2')
    
    path ="F:\Data\行为检测\摄像头分类\VIP区"
    rename_allfiles(path,'_VIP')

    path ="F:\Data\行为检测\摄像头分类\司机室通道"
    rename_allfiles(path,'_DriverRoom')

    path ="F:\Data\行为检测\摄像头分类\正面摄像头"
    rename_allfiles(path,'_FrontCam')

    path ="F:\Data\行为检测\摄像头分类\背面摄像头"
    rename_allfiles(path,'_BackCam')

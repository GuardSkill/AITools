'''
Author: Siyuan Li
Date: 2022-06-21 11:04:12
LastEditors: Siyuan Li
LastEditTime: 2022-06-28 16:56:21
FilePath: \AITools\file\rename.py
Description: 将图像重名令为从1开始的图像
Email: 497291093@qq.com
Copyright (c) 2022 by Siyuan Li. 
'''
# ubuntu重名令jpg图像命令
#  find . -name "*.jpg" -exec mogrify -format png {} \;

import os
path = "dataset/MVTec/jiancepen_origin/train/good"
path= "F:/Data/WorkshedDetectTrain/FalsePredict/202206_pole"
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
    newname=os.path.join('202206_pole',path,str(count).zfill(3)+filetype)  
    os.rename(oldname,newname)
    count+=1

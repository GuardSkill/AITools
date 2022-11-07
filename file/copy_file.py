'''
Author: Siyuan Li
Date: 2022-09-23 14:50:26
LastEditors: Siyuan Li
LastEditTime: 2022-10-08 17:00:42
FilePath: \AITools\file\copy_file.py
Description: 
Email: 497291093@qq.com
Copyright (c) 2022 by Siyuan Li - ZHONGCHAO XINDA, All Rights Reserved. 
'''
import os
from shutil import copyfile

src=r"\\192.168.31.10\AlgorithmData\Data\ZNJT\ZhongChe_ChengKeXingWei\20220808_1w_video\没处理的"
dst=r'\\192.168.31.10\AlgorithmData\Data\ZNJT\ZhongChe_ChengKeXingWei\20220808_1w_video\没处理的_6_stride'

src=r"F:\Data\Datasets\FireDetection\ObjectDetction\fire-dataset-2"
dst=r"F:\Data\Datasets\FireDetection\ObjectDetction\fire-dataset-2-stride10"

src=r"\\192.168.31.10\AlgorithmData\Data\ZNJT\ZhongChe_ChengKeXingWei\20220926\20220926_4_stride_facemask"
dst=r"\\192.168.31.10\AlgorithmData\Data\ZNJT\ZhongChe_ChengKeXingWei\20220926\20220926_4_stride_facemask2"
condition_folder=r"\\192.168.31.10\AlgorithmData\Data\ZNJT\ZhongChe_ChengKeXingWei\20220926\NeedAlter"

def listDir(rootDir, image_list, endwith):
    files = os.listdir(rootDir)
    for filename in os.listdir(rootDir):
        pathname = os.path.join(rootDir, filename)
        if os.path.isfile(pathname):
            if pathname.split(".")[-1].lower() in endwith:
                image_list.append(pathname)
        else:
            listDir(pathname, image_list, endwith)

def copy_files_and_label_with_stride(src,dst,stride=1):
    '''
    拷贝图像以及它的标签。stride表示间隔
    '''
    image_list=[]
    endwith=['png']
    listDir(src, image_list, endwith)
    os.makedirs(dst,exist_ok=True)
    image_list.sort()
    for index,img_path in enumerate(image_list):
        if index%stride!=0:
            continue
        copyfile(img_path,os.path.join(dst,os.path.basename(img_path)))
        json_name=img_path.replace("png","json")
        if os.path.exists(json_name):
             copyfile(json_name,os.path.join(dst,os.path.basename(json_name)))

def copy_files_and_label_with_stride_in_different_folders(src,dst,stride=1):
    '''
    拷贝图像以及它的标签。stride表示间隔,图像和标签在不同的文件夹
    '''
    image_list=[]
    endwith=['jpg']
    listDir(src+r'\train', image_list, endwith)
    os.makedirs(dst,exist_ok=True)
    os.makedirs(dst+r'\train\images',exist_ok=True)
    os.makedirs(dst+r'\train\labels',exist_ok=True)
    os.makedirs(dst+r'\valid',exist_ok=True)
    image_list.sort()
    for index,img_path in enumerate(image_list):
        if index%stride!=0 and "mp4" in img_path:
            continue
        copyfile(img_path,os.path.join(dst+r'\train\images',os.path.basename(img_path)))
        json_name=img_path.replace(".jpg",".txt")
        json_name=json_name.replace("images","labels")
        if os.path.exists(json_name):
             copyfile(json_name,os.path.join(dst+r'\train\labels',os.path.basename(json_name)))

def copy_files_with_stride(src,dst,stride=1):
    '''
    带间隔地拷贝一些图像
    '''
    image_list=[]
    endwith=['png']
    listDir(src, image_list, endwith)
    os.makedirs(dst,exist_ok=True)
    image_list.sort()
    for index,img_path in enumerate(image_list):
        if index%stride!=0:
            continue
        copyfile(img_path,os.path.join(dst,os.path.basename(img_path)))

def copy_files_with_condition(src,dst,condition_folder):
    '''
    移动两个文件夹中共有的文件（文件名相同的文件）到新的文件夹。
    '''
    image_list=[]
    endwith=['png']
    listDir(src, image_list, endwith)
    need_list=[]
    listDir(condition_folder, need_list, endwith)
    need_name=[os.path.basename(path) for path in need_list]
    new_list=[]
    for path in image_list:
        if os.path.basename(path) in need_name:
            new_list.append(path)
    image_list=new_list
    os.makedirs(dst,exist_ok=True)
    image_list.sort()
    for index,img_path in enumerate(image_list):
        copyfile(img_path,os.path.join(dst,os.path.basename(img_path)))


# src=r"\\192.168.31.10\AlgorithmData\Data\ZNJT\ZhongChe_ChengKeXingWei\20220808_1w_video\06_01_cam2"
# src=r"F:\Data\Datasets\FireDetection\fire-dataset-dunnings\images-224x224\train\nofire"
# dst=r'\\192.168.31.10\AlgorithmData\Data\ZNJT\ZhongChe_ChengKeXingWei\20220808_1w_video\06_01_cam2_stride'
# dst=r"F:\Data\Datasets\FireDetection\fire-dataset-dunnings\images-224x224\train\nofire_stride"
# copy_files_and_label_with_stride(src,dst,6)
# copy_files_and_label_with_stride_in_different_folders(src,dst,18)
# copy_files_with_stride(src,dst,stride=4)


copy_files_with_condition(src,dst,condition_folder)
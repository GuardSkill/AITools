'''
Author: Siyuan Li
Date: 2022-06-21 11:04:12
LastEditors: Siyuan Li
LastEditTime: 2022-10-08 13:48:07
FilePath: \AITools\file\rename.py
Description: 将图像重名令为从1开始的图像
Email: 497291093@qq.com
Copyright (c) 2022 by Siyuan Li - ZHONGCHAO XINDA, All Rights Reserved. 
'''
# ubuntu重名令jpg图像命令
#  find . -name "*.jpg" -exec mogrify -format png {} \;
import os
import json
path=r"\\192.168.31.10\AlgorithmData\Data\ZNJT\ShangHai_jcp\LabelData\NeedLabel"
path=r"\\192.168.31.10\AlgorithmData\Data\ZNJT\ShangHai_jcp\LabelData\20221101_hat_clothes\AllAddLabel"

prefix="NJNHeadCloth20221101_"
postfix=['png','jpg','jpeg']

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
        newname=os.path.join(path,str(count).zfill(4)+filetype)  
        os.rename(oldname,newname)
        count+=1
def rename_allfiles(path,prefix='',postfix=["jpg", "png"]):
    filelist=[]
    listDir(path,filelist,postfix)
    # listDir(path,filelist,["mp4"])
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
        newname=os.path.join(dir_name,prefix+str(count).zfill(4)+filetype)  
        os.rename(oldname,newname)
        count+=1

def rename_allfiles_with_label(path,prefix='',postfix=["jpg", "png"]):
    filelist=[]
    listDir(path,filelist,postfix)
    # listDir(path,filelist,["mp4"])
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
        newname=os.path.join(dir_name,prefix+str(count).zfill(5)+filetype)  
        os.rename(oldname,newname)
        oldname=oldname.replace(filetype,".json")
        filetype='.json'
        new_json_name=os.path.join(dir_name,prefix+str(count).zfill(5)+filetype)  
        os.rename(oldname,new_json_name)
        try:    
            json_obj = json.load(open(new_json_name, "r", encoding="utf-8"))
            json_obj['imagePath']=os.path.basename(newname)
            with open(new_json_name,'w') as outfile:
                json.dump(json_obj,outfile)
        except:
            print(newname,"is a backgroud img")
        finally:
            None
        count+=1
def generate_json_for_allfiles(one_json_path,path):
    '''
    根据模板标签文件为其他图像复制和生成标签，适用于视频中很对标签都是完全相同的情况
    '''
    filelist=[]
    # listDir(path,filelist,["jpg", "png"])
    listDir(path,filelist,["mp4",'png'])
    count=0
    f = open(one_json_path, 'r')
    content = f.read()
    temp_json=json.loads(content)
    for file in filelist:
        print(file)
        dir_name=os.path.dirname(file)
        filename=os.path.splitext(file)[0] 
        filetype=os.path.splitext(file)[1]
        temp_json["imagePath"]=os.path.basename(file)
        newjson=os.path.join(dir_name,filename+".json")
        b = json.dumps(temp_json)
        f2 = open(newjson, 'w')
        f2.write(b)
        f2.close()
    f.close()

if __name__ == "__main__":  
    # rename_allfiles(path,prefix,postfix)
    rename_allfiles_with_label(path,prefix,postfix)


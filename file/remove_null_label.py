import os
import json
import cv2
from shutil import copyfile

# src=r"\\192.168.31.10\AlgorithmData\Data\ZNJT\ZhongChe_ChengKeXingWei\train_images\Lean_label\Lean_11_02"
# dst=r"\\192.168.31.10\AlgorithmData\Data\ZNJT\ZhongChe_ChengKeXingWei\train_images\Lean_label\Lean_11_02_No_background_label"
# src=r"\\192.168.31.10\AlgorithmData\Data\ZNJT\ZhongChe_ChengKeXingWei\train_images\FaceMask_label\FaceMask_1027"
# dst=r"\\192.168.31.10\AlgorithmData\Data\ZNJT\ZhongChe_ChengKeXingWei\train_images\FaceMask_label\FaceMask_1027_ALL"
# src=r"\\192.168.31.10\AlgorithmData\Data\ZNJT\ZhongChe_ChengKeXingWei\train_images\Packages_label\Package"
# dst=r"\\192.168.31.10\AlgorithmData\Data\ZNJT\ZhongChe_ChengKeXingWei\train_images\Packages_label\Package_1027_ALL"
src=r"\\192.168.31.10\AlgorithmData\Data\ZNJT\ZhongChe_ChengKeXingWei\train_images\Smoking_label\Smoking"
dst=r"\\192.168.31.10\AlgorithmData\Data\ZNJT\ZhongChe_ChengKeXingWei\train_images\Smoking_label\Smoking_1109_ALL"


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


def copy_files_and_label_with_stride_save_jpgimg(src,dst,stride=1):
    '''
    拷贝图像以及它的标签。stride表示间隔,新图像用jpg存储。
    并删除冗余的json文件。
    '''
    image_list=[]
    endwith=['png']
    endwith=postfix
    listDir(src, image_list, endwith)
    os.makedirs(dst,exist_ok=True)
    image_list.sort()
    for index,img_path in enumerate(image_list):
        if index%stride!=0:
            continue
        filename=os.path.splitext(img_path)[0]   
        filename=os.path.basename(filename)
        filetype=os.path.splitext(img_path)[1]        # this is .png !!!!!!!!!!!!!
        json_name=img_path.replace(filetype,".json")  
        newname=os.path.join(dst,filename+'.jpg')
        new_json_name=os.path.join(dst,os.path.basename(json_name)) 
        if filetype=='jpg':
            copyfile(img_path,newname)
            if os.path.exists(json_name):
                try:    
                    json_obj = json.load(open(json_name, "r", encoding="utf-8"))
                    x=json_obj['imagePath']
                    json_obj['imagePath']=json_obj['imagePath']
                    copyfile(json_name,new_json_name)
                except:
                    print(newname,"is a backgroud img, we won't move label")
                finally:
                    None
        else:
            img=cv2.imread(img_path)
            cv2.imwrite(newname,img)
            if os.path.exists(json_name):
                try:   
                    json_obj = json.load(open(json_name, "r", encoding="utf-8"))
                    x=json_obj['imagePath']
                    json_obj['imagePath']=os.path.basename(newname)
                    with open(new_json_name,'w') as outfile:
                        json.dump(json_obj,outfile)
                except:
                    print(newname,"is a backgroud img, we won't move label")
                finally:
                    None

copy_files_and_label_with_stride_save_jpgimg(src,dst,stride=1)
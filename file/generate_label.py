import os
import json
def listDir(rootDir, image_list, endwith):
    files = os.listdir(rootDir)
    for filename in os.listdir(rootDir):
        pathname = os.path.join(rootDir, filename)
        if os.path.isfile(pathname):
            if pathname.split(".")[-1].lower() in endwith:
                image_list.append(pathname)
        else:
            listDir(pathname, image_list, endwith)

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

one_json_path=r"\\192.168.31.10\AlgorithmData\lisiyuan\Workshed_OD\20221114\Switch\ALL_Close_images\221114_SwitchClose_0000.json"
path=r"\\192.168.31.10\AlgorithmData\lisiyuan\Workshed_OD\20221114\Switch\ALL_Close_images"
one_json_path=r"\\192.168.31.10\AlgorithmData\lisiyuan\Workshed_OD\20221114\Switch\Open_images\221114_SwitchOpen_0000.json"
path=os.path.dirname(one_json_path)
generate_json_for_allfiles(one_json_path,path)
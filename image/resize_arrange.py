import glob
import os

import cv2
import numpy as np

def get_flist(flist):
    flist = list(glob.glob(flist + '/*.jpg')) + list(glob.glob(flist + '/*.png')) + list(
        glob.glob(flist + '/*.jfif'))
    flist.sort()
    return flist
# File=r"\3.png"
# position=(377,439)
# File=r"\69.png"
# position=(250,275)
File=r"\465.jpg"
# position=(564,181)
imgs=[]
# crop_imgs=[]
FilePaths=[]
dir="../MaterialRet"

# FilePath=dir+r"\raw"
# FilePaths.append(FilePath)
# FilePath=dir+"\damaged"
# FilePaths.append(FilePath)
# FilePath=dir+"\CA"
# FilePaths.append(FilePath)

# FilePath="/home/sobey/PycharmProjects/Inpainting/Example/Place2/Output/CoModGAN_OutputInput"
FilePath="/home/sobey/Dataset/Material/img"
FilePaths.append(FilePath)
FilePath='/home/sobey/Dataset/Material/CoModGAN_Out/Damaged'
FilePaths.append(FilePath)
FilePath='/home/sobey/Dataset/Material/MADF_Out'
FilePaths.append(FilePath)
FilePath='/home/sobey/Dataset/Material/PicUP_Out'
FilePaths.append(FilePath)
FilePath='/home/sobey/Dataset/Material/CoModGAN_Out/Out'
FilePaths.append(FilePath)

# FilePaths.append(FilePath)
# FilePath=r"D:\OneDrive\Lab\Results\chanllenge\31.701_Sobel_val27.29_train28.90\OR"
# FilePaths.append(FilePath)
# FilePath=r"D:\OneDrive\Lab\Results\chanllenge\31.3246_val28.23_train28.68\EC"
# FilePath=r"E:\Dataset\test_data\predict\OR"

# Output=dir+r'\concatenate'


for j in range(0,4):
    File = r"/{}.png".format(str(j))
    imgs = []
    for i in range(FilePaths.__len__()):
        # path=FilePaths[i]+File
        path=get_flist(FilePaths[i])[j]
        img = cv2.imread(path)
        # img=cv2.resize(img, (int(256), int(256)))
        img = cv2.copyMakeBorder(img, top=3, bottom=3, left=3, right=3,
                                      borderType=cv2.BORDER_CONSTANT, value=[255, 255, 255])
        imgs.append(img)

    vis = np.concatenate(imgs, axis=1)
    # f_path=os.path.join(dir,'/{}.png'.format(str(j)))
    f_path=dir+'/{}.png'.format(str(j))
    cv2.imwrite(f_path,vis)

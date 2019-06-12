import cv2
import numpy as np

# File=r"\3.png"
# position=(377,439)
# File=r"\69.png"
# position=(250,275)
File=r"\12.png"
position=(564,181)
imgs=[]
crop_imgs=[]
FilePaths=[]

FilePath=r"E:\Dataset\test_data\OR\damaged_img"
FilePaths.append(FilePath)
FilePath=r"D:\OneDrive\Lab\Results\chanllenge\ori_imagenet_model\OR"
# FilePaths.append(FilePath)
# FilePath=r"D:\OneDrive\Lab\Results\chanllenge\31.701_Sobel_val27.29_train28.90\OR"
# FilePaths.append(FilePath)
# FilePath=r"D:\OneDrive\Lab\Results\chanllenge\31.3246_val28.23_train28.68\EC"
# FilePath=r"E:\Dataset\test_data\predict\OR"
FilePaths.append(FilePath)
Output=r'D:\OneDrive\Lab\Results\chanllenge'



for i in range(FilePaths.__len__()):
    FilePaths[i]=FilePaths[i]+File
    img = cv2.imread(FilePaths[i])
    img=cv2.resize(img, (int(512), int(512)))
    img = cv2.copyMakeBorder(img, top=3, bottom=3, left=3, right=3,
                                  borderType=cv2.BORDER_CONSTANT, value=[255, 255, 255])
    imgs.append(img)

vis = np.concatenate(imgs, axis=1)
cv2.imwrite(Output+r'\OR_re6.png', vis)
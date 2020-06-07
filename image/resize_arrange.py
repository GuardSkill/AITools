import cv2
import numpy as np

# File=r"\3.png"
# position=(377,439)
# File=r"\69.png"
# position=(250,275)
File=r"\465.jpg"
# position=(564,181)
imgs=[]
# crop_imgs=[]
FilePaths=[]
dir=r"C:\Users\49729\Desktop\results\Others\Places2"

FilePath=dir+r"\raw"
FilePaths.append(FilePath)
FilePath=dir+"\damaged"
FilePaths.append(FilePath)
FilePath=dir+"\CA"
FilePaths.append(FilePath)
FilePath=dir+"\edge-connect"
FilePaths.append(FilePath)
FilePath=dir+"\ICONIP2020"
FilePaths.append(FilePath)

# FilePaths.append(FilePath)
# FilePath=r"D:\OneDrive\Lab\Results\chanllenge\31.701_Sobel_val27.29_train28.90\OR"
# FilePaths.append(FilePath)
# FilePath=r"D:\OneDrive\Lab\Results\chanllenge\31.3246_val28.23_train28.68\EC"
# FilePath=r"E:\Dataset\test_data\predict\OR"

# Output=dir+r'\concatenate'


for j in range(1,100):
    File = r"\{}.jpg".format(str(j))
    imgs = []
    for i in range(FilePaths.__len__()):
        path=FilePaths[i]+File
        img = cv2.imread(path)
        # img=cv2.resize(img, (int(256), int(256)))
        img = cv2.copyMakeBorder(img, top=3, bottom=3, left=3, right=3,
                                      borderType=cv2.BORDER_CONSTANT, value=[255, 255, 255])
        imgs.append(img)

    vis = np.concatenate(imgs, axis=1)
    cv2.imwrite(dir+r'\{}.png'.format(str(j)), vis)

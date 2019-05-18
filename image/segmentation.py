import cv2
import numpy as np

# File=r"\3.png"
# position=(377,439)
# File=r"\69.png"
# position=(250,275)
File=r"\32.png"
position=(564,181)
imgs=[]
crop_imgs=[]
FilePaths=[]

FilePath=r"E:\Dataset\test_data\EC\damaged_img"
FilePaths.append(FilePath)
FilePath=r"D:\OneDrive\Lab\Results\chanllenge\ori_imagenet_model\EC"
FilePaths.append(FilePath)
FilePath=r"D:\OneDrive\Lab\Results\chanllenge\31.701_Sobel_val27.29_train28.90\EC"
FilePaths.append(FilePath)
# FilePath=r"D:\OneDrive\Lab\Results\chanllenge\31.3246_val28.23_train28.68\EC"
FilePath=r"E:\Dataset\test_data\predict\EC"
FilePaths.append(FilePath)
Output=r'D:\OneDrive\Lab\Results\chanllenge'

for i in range(FilePaths.__len__()):
    FilePaths[i]=FilePaths[i]+File
    img = cv2.imread(FilePaths[i])
    imgs.append(img)

kernel_x, kernel_y = 120, 120
i=0
for img in imgs:
    x, y = position
    crop_img = img[y:y+kernel_x, x:x+kernel_y]
    crop_img=cv2.copyMakeBorder(crop_img, top=3, bottom=3, left=3, right=3,
                        borderType=cv2.BORDER_CONSTANT, value=[255, 255, 255])
    crop_imgs.append(crop_img)
vis = np.concatenate(crop_imgs, axis=1)
cv2.imwrite(Output+r'\re3.png', vis)
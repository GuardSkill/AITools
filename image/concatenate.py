import cv2
import numpy as np

PIC_NUM = 3
FilePATH = r'D:\OneDrive\Lab\Results\chanllenge'
imgs = []

for i in range(1, PIC_NUM + 1):
    File = FilePATH + r"\re{}.png".format(i)
    img = cv2.imread(File)
    imgs.append(img)
vis = np.concatenate(imgs, axis=0)
cv2.imwrite(FilePATH + r'\Result.png', vis)

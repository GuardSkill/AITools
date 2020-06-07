import cv2
import numpy as np

# concatenate some images (across rows)
PIC_NUM = 6
FilePATH = r'C:\Users\49729\Desktop\results\Others'
imgs = []

for i in range(1, PIC_NUM + 1):
    File = FilePATH + r"\{}.png".format(i)
    img = cv2.imread(File)
    imgs.append(img)
vis = np.concatenate(imgs, axis=0)
cv2.imwrite(FilePATH + r'\Result.png', vis)

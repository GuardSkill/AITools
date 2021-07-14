import cv2
import numpy as np

# concatenate some images (across rows)
PIC_NUM = 4
FilePATH = r'../MaterialRet'
imgs = []

for i in range(0, PIC_NUM):
    File = FilePATH + r"/{}.png".format(i)
    img = cv2.imread(File)
    imgs.append(img)
vis = np.concatenate(imgs, axis=0)
cv2.imwrite(FilePATH + r'/Result.png', vis)

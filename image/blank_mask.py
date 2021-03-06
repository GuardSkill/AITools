import random
import os
from PIL import Image,ImageOps
from glob import glob
import numpy as np
import cv2

img_dir='E:\PyProjects\edge-connect-master\examples\places2\images'
mask_dir='E:\PyProjects\edge-connect-master\examples\places2\masks'
ext = {'.JPG', '.JPEG', '.PNG', '.TIF', 'TIFF'}
img_paths=[]
mask_paths =[]

i=1

for file in glob('{:s}/*'.format(img_dir)):
    if os.path.splitext(file)[1].upper() in ext:
        img_paths.append(file)

for file in glob('{:s}/*'.format(mask_dir)):
    if os.path.splitext(file)[1].upper() in ext:
        mask_paths.append(file)

N_img=len(img_paths)
N_mask=len(mask_paths)
N_mini=N_mask if N_img>N_mask else N_img

for i in range(N_mini):
    mask = cv2.imread(mask_paths[i])
    kernel = np.ones((6, 6), np.uint8)
    er_kernel = np.ones((3, 3), np.uint8)
    img_dilation = cv2.dilate(mask, kernel, iterations=1)
    mask=np.array(img_dilation)
    img = np.array(cv2.imread(img_paths[i]))
    img[mask != 0] = 0
    Image.fromarray(img).save(img_paths[i])


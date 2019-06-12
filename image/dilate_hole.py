import cv2
import os
from PIL import Image,ImageOps
from glob import glob
import numpy as np

# dialate holes in mask map for bird dataset
img_dir='E:\PyProjects\edge-connect-master\examples\places2\images'
mask_dir='E:\PyProjects\edge-connect-master\examples\places2\masks'
ext = {'.JPG', '.JPEG', '.PNG', '.TIF', 'TIFF'}
img_paths=[]
mask_paths =[]

i=1

# resize img
for file in glob('{:s}/*'.format(img_dir)):
    if os.path.splitext(file)[1].upper() in ext:
        img_paths.append(file)
        img=cv2.imread(file)
        if img.shape[0]!=512|img.shape[1]!=512:
            img=cv2.resize(img,(512,512),interpolation = cv2.INTER_CUBIC)
            os.remove(file)
            cv2.imwrite(os.path.splitext(file)[0]+'.png',img)

# resize mask and dilate it
for file in glob('{:s}/*'.format(mask_dir)):
    if os.path.splitext(file)[1].upper() in ext:
        mask_paths.append(file)
        img = cv2.imread(file)
        if img.shape[0] != 512|img.shape[1] != 512:
            img=cv2.resize(img, (512, 512), interpolation=cv2.INTER_CUBIC)
        ret, img = cv2.threshold(img, 1, 255, cv2.THRESH_BINARY)
        kernel = np.ones((5, 5), np.uint8)
        img_dilation = cv2.dilate(img, kernel, iterations=2)
        ret, img = cv2.threshold(img_dilation, 1, 255, cv2.THRESH_BINARY)
        os.remove(file)
        img=cv2.imwrite(os.path.splitext(file)[0]+'.png',img)


N_img=len(img_paths)
N_mask=len(mask_paths)
N_mini=N_mask if N_img>N_mask else N_img

# for i in range(N_mini):
#     img=np.array(Image.open(img_paths[i]))
#     mask = np.array(Image.open(mask_paths[i]))
#     img[mask != 0] = 255
#     Image.fromarray(img).save(img_paths[i])

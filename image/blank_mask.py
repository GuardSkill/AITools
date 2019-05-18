import random
import os
from PIL import Image,ImageOps
from glob import glob
import numpy as np

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
    img=np.array(Image.open(img_paths[i]))
    mask = np.array(Image.open(mask_paths[i]))
    img[mask != 0] = 0
    Image.fromarray(img).save(img_paths[i])

def create_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

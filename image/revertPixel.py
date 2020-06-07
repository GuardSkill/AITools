import random
from PIL import Image,ImageOps
from glob import glob
#str1='E:/PyProjects/pytorch-inpainting-with-partial-conv-master/mask/NVDIA_mask_dataset'
str1='E://mask'
mask_paths = glob('{:s}/*.png'.format(str1))
N_mask = len(mask_paths)
i=1
for mask_path in mask_paths:
    mask = Image.open(mask_path)
    # pixels = mask.load()
    # r, g, b = mask.getpixel((79, 86))
    # for i in range(mask.size[0]):  # for every pixel:
    #     for j in range(mask.size[1]):
    #         if pixels[i, j] <= (122, 122, 122):
    #             pixels[i, j] = (255, 255, 255)
    #         else:
    #             pixels[i, j] = (0, 0, 0)
    # mask.save(str1+'/Mask.jpg')
    mask_inv=ImageOps.invert(mask)
    mask_inv.save(mask_path)
   #mask_inv.save(str1+'/Mask'+str(i)+'.jpg')
    i=i+1

def __len__(self):
    return len(self.paths)

import os
from glob import glob

img_dir='./damaged/'
mask_dir='./mask/'
output_dir='./output/'
ext = {'.JPG', '.JPEG', '.PNG', '.TIF', 'TIFF'}
img_paths=[]
mask_paths =[]

i=1

for img_path in glob('{:s}/*'.format(img_dir)):
    if os.path.splitext(img_path)[1].upper() in ext:
        img_paths.append(img_path)
        base_name=os.path.basename(img_path)
        mask_base_name=os.path.splitext(base_name)[0]+'.png'
        mask_path=os.path.join(mask_dir,mask_base_name)
        mask_paths.append(mask_path)
        # print(img_path,mask_path)


# for file in glob('{:s}/*'.format(mask_dir)):
#     if os.path.splitext(file)[1].upper() in ext:
#         mask_paths.append(file)

N_img=len(img_paths)
N_mask=len(mask_paths)
N_mini=N_mask if N_img>N_mask else N_img

for i in range(N_mini):
    # print(mask_paths[i],img_paths[i])
    output_path=os.path.join(output_dir,os.path.basename(img_paths[i]))
    os.system("th inpaint.lua --input {} --mask {} --nopostproc".format(img_paths[i], mask_paths[i]))
    os.system("mv out.png {}".format(output_path))


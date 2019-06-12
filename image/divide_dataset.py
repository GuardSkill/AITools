import os
from glob import glob
import cv2
import numpy as np
from util.systools import create_dir

MASK_DIR = "E:\Dataset\Mask\IrregularHoles"
BASE_DIR = os.path.dirname(MASK_DIR)
mask_paths = glob('{:s}/*.jpg'.format(MASK_DIR))

for mask in mask_paths:
    msk = np.array(cv2.imread(mask, cv2.IMREAD_GRAYSCALE))
    NoHoleNum = np.count_nonzero(msk)
    ratio = (msk.size - NoHoleNum) / msk.size
    if (ratio < 0.2) & (ratio > 0.1):
        create_dir(BASE_DIR + '\MaskSize1')
        cv2.imwrite(BASE_DIR + '/MaskSize1/' + os.path.basename(mask), msk)
    elif (ratio > 0.2) & (ratio < 0.3):
        create_dir(BASE_DIR + '\MaskSize2')
        cv2.imwrite(BASE_DIR + '/MaskSize2/' + os.path.basename(mask), msk)
    elif (ratio > 0.3) & (ratio < 0.4):
        create_dir(BASE_DIR + '\MaskSize3')
        cv2.imwrite(BASE_DIR + '/MaskSize3/' + os.path.basename(mask), msk)
    elif (ratio > 0.4) & (ratio < 0.5):
        create_dir(BASE_DIR + '\MaskSize4')
        cv2.imwrite(BASE_DIR + '/MaskSize4/' + os.path.basename(mask), msk)

import glob
import os

import onnxruntime as rt
import numpy as np
import time
import cv2
from decode import SegDetectorRepresenter
# from psenet.PSENET import SingletonType


class SingletonType(type):
    def __init__(cls, *args, **kwargs):
        super(SingletonType, cls).__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        obj = cls.__new__(cls, *args, **kwargs)
        cls.__init__(obj, *args, **kwargs)
        return obj

mean = (0.485, 0.456, 0.406)
std = (0.229, 0.224, 0.225)


def draw_bbox(img_path, result, color=(255, 0, 0), thickness=2):
    if isinstance(img_path, str):
        img_path = cv2.imread(img_path)
        # img_path = cv2.cvtColor(img_path, cv2.COLOR_BGR2RGB)
    img_path = img_path.copy()
    for point in result:
        point = point.astype(int)

        cv2.polylines(img_path, [point], True, color, thickness)
    return img_path


class DBNET(metaclass=SingletonType):
    def __init__(self, MODEL_PATH, short_size=640):
        self.sess = rt.InferenceSession(MODEL_PATH)
        self.short_size = short_size
        self.decode_handel = SegDetectorRepresenter()

    def process(self, img):

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w = img.shape[:2]

        if h < w:
            scale_h = self.short_size / h
            tar_w = w * scale_h
            tar_w = tar_w - tar_w % 32
            tar_w = max(32, tar_w)
            scale_w = tar_w / w

        else:
            scale_w = self.short_size / w
            tar_h = h * scale_w
            tar_h = tar_h - tar_h % 32
            tar_h = max(32, tar_h)
            scale_h = tar_h / h

        img = cv2.resize(img, None, fx=scale_w, fy=scale_h)

        img = img.astype(np.float32)

        img /= 255.0
        img -= mean
        img /= std
        img = img.transpose(2, 0, 1)
        transformed_image = np.expand_dims(img, axis=0)
        out = self.sess.run(["out1"], {"input0": transformed_image.astype(np.float32)})
        box_list, score_list = self.decode_handel(out[0][0], h, w)
        if len(box_list) > 0:
            idx = box_list.reshape(box_list.shape[0], -1).sum(axis=1) > 0  # 去掉全为0的框
            box_list, score_list = box_list[idx], score_list[idx]
        else:
            box_list, score_list = [], []
        return box_list, score_list


def create_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
def get_flist(flist):
    flist = list(glob.glob(flist + '/*.jpg')) + list(glob.glob(flist + '/*.png')) + list(
        glob.glob(flist + '/*.jfif'))
    flist.sort()
    return flist

def infer_from_images(checkpoint="./models/dbnet.onnx", input_folder=None, output_folder=None):
    text_handle = DBNET(MODEL_PATH=checkpoint)
    if os.path.isdir(input_folder):
        if output_folder is None:
            output_folder='./outputs'
            output_folder=os.path.join(output_folder, os.path.basename(input_folder))
        create_dir(output_folder)
        if os.path.isfile(output_folder):
            print("ALL paths should be the folder, or all are image paths")
            return -1
        img_list = get_flist(input_folder)
        for file_name in img_list:
            img = cv2.imread(file_name)
            box_list, score_list = text_handle.process(img)
            img = draw_bbox(img, box_list)
            saved_path=os.path.join(output_folder, os.path.basename(file_name))
            cv2.imwrite(saved_path, img)
            print(f'img is writed - shape :{img.shape}')

if __name__ == "__main__":
    SINGE_IMAGE=0
    if SINGE_IMAGE:
        text_handle = DBNET(MODEL_PATH="./models/dbnet.onnx")
        # file_name = '/home/sobey/Dataset/Material/Video/字幕区域修复/其他/00002545.png'
        # file_name = '/Disk1/Video/央视频/frame200.png'
        file_name = '/home/sobey/Dataset/Material/Video/字幕区域修复/红色底板/00000298.png'

        # file_name ="./test_imgs/1.jpg"
        img = cv2.imread(file_name)
        print(img.shape)
        box_list, score_list = text_handle.process(img)
        img = draw_bbox(img, box_list)
        cv2.imwrite("test.jpg", img)
    else:
        input_folder = '/home/sobey/Dataset/Material/Video/字幕区域修复/其他'
        # input_folder = '/Disk1/Video/央视频'
        # output_folder='./少字_单一背景_新闻'
        output_folder =None
        infer_from_images(checkpoint="./models/dbnet.onnx", input_folder=input_folder, output_folder=output_folder)

import os

import io
import cv2

import random
import zipfile
from glob import glob
import math
import numpy as np
import torch.nn.functional as F
import torchvision.transforms as transforms
from PIL import Image, ImageOps, ImageDraw, ImageFilter

import torch
import torchvision
import torch.nn as nn
import torch.distributed as dist

# import matplotlib
# from matplotlib import pyplot as plt
# matplotlib.use('agg')

def get_mask_img_from_points_(mask_info, size, expand_size=10):
    '''
    针对输入待修复区域为矩形等情况的mask生成函数
    TODO: 实现支持多边形修复区域的mask功能
    '''
    h, w = size
    mask = np.ones((h, w, 3), dtype=np.uint8)
    new_rects = []
    for region_ in mask_info:
        if region_.get('region_type') == 'rectangle':
            rect = region_.get('points', [])
            assert len(rect) == 4, f'当修复框为矩形时，需要输入矩形四点坐标,而不能是{rect}'
            (b_h, b_h1, b_w, b_w1) = (max(0, rect[1] - expand_size), min(h, rect[3] + expand_size),
                                      max(0, rect[0] - expand_size), min(w, rect[2] + expand_size))
            mask[b_h:b_h1, b_w:b_w1] = 0
            new_rect = (b_h, b_h1, b_w, b_w1)
            new_rects.append(new_rect)
        else:
            NotImplementedError
    return (1 - mask) * 255, new_rects

def dilaited_mask( pil_mask, w, h, iter=4):
    m = pil_mask.copy()
    m = m.resize((w, h), Image.NEAREST)
    m = np.array(np.array(m) > 0).astype(np.uint8)
    m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3)), iterations=iter)
    return m

def read_mask( mask_paths,size=(432, 240), raw_w=1920, raw_h=1080,dilation=5):
    w, h = size
    masks = []
    raw_masks = []
    bboxs=[]
    for mask in mask_paths:
        if isinstance(mask, str):
            pil_raw_mask = Image.open(os.path.join(mask)).convert('L')  # binary Image  only 0/255
            m = dilaited_mask(pil_raw_mask, w, h)
            raw_masks.append(pil_raw_mask)
            masks.append(Image.fromarray(m * 255))
            bboxs.append(None)
        elif isinstance(mask, np.ndarray):
            pil_raw_mask = Image.fromarray(np.array(mask > 0).astype(np.uint8) * 255)
            m = dilaited_mask(pil_raw_mask, w, h)
            raw_masks.append(pil_raw_mask)
            masks.append(Image.fromarray(m * 255))
            bboxs.append(None)
        elif isinstance(mask, list):
            mask_origin, new_rects = get_mask_img_from_points_(mask, size=(raw_h, raw_w))
            # # 扩张方式1  Warning: 现在不可使用它
            # mask_expand = self.get_mask_img_from_points_(mask, size=(raw_h, raw_w),
            #                                              expand_size=dilation)  # 扩张实际需求修复的区域
            # mask_expand = np.array(Image.fromarray(mask_expand).resize((w, h)).convert('L'))
            # mask_expand = np.array(mask_expand > 0).astype(np.uint8)
            # pil_raw_mask = np.array(np.array(Image.fromarray(mask_origin).convert('L')) > 0).astype(np.uint8)
            # 扩张方式2
            pil_raw_mask = Image.fromarray(mask_origin).convert('L')
            mask_expand = dilaited_mask(pil_raw_mask, w, h, iter=1)  # 在矩形框很准的情况下，只迭代一次
            raw_masks.append(pil_raw_mask)
            masks.append(Image.fromarray(mask_expand * 255).convert('L'))
            bboxs.append(new_rects)
        else:
            raise TypeError(
                f'输入的待修复区域的类型存在问题')
    return raw_masks, masks,bboxs

# #####################################################
# #####################################################

class ZipReader(object):
    file_dict = dict()

    def __init__(self):
        super(ZipReader, self).__init__()

    @staticmethod
    def build_file_dict(path):
        file_dict = ZipReader.file_dict
        if path in file_dict:
            return file_dict[path]
        else:
            file_handle = zipfile.ZipFile(path, 'r')
            file_dict[path] = file_handle
            return file_dict[path]

    @staticmethod
    def imread(path, image_name):
        zfile = ZipReader.build_file_dict(path)
        data = zfile.read(image_name)
        im = Image.open(io.BytesIO(data))
        return im

# ###########################################################################
# ###########################################################################


class GroupRandomHorizontalFlip(object):
    """Randomly horizontally flips the given PIL.Image with a probability of 0.5
    """

    def __init__(self, is_flow=False):
        self.is_flow = is_flow

    def __call__(self, img_group, is_flow=False):
        v = random.random()
        if v < 0.5:
            ret = [img.transpose(Image.FLIP_LEFT_RIGHT) for img in img_group]
            if self.is_flow:
                for i in range(0, len(ret), 2):
                    # invert flow pixel values when flipping
                    ret[i] = ImageOps.invert(ret[i])
            return ret
        else:
            return img_group


class Stack(object):
    def __init__(self, roll=False):
        self.roll = roll

    def __call__(self, img_group):
        mode = img_group[0].mode
        if mode == '1':
            img_group = [img.convert('L') for img in img_group]
            mode = 'L'
        if mode == 'L':
            return np.stack([np.expand_dims(x, 2) for x in img_group], axis=2)
        elif mode == 'RGB':
            if self.roll:
                return np.stack([np.array(x)[:, :, ::-1] for x in img_group], axis=2)
            else:
                return np.stack(img_group, axis=2)
        else:
            raise NotImplementedError(f"Image mode {mode}")


class ToTorchFormatTensor(object):
    """ Converts a PIL.Image (RGB) or numpy.ndarray (H x W x C) in the range [0, 255]
    to a torch.FloatTensor of shape (C x H x W) in the range [0.0, 1.0] """

    def __init__(self, div=True):
        self.div = div

    def __call__(self, pic):
        if isinstance(pic, np.ndarray):
            # numpy img: [L, C, H, W]
            img = torch.from_numpy(pic).permute(2, 3, 0, 1).contiguous()
        else:
            # handle PIL Image
            img = torch.ByteTensor(
                torch.ByteStorage.from_buffer(pic.tobytes()))
            img = img.view(pic.size[1], pic.size[0], len(pic.mode))
            # put it from HWC to CHW format
            # yikes, this transpose takes 80% of the loading time/CPU
            img = img.transpose(0, 1).transpose(0, 2).contiguous()
        img = img.float().div(255) if self.div else img.float()
        return img


# ##########################################
# ##########################################

# def create_random_shape_with_random_motion(video_length, imageHeight=240, imageWidth=432):
#     # get a random shape
#     height = random.randint(imageHeight//3, imageHeight-1)
#     width = random.randint(imageWidth//3, imageWidth-1)
#     edge_num = random.randint(6, 8)
#     ratio = random.randint(6, 8)/10
#     region = get_random_shape(
#         edge_num=edge_num, ratio=ratio, height=height, width=width)
#     region_width, region_height = region.size
#     # get random position
#     x, y = random.randint(
#         0, imageHeight-region_height), random.randint(0, imageWidth-region_width)
#     velocity = get_random_velocity(max_speed=3)
#     m = Image.fromarray(np.zeros((imageHeight, imageWidth)).astype(np.uint8))
#     m.paste(region, (y, x, y+region.size[0], x+region.size[1]))
#     masks = [m.convert('L')]
#     # return fixed masks
#     if random.uniform(0, 1) > 0.5:
#         return masks*video_length
#     # return moving masks
#     for _ in range(video_length-1):
#         x, y, velocity = random_move_control_points(
#             x, y, imageHeight, imageWidth, velocity, region.size, maxLineAcceleration=(3, 0.5), maxInitSpeed=3)
#         m = Image.fromarray(
#             np.zeros((imageHeight, imageWidth)).astype(np.uint8))
#         m.paste(region, (y, x, y+region.size[0], x+region.size[1]))
#         masks.append(m.convert('L'))
#     return masks


# def get_random_shape(edge_num=9, ratio=0.7, width=432, height=240):
#     '''
#       There is the initial point and 3 points per cubic bezier curve.
#       Thus, the curve will only pass though n points, which will be the sharp edges.
#       The other 2 modify the shape of the bezier curve.
#       edge_num, Number of possibly sharp edges
#       points_num, number of points in the Path
#       ratio, (0, 1) magnitude of the perturbation from the unit circle,
#     '''
#     points_num = edge_num*3 + 1
#     angles = np.linspace(0, 2*np.pi, points_num)
#     codes = np.full(points_num, Path.CURVE4)
#     codes[0] = Path.MOVETO
#     # Using this instad of Path.CLOSEPOLY avoids an innecessary straight line
#     verts = np.stack((np.cos(angles), np.sin(angles))).T * \
#         (2*ratio*np.random.random(points_num)+1-ratio)[:, None]
#     verts[-1, :] = verts[0, :]
#     path = Path(verts, codes)
#     # draw paths into images
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#     patch = patches.PathPatch(path, facecolor='black', lw=2)
#     ax.add_patch(patch)
#     ax.set_xlim(np.min(verts)*1.1, np.max(verts)*1.1)
#     ax.set_ylim(np.min(verts)*1.1, np.max(verts)*1.1)
#     ax.axis('off')  # removes the axis to leave only the shape
#     fig.canvas.draw()
#     # convert plt images into numpy images
#     data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
#     data = data.reshape((fig.canvas.get_width_height()[::-1] + (3,)))
#     plt.close(fig)
#     # postprocess
#     data = cv2.resize(data, (width, height))[:, :, 0]
#     data = (1 - np.array(data > 0).astype(np.uint8))*255
#     corrdinates = np.where(data > 0)
#     xmin, xmax, ymin, ymax = np.min(corrdinates[0]), np.max(
#         corrdinates[0]), np.min(corrdinates[1]), np.max(corrdinates[1])
#     region = Image.fromarray(data).crop((ymin, xmin, ymax, xmax))
#     return region


def random_accelerate(velocity, maxAcceleration, dist='uniform'):
    speed, angle = velocity
    d_speed, d_angle = maxAcceleration
    if dist == 'uniform':
        speed += np.random.uniform(-d_speed, d_speed)
        angle += np.random.uniform(-d_angle, d_angle)
    elif dist == 'guassian':
        speed += np.random.normal(0, d_speed / 2)
        angle += np.random.normal(0, d_angle / 2)
    else:
        raise NotImplementedError(
            f'Distribution type {dist} is not supported.')
    return (speed, angle)


def get_random_velocity(max_speed=3, dist='uniform'):
    if dist == 'uniform':
        speed = np.random.uniform(max_speed)
    elif dist == 'guassian':
        speed = np.abs(np.random.normal(0, max_speed / 2))
    else:
        raise NotImplementedError(
            f'Distribution type {dist} is not supported.')
    angle = np.random.uniform(0, 2 * np.pi)
    return (speed, angle)


def random_move_control_points(X, Y, imageHeight, imageWidth, lineVelocity, region_size, maxLineAcceleration=(3, 0.5), maxInitSpeed=3):
    region_width, region_height = region_size
    speed, angle = lineVelocity
    X += int(speed * np.cos(angle))
    Y += int(speed * np.sin(angle))
    lineVelocity = random_accelerate(
        lineVelocity, maxLineAcceleration, dist='guassian')
    if ((X > imageHeight - region_height) or (X < 0) or (Y > imageWidth - region_width) or (Y < 0)):
        lineVelocity = get_random_velocity(maxInitSpeed, dist='guassian')
    new_X = np.clip(X, 0, imageHeight - region_height)
    new_Y = np.clip(Y, 0, imageWidth - region_width)
    return new_X, new_Y, lineVelocity



# ##############################################
# ##############################################

if __name__ == '__main__':

    trials = 10
    # for _ in range(trials):
    #     video_length = 10
    #     # The returned masks are either stationary (50%) or moving (50%)
    #     masks = create_random_shape_with_random_motion(
    #         video_length, imageHeight=240, imageWidth=432)
    #
    #     for m in masks:
    #         cv2.imshow('mask', np.array(m))
    #         cv2.waitKey(500)


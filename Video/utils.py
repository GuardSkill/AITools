#coding: utf-8
import os
import time
import cv2

def get_file_list(root_path, postfix=None):
    '''
    获取root_path目录下的所有后缀名为postfix的文件
    '''
    file_list = []
    for root, dirs, files in os.walk(root_path):
        for file in files:
            filename = os.path.join(root, file)
            file_list.append(filename)

    if postfix:
        file_list = list(filter(lambda filename: filename.endswith(postfix), file_list))

    return file_list


def files_filter(files, postfixs):
    filtered_files = []
    for file in files:
        postfix = file.split('.')[-1]
        if postfix.lower() in postfixs:
            filtered_files.append(file)

    return filtered_files


def get_str_date():
    '''
    获取日期
    '''
    localtime = time.localtime(time.time())

    return time.strftime("%Y%m%d", localtime)


def video_to_images(video_file, image_save_path=None, prefix_name=None, interval=1, start_frame=0):
    '''
    视频文件转图像文件
    :param video_path:
    :param image_name:
    :param interval:
    :return:
    '''
    if image_save_path is None:
        postfix = '.'+video_file.split('.')[1]
        image_save_path = video_file.replace(postfix, '_images')
    if not os.path.exists(image_save_path):
        os.makedirs(image_save_path)

    if prefix_name is None:
        video_name = os.path.basename(video_file).split('.')[0]
        dirname = os.path.basename(os.path.dirname(video_file))
        # prefix_name = get_strdata() + '_' + video_name
        prefix_name = dirname + '_' + video_name
        prefix_name= video_name


    cap = cv2.VideoCapture(video_file)
    frame_num = 0
    save_count = 0
    while (True and cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            frame_num += 1
            if frame_num < start_frame:
                continue
            if frame_num % interval == 0:
                save_name = os.path.join(image_save_path, "{}_{:0>6d}.png".format(prefix_name, frame_num))
                # print(save_name)
                cv2.imwrite(save_name, frame)
                save_count += 1
        else:
            break
    cap.release()
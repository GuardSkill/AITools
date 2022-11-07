#coding: utf-8
import os
import time
import cv2
import ffmpeg

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


def video_to_images_uniform_cv2(video_file, image_save_path=None, prefix_name=None, interval=1, start_frame=0):
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


def video_to_images_middle_sample_ffmpeg(video_file, image_save_path=None, prefix_name=None,max_save_count_per_video=9):
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

    probe = ffmpeg.probe(video_file)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)

    probe = ffmpeg.probe(video_file)
    time = float(probe["format"]["duration"]) // 2
    width = probe['streams'][0]['width']

    # Set how many spots you want to extract a video from. 
    parts = max_save_count_per_video

    intervals = time // parts
    intervals = int(intervals)
    interval_list = [(i * intervals, (i + 1) * intervals) for i in range(parts)]
    i = 0

    for item in interval_list:
        save_name =os.path.join(image_save_path, "{}_{:0>6d}_{}.png".format(prefix_name,item[1],i))
        (
            ffmpeg
            .input(video_file, ss=item[1])
            .filter('scale', width, -1)
            .output(save_name, vframes=1)
            .run()
        )
        i += 1
def classify_extract_video_ffmpeg(video_file, image_save_path=None, prefix_name=None,second_interval=30):
    '''
    视频文件按元数据分类，再转图像文件
    :param video_path:
    :param image_name:
    :param interval:
    :return:
    '''
    if image_save_path is None:
        postfix = '.'+video_file.split('.')[1]
        image_save_path = video_file.replace(postfix, '_images')
    cam1_image_save_path=os.path.join(image_save_path,"cam1")
    cam2_image_save_path=os.path.join(image_save_path,"cam2")
    if not os.path.exists(cam1_image_save_path):
        os.makedirs(cam1_image_save_path)
    if not os.path.exists(cam2_image_save_path):
        os.makedirs(cam2_image_save_path)
    if prefix_name is None:
        video_name = os.path.basename(video_file).split('.')[0]
        dirname = os.path.basename(os.path.dirname(video_file))
        # prefix_name = get_strdata() + '_' + video_name
        prefix_name = dirname + '_' + video_name
        prefix_name= video_name

    probe = ffmpeg.probe(video_file)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    if video_stream is None:
        print('No video stream found!')

    width = int(video_stream['width'])
    height = int(video_stream['height'])
    if width== 1280 and height==720:
        image_save_path=cam1_image_save_path
    else:
        image_save_path=cam2_image_save_path
    probe = ffmpeg.probe(video_file)
    time = float(probe["format"]["duration"]) 
    width = probe['streams'][0]['width']
    if time <=second_interval:
        second_interval=time//2+1
    # Set how many spots you want to extract a video from. 
    # parts = max_save_count_per_video

    # intervals = time // parts
    # intervals = int(intervals)
    intervals = int(second_interval)
    parts= int(time // second_interval)
    interval_list = [(i * intervals, (i + 1) * intervals) for i in range(parts)]
    i = 0

    for item in interval_list:
        save_name =os.path.join(image_save_path, "{}_{:0>6d}_{}.png".format(prefix_name,item[1],i))
        (
            ffmpeg
            .input(video_file, ss=item[1])
            .filter('scale', width, -1)
            .output(save_name, vframes=1)
            .run()
        )
        i += 1
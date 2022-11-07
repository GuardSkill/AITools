'''
Author: Siyuan Li
Date: 2022-08-08 14:33:12
LastEditors: Siyuan Li
LastEditTime: 2022-08-17 16:27:46
FilePath: \AITools\Video\test_ffmpeg.py
Description: 利用ffmpeg从视频中平均采样图像
Email: 497291093@qq.com
Copyright (c) 2022 by Siyuan Li - ZHONGCHAO XINDA, All Rights Reserved. 
'''

import ffmpeg
from utils import classify_extract_video_ffmpeg

# from utils import video_to_images_middle_sample


# video_file=r"E:/CVMS_RECORD/06_02/20211004_06_02_0013_508706.MP4"
# TEST1
video_file=r"F:/Data/ActionDet/train_data/Falldown/FallDown.mkv"
classify_extract_video_ffmpeg(video_file, image_save_path=None, prefix_name=None,second_interval=30)
# probe = ffmpeg.probe(video_file)

# # example code:
# time = float(probe["format"]["duration"]) // 2
# width = probe['streams'][0]['width']
# parts = 7
# intervals = time // parts
# intervals = int(intervals)
# interval_list = [(i * intervals, (i + 1) * intervals) for i in range(parts)]
# i = 0

# for item in interval_list:
#     (
#         ffmpeg
#         .input(video_file, ss=item[1])
#         .filter('scale', width, -1)
#         .output('Image' + str(i) + '.jpg', vframes=1)
#         .run()
#     )
#     i += 1
    

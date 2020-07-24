import os

# 训练建立目录
def create_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
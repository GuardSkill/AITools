import datetime
cur_dateTime=datetime.datetime.now().strftime('%Y%m%d%H')    
input=f'python train.py --data data/sdg.yaml --cfg models/yolov5s.yaml --weights yolov5s.pt --batch-size 26 --project runs/runs_sdg --name {cur_dateTime} --device 3'
def get_args_str(input):
    '''将命令行方式的python启动改为vscode所需要args
    '''
    args=input.split(' ')[2:]
    all_str='"args": ['
    for arg in args:
        all_str+='"'+arg+'",'
    all_str+=']'
    print(all_str)
get_args_str(input)
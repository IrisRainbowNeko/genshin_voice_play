import cv2
import os
from tqdm import tqdm
import argparse

def video_proc(videoname, save_dir, skip=10):
    os.makedirs(save_dir, exist_ok=True)
    capture = cv2.VideoCapture(videoname)
    f_count=0
    base_name=os.path.basename(videoname)[:-4]
    pbar=tqdm(total=capture.get(cv2.CAP_PROP_FRAME_COUNT))
    if capture.isOpened():
        while True:
            for i in range(skip):
                ret,frame=capture.read() # img 就是一帧图片
                f_count+=1
                pbar.update(1)
                if not ret:
                    return

            frame=cv2.resize(frame, (1920, 1080))
            cv2.imwrite(os.path.join(save_dir, f'{base_name}_f{f_count}.jpg'), frame)
    else:
        print('视频打开失败！')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("video_dir")
    parser.add_argument("out_dir")
    parser.add_argument("--skip", type=int, default=10)
    args = parser.parse_args()

    video_list=os.listdir(args.video_dir)
    for file in video_list:
        print(file)
        video_proc(os.path.join(args.video_dir, file), args.out_dir, skip=args.skip)
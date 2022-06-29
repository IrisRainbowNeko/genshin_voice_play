import os

from control import *
from mmtracking.Interface import TrackerInterface
from xvlm.Interface import XVLMInterface
import utils

from tqdm import tqdm
import numpy as np
import cv2
import argparse

class VoicePlayer:
    def __init__(self, args):
        self.args=args
        self.pred_imsize = (1280, 720)

        self.model_tracker = TrackerInterface()
        self.model_vlm = XVLMInterface()

        self.controller = FollowController(self.pred_imsize)
        self.attacker = ScriptAttacker('control/script')

    def text_proc(self, text:str):
        part=text.split('攻击')
        if len(part)==1:
            return part
        cmd, enemy = part
        pidx=cmd.find('战术')
        plan = utils.trans_ch_int(cmd[pidx+2:]) if pidx!=-1 else 1
        return {'plan':plan-1, 'enemy':enemy}

    def render(self, action_list):
        capture = cv2.VideoCapture(self.args.video)
        fps = capture.get(cv2.CAP_PROP_FPS)

        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        video = cv2.VideoWriter(self.args.output, fourcc, fps, (1920,1080))

        draw_bbox=False
        bbox=None
        cmd_idx=0

        for i in tqdm(range(int(capture.get(cv2.CAP_PROP_FRAME_COUNT)))):
            ret, frame = capture.read()

            if bbox is not None:
                bbox=self.model_tracker.predict(frame)[:4]

            if cmd_idx<len(action_list) and (i*(1/fps)*1000) > action_list[cmd_idx][0]:
                if action_list[cmd_idx][1]!='track over':
                    text_dict = self.text_proc(action_list[cmd_idx][1])
                    if len(text_dict) > 1:
                        bbox = self.model_vlm.predict(frame, text_dict['enemy'])
                        self.model_tracker.reset(bbox)
                cmd_idx+=1

            if bbox is not None:
                cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (0, 255, 0), 2)

            video.write(frame)

        capture.release()
        video.release()


def make_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", type=str, default='./video/v1.mp4')
    parser.add_argument("--output", type=str, default='./video/v1_proc.mp4')
    parser.add_argument("--actions", type=str, default='log_v1.txt')
    return parser.parse_args()

if __name__ == '__main__':
    args = make_args()

    with open(args.actions, encoding='utf8') as f:
        log=f.readlines()
    log=[x.strip().split(',') for x in log if len(x.strip())>0]
    for i in range(len(log)):
        log[i][0]=int(log[i][0].strip())
        log[i][1]=log[i][1].strip()

    player = VoicePlayer(args)
    player.render(log)
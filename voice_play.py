from control import *
from window_capture import WindowCapture

from multiprocessing import Process, Queue
#import threading
import time
import win32api
import winsound
import numpy as np
import cv2
import argparse

#监听是否有语音指令
def voice_listener(speech_queue, stop_queue):
    from voice import SpeechRecognizer, StreamPatcher
    print('voice listener start')
    model_speech = SpeechRecognizer()

    with StreamPatcher() as sp:
        winsound.Beep(500, 500)
        while True:
            if stop_queue.qsize()>0:
                break
            for _ in iter(sp):
                pass

            text = model_speech.next(sp.rec_data.tobytes())
            speech_queue.put(text)

def img_saver(img_queue, stop_queue):
    while True:
        if stop_queue.qsize()>0:
            break
        if img_queue.qsize()<=0:
            time.sleep(0.05)
            continue

        data=img_queue.get()
        cv2.imwrite(f'vis/{data[0]}.jpg', data[1])

class VoicePlayer:
    def __init__(self, args):
        self.args=args
        self.pred_imsize = (1280, 720)

        self.model_tracker = TrackerInterface()
        self.model_vlm = XVLMInterface()

        self.controller = FollowController(self.pred_imsize)
        self.attacker = ScriptAttacker('')
        self.capture = WindowCapture('原神')

        self.test()

    def test(self):
        img = cv2.imread('vis/1656394043254.jpg', cv2.IMREAD_COLOR)
        bbox = self.model_vlm.predict(img, '右边的火史莱姆')
        print('test ok')

    def text_proc(self, text:str):
        cmd, enemy = text.split('攻击')
        pidx=cmd.find('战术')
        plan = cmd[pidx+2:] if pidx!=-1 else '一'
        return {'plan':plan, 'enemy':enemy}

    def start(self, vis=False):
        speech_queue=Queue(maxsize=100)
        stop_queue=Queue(maxsize=2)
        Process(target=voice_listener, args=(speech_queue, stop_queue)).start()

        if vis:
            img_queue = Queue(maxsize=100)
            Process(target=img_saver, args=(img_queue, stop_queue)).start()

        while True:
            if win32api.GetKeyState(ord('Q')) < 0:
                stop_queue.put(True)
                return

            if speech_queue.qsize()<=0:
                time.sleep(0.1)
                continue

            text = speech_queue.get()
            print(text)
            text_dict = self.text_proc(text)

            img = self.capture.cap(resize=self.pred_imsize)
            bbox = self.model_vlm.predict(img, text_dict['enemy'])

            self.model_tracker.reset(bbox)

            while speech_queue.qsize()<=0: #没有新指令就一直追踪当前指令
                if win32api.GetKeyState(ord('Q')) < 0:
                    stop_queue.put(True)
                    return

                if vis:
                    canvas = np.copy(img)
                    cv2.rectangle(canvas, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (0, 255, 0), 2)
                    t = int(time.time() * 1000)
                    img_queue.put([t, canvas])

                if self.controller.step(bbox): #追踪目标执行完毕
                    self.attacker.attack(text_dict['plan']) #按预设进行攻击
                    break

                img = self.capture.cap(resize=self.pred_imsize)
                bbox=self.model_tracker.predict(img)['track_bboxes'][:4]

def make_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vis", type=bool, default=False)
    return parser.parse_args()

if __name__ == '__main__':
    #从外面import这些wenet会报错
    from mmtracking.Interface import TrackerInterface
    #from voice import SpeechRecognizer, StreamPatcher
    from xvlm.Interface import XVLMInterface

    args = make_args()
    player = VoicePlayer(args)

    print('press t to start')
    winsound.Beep(700, 500)
    while win32api.GetKeyState(ord('T')) >= 0:
        pass
    player.start(args.vis)
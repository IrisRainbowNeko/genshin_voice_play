from mmtracking.Interface import TrackerInterface
from voice import SpeechRecognizer, StreamPatcher
from xvlm.Interface import XVLMInterface
from control import *
from window_capture import WindowCapture

import threading
import time
import win32api

class VoicePlayer:
    def __init__(self):
        self.pred_imsize = (1280, 720)

        self.model_speech = SpeechRecognizer()
        self.model_tracker = TrackerInterface()
        self.model_vlm = XVLMInterface()

        self.controller = FollowController(self.pred_imsize)
        self.attacker = ScriptAttacker('')
        self.capture = WindowCapture('原神')

        self.sp_flag=False

    #监听是否有语音指令
    def voice_listener(self, speech_queue):
        with StreamPatcher() as sp:
            while True:
                if self.sp_flag:
                    break
                for _ in iter(sp):
                    pass

                text = self.model_speech.next(sp.rec_data.tobytes())
                speech_queue.append(text)

    def text_proc(self, text:str):
        cmd, enemy = text.split('攻击')
        pidx=cmd.find('战术')
        plan = cmd[pidx+2:] if pidx!=-1 else '一'
        return {'plan':plan, 'enemy':enemy}

    def start(self):
        speech_queue=[]
        threading.Thread(target=self.voice_listener, args=(speech_queue, )).start()

        while True:
            if win32api.GetKeyState(ord('Q')) < 0:
                self.sp_flag = True
                return

            if len(speech_queue)<=0:
                time.sleep(0.1)
                continue

            text = speech_queue.pop(0)
            text_dict = self.text_proc(text)

            img = self.capture.cap(resize=self.pred_imsize)
            bbox = self.model_vlm.predict(img, text_dict['enemy'])

            self.model_tracker.reset(bbox)

            while len(speech_queue)<=0: #没有新指令就一直追踪当前指令
                if win32api.GetKeyState(ord('Q')) < 0:
                    self.sp_flag = True
                    return

                if self.controller.step(bbox): #追踪目标执行完毕
                    self.attacker.attack(text_dict['plan']) #按预设进行攻击
                    break

                img = self.capture.cap(resize=self.pred_imsize)
                bbox=self.model_tracker.predict(img)[:4]

if __name__ == '__main__':
    print('press t to start')
    while win32api.GetKeyState(ord('T')) >= 0:
        pass

    player = VoicePlayer()
    player.start()
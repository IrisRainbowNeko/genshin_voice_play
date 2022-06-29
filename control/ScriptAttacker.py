import os

from utils import *
import time
from utils import *

class ScriptAttacker:
    def __init__(self, script_dir, screen_size=(2560, 1440)):
        self.script_dir=script_dir
        self.screen_size=screen_size
        self.screen_center = (screen_size[0] // 2, screen_size[1] // 2)

        self.scripts=[self.load_script(os.path.join(script_dir, f'{i+1}.txt')) for i in range(len(os.listdir(script_dir)))]

    def load_script(self, file):
        with open(file, encoding='utf8') as f:
            data=[x.strip() for x in f.readlines()]

        data=[x.split() for x in data if not (x.startswith('#') or len(x)<=0)]
        return data

    def attack(self, plan):
        mouse_dict={'r':MOUSE_RIGHT, 'l':MOUSE_LEFT}

        for cmd in self.scripts[plan]:
            print(cmd)
            if cmd[0]=='key':
                if len(cmd)==2:
                    tap_key(ord(cmd[1].upper()), 0.1)
                else:
                    (press_key if cmd[1]=='down' else release_key)(ord(cmd[2].upper()))
            elif cmd[0]=='mouse':
                button=mouse_dict[cmd[1]]
                mouse_ctrl.down(button)
                time.sleep(float(cmd[2]))
                mouse_ctrl.up(button)
            elif cmd[0]=='delay':
                time.sleep(float(cmd[1]))
            else:
                raise ValueError("unknown cmd")
from utils import *

class ScriptAttacker:
    def __init__(self, script_dir, screen_size=(2560, 1440)):
        self.script_dir=script_dir
        self.screen_size=screen_size
        self.screen_center = (screen_size[0] // 2, screen_size[1] // 2)

    def attack(self, plan):
        mouse_ctrl.click(*self.screen_center)
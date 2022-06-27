from utils import *

class FollowController:
    def __init__(self, imsize, th_center=0.1, th_close=0.7, base_move_speed=50, screen_size=(2560, 1440)):
        self.imsize=imsize
        self.th_center=th_center
        self.th_close=th_close
        self.screen_size=screen_size
        self.screen_center=(screen_size[0]//2, screen_size[1]//2)
        self.base_move_speed=base_move_speed

        self.go=False
        self.key_go=87

    def step(self, bbox):
        cx=(bbox[0]+bbox[2])/2
        #cy=(bbox[1]+bbox[3])/2
        h=bbox[3]-bbox[1]

        if h/self.screen_size[1] > self.th_close:
            if self.go:
                release_key(self.key_go)
            return True
        else:
            self.move_mouse(cx-self.screen_center[0])

    def move_mouse(self, dx_rate):
        if abs(dx_rate)>self.th_center:
            if self.go:
                release_key(self.key_go)
            #mouse_down(*self.screen_center)
            mvdx=int(-self.base_move_speed*dx_rate*2)
            mouse_ctrl.move(mvdx, 0)
            #mouse_up(self.screen_center[0]+mvdx, self.screen_center[1])
        else:
            press_key(self.key_go)
            self.go=True


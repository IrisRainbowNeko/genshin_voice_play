import win32api, win32con
import time

MOUSE_LEFT=0
MOUSE_MID=1
MOUSE_RIGHT=2
mouse_list_down=[win32con.MOUSEEVENTF_LEFTDOWN, win32con.MOUSEEVENTF_MIDDLEDOWN, win32con.MOUSEEVENTF_RIGHTDOWN]
mouse_list_up=[win32con.MOUSEEVENTF_LEFTUP, win32con.MOUSEEVENTF_MIDDLEUP, win32con.MOUSEEVENTF_RIGHTUP]

def mouse_down(x, y, button=MOUSE_LEFT):
    time.sleep(0.02)
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(mouse_list_down[button], x, y, 0, 0)

def mouse_move(dx, dy):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, dx, dy, 0, 0)

def mouse_up(x, y, button=MOUSE_LEFT):
    time.sleep(0.02)
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(mouse_list_up[button], x, y, 0, 0)

def mouse_click(x, y, button=MOUSE_LEFT):
    mouse_down(x, y, button)
    mouse_up(x, y, button)

def release_key(key_code):
    win32api.keybd_event(key_code, win32api.MapVirtualKey(key_code, 0), win32con.KEYEVENTF_KEYUP, 0)

def press_key(key_code):
    win32api.keybd_event(key_code, win32api.MapVirtualKey(key_code, 0), 0, 0)

def tap_key(key_code, t):
    press_key(key_code)
    time.sleep(t)
    release_key(key_code)

class MouseController:
    def __init__(self, sx, sy):
        self.px=sx
        self.py=sy

    def move(self, dx, dy):
        mouse_move(dx, dy)
        self.px+=dx
        self.py+=dy

    def down(self, button=MOUSE_LEFT):
        mouse_down(self.px, self.py, button)

    def up(self, button=MOUSE_LEFT):
        mouse_up(self.px, self.py, button)

    def click(self):
        self.down()
        self.up()

mouse_ctrl = MouseController(2560//2, 1440//2)
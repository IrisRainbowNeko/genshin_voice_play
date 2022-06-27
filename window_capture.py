import win32api, win32con, win32gui, win32ui
import numpy as np
import cv2

class WindowCapture:
    def __init__(self, name, width=2560, height=1440):
        self.WINDOW_NAME = name
        self.DEFAULT_MONITOR_WIDTH = width
        self.DEFAULT_MONITOR_HEIGHT = height

        self.hwnd = win32gui.FindWindow(None, self.WINDOW_NAME)
        self.genshin_window_rect = win32gui.GetWindowRect(self.hwnd)

    def cap(self, area=None, resize=None):
        if area is None:
            area=[0,0,self.DEFAULT_MONITOR_WIDTH, self.DEFAULT_MONITOR_HEIGHT]
        w, h = area[2:]

        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()

        dataBitMap.CreateCompatibleBitmap(dcObj, w, h)

        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (w, h), dcObj, (area[0], area[1]), win32con.SRCCOPY)
        # dataBitMap.SaveBitmapFile(cDC, bmpfilenamename)
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype="uint8")
        img.shape = (h, w, 4)
        img=cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        if resize is not None:
            img=cv2.resize(img, resize)

        return img
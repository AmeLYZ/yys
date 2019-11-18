import time

import win32gui
import win32com.client

import numpy as np
from PIL import Image, ImageDraw, ImageGrab


# return the loction of YYS windows
def FindYYSWindows():
    classname = "Win32Window0"
    titlename = "阴阳师-网易游戏"
    
    hwnd = win32gui.FindWindow(classname, titlename)
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    
    # if delete the first two lines, there will be a bug with the func win32gui.SetForegroundWindow()
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    win32gui.SetForegroundWindow(hwnd)

    return (left, top, right, bottom)


def screenshot(windows_location):
    filename = 'screenshot{}.png'.format(time.time())
    
    img = ImageGrab.grab(windows_location)
    img.save("screenshot\\{}".format(filename), 'png')
    
    return filename
    
     
if __name__ == "__main__":
    loc = FindYYSWindows()   
    
    while 1:
        time.sleep(0.2)
        filename = screenshot(loc)
        print("file {} save successfully".format(filename))
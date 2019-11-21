import time
import random

import pyautogui
import win32gui
import win32con
import win32com.client

import cv2
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
    


    
    
class OnmyojiPassenger(object):
    """ init params"""
    def __init__(self):
        self.mouth_location = (0, 0)
        
        # left top right bottom
        left, top, right, bottom = FindYYSWindows()
        self.windows_location = left, top, right, bottom
        
        # def blank safe zone
        bl = np.percentile([left, right], 80)
        bt = np.percentile([top, bottom], 70)
        br = np.percentile([left, right], 90)
        bb = np.percentile([top, bottom], 78)
        self.blank_zone = bl, bt, br, bb


    def screenshot(self):
        img = ImageGrab.grab(self.windows_location)
        
        # img.save('test.png', 'png')
        # img.save('{}.png'.format(time.time()), 'png')
        
        return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)



    def find_piece(self, img, template):
        piece_template = cv2.imread(template)
        h, w = piece_template.shape[:2]
        
        meth = eval('cv2.TM_CCORR_NORMED')
        res = cv2.matchTemplate(img, piece_template, meth)
        
        # max_val shows the best score, while max_loc shows the index of it 
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        print(max_val, max_loc)
        
        
        if random.random() > 0.7:
            pyautogui.moveTo(max_loc[0]+self.windows_location[0], max_loc[1]+self.windows_location[1])
        
        if max_val >= 0.999:
            safe_zone = (max_loc[0], max_loc[1], max_loc[0]+w, max_loc[1]+h)
            
        else:
            safe_zone = (0, 0, 0, 0)
        
        """
        draw_img = img.copy()
        ret = cv2.rectangle(draw_img, (safe_zone[0], safe_zone[1]), (safe_zone[2], safe_zone[3]), (0, 0, 255), 2)
        cv2.imshow('ret', ret)
        cv2.waitKey(0)
        cv2.destroyAllWindows()   
        """  
        
        return safe_zone


    def safe_click(self, safe_zone, click_time=2):
        # random click n times in safe zone
        
        safe_click_time = random.randint(click_time, click_time+1)
        safe_click_frec = random.randint(150, 180)/1000
        
        for i in range(safe_click_time):
            safe_point = (random.randint(safe_zone[0], safe_zone[2])+self.windows_location[0], 
                          random.randint(safe_zone[1], safe_zone[3])+self.windows_location[1])
            pyautogui.moveTo(safe_point)
            pyautogui.click()
            time.sleep(safe_click_frec)


        
    def mitama(self, need_number=5):
        counter = 0
        for counter in range(1, need_number+1):
            # invite button
            safe_zone = (0, 0, 0, 0)        
            while(safe_zone == (0, 0, 0, 0)):
                time.sleep(0.1)
                img = self.screenshot()
                safe_zone = onmyoji.find_piece(img, 'image\\invite1.png')
                            
            auto_zone = onmyoji.find_piece(img, 'image\\invite2.png')
            
            # auto prepared
            if auto_zone != (0, 0, 0, 0):
                self.safe_click(auto_zone)
                    
            # not auto prepared                
            else:
                self.safe_click(safe_zone)   

                # 0: unlocked  1: not find  2: locked
                lock_state = 1

                while(lock_state == 1):
                    time.sleep(0.1)
                    img = self.screenshot()
                    
                    # find the lock state                    
                    state0 = 0 if onmyoji.find_piece(img, 'image\\locked0.png') != (0, 0, 0, 0) else 1
                    state1 = 1 if onmyoji.find_piece(img, 'image\\locked1.png') != (0, 0, 0, 0) else 0                   
                    lock_state = state0 + state1
                    # print('state0 & state1: {} & {}'.format(state0, state1))
                    print('lock state:{}'.format(lock_state))

                # unlocked, need to press the prepare-button
                if lock_state == 0:
                    safe_zone = (0, 0, 0, 0)
                    
                    while(safe_zone == (0, 0, 0, 0)):
                        time.sleep(0.1)
                        img = self.screenshot()
                        safe_zone = onmyoji.find_piece(img, 'image\\prepare.png')    
                    
                    # self.safe_click(safe_zone)
                    
                # locked, no need to press the prepare -button
                else:
                    pass


            # finish one task
            safe_zone = (0, 0, 0, 0)
            while(safe_zone == (0, 0, 0, 0)):
                time.sleep(0.1)
                img = self.screenshot()
                safe_zone = onmyoji.find_piece(img, 'image\\finish1.png')
            
            self.safe_click(safe_zone)   
          
            safe_zone = (0, 0, 0, 0)
            while(safe_zone == (0, 0, 0, 0)):
                time.sleep(0.1)
                img = self.screenshot()
                safe_zone = onmyoji.find_piece(img, 'image\\finish2.png')

            # delay needed
            
            self.safe_click(safe_zone)
            time.sleep(2)
            # task counter            
            print("完成{}次任务, 还差{}次任务".format(counter, need_number-counter))
            


if __name__ == "__main__":
    onmyoji  = OnmyojiPassenger()
    loc = onmyoji.windows_location
    print('onmyoji window: ', loc)
    
    
    # img = onmyoji.screenshot()
    # img = cv2.imread("test.png")
    # safe_zone = onmyoji.find_piece(img, 'image\\finish2.png')
    # pyautogui.moveTo(safe_zone[0], safe_zone[1])
    onmyoji.mitama()
    

    
    
    
    
    
    
    
    

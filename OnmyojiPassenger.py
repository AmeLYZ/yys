
import time
import random

import pyautogui
import win32gui
import win32con

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageGrab

# def safe zone





# return the loction of YYS windows
def FindYYSWindows():
    classname = "Win32Window0"
    titlename = "阴阳师-网易游戏"
    
    hwnd = win32gui.FindWindow(classname, titlename)
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    
    # set the windows foreground
    # win32gui.SetForegroundWindow(hwnd)

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
        img.save('test.png', 'png')
        # img.save('{}.png'.format(time.time()), 'png')
        return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        # return cv2.imread("test.png")


    def find_piece(self, img, template):
        piece_template = cv2.imread(template)
        h, w = piece_template.shape[:2]
        
        meth = eval('cv2.TM_CCORR_NORMED')
        res = cv2.matchTemplate(img, piece_template, meth)
        
        # max_val shows the best score, while max_loc shows the index of it 
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        #  print(min_val, max_val, min_loc, max_loc)
        
        if max_val >= 0.99:
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
        # click time >= 2
        
        safe_click_time = random.randint(click_time-1, click_time+1)
        safe_click_frec = random.randint(120, 180)/1000
        
        for i in range(click_time):
            safe_point = (random.randint(safe_zone[0], safe_zone[2])+self.windows_location[0], 
                          random.randint(safe_zone[1], safe_zone[3])+self.windows_location[1])
            pyautogui.moveTo(safe_point)
            pyautogui.click()
            time.sleep(safe_click_frec)

        
    def mitama(self):
        timer = 1
        while 1:  
            safe_zone = (0, 0, 0, 0)        
            while(safe_zone == (0, 0, 0, 0)):
                time.sleep(0.2)
                img = self.screenshot()
                safe_zone = onmyoji.find_piece(img, 'image\\invite1.png')
                            
            auto_zone = onmyoji.find_piece(img, 'image\\invite2.png')
            
            # if: not auto prepare
            if auto_zone == (0, 0, 0, 0):
                # print('find safe zone')
                self.safe_click(safe_zone)   
                
                safe_zone = (0, 0, 0, 0)
                while(safe_zone == (0, 0, 0, 0)):
                    time.sleep(0.2)
                    img = self.screenshot()
                    safe_zone = onmyoji.find_piece(img, 'image\\finish1.png')  
            # else: auto prepare                    
            else:
                self.safe_click(auto_zone)
              
  
            
            safe_zone = (0, 0, 0, 0)
            while(safe_zone == (0, 0, 0, 0)):
                time.sleep(0.2)
                img = self.screenshot()
                safe_zone = onmyoji.find_piece(img, 'image\\finish1.png')
            
            # print('find safe zone')
            self.safe_click(safe_zone)   
          
            safe_zone = (0, 0, 0, 0)
            while(safe_zone == (0, 0, 0, 0)):
                time.sleep(0.2)
                img = self.screenshot()
                safe_zone = onmyoji.find_piece(img, 'image\\finish2.png')
            
            # print('find safe zone')
            self.safe_click(safe_zone)  
            print("完成{}次任务".format(timer))
            timer += 1


if __name__ == "__main__":
    onmyoji  = OnmyojiPassenger()
    loc = onmyoji.windows_location
    print('onmyoji window: ', loc)
    
    
    # img = onmyoji.screenshot()
    # img = cv2.imread("test.png")
    # safe_zone = onmyoji.find_piece(img, 'image\\finish2.png')
    # pyautogui.moveTo(safe_zone[0], safe_zone[1])
    onmyoji.mitama()
    

    
    
    
    
    
    
    
    

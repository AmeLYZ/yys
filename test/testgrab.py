import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageGrab


img = ImageGrab.grab()
img.save('testgrab.png', 'png')

img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)



draw_img = img.copy()

cv2.imshow('draw_img', draw_img)
cv2.waitKey(0)
cv2.destroyAllWindows()   
  
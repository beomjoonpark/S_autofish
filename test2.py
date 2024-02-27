from PIL import Image
from PIL import ImageGrab
from PIL import ImageChops
from PIL import ImageStat
import pyautogui
import time
time.sleep(1)
screen=ImageGrab.grab()
a=pyautogui.position()
b=screen.getpixel(a)
print(a,b)


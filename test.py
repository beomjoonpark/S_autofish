import pyautogui
from PIL import Image
from PIL import ImageGrab
from PIL import ImageChops
from PIL import ImageStat
from time import sleep
screen=ImageGrab.grab()
a=pyautogui.position()
b=screen.getpixel(a)
print(b)
#print(a)

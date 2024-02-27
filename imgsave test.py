import pyautogui as pag
import time
from PIL import Image
from PIL import ImageGrab
from PIL import ImageChops
from PIL import ImageStat
import cv2
import numpy as np
from random import randint
from playsound import playsound

img=ImageGrab.grab()
img.save('./data/img.png')

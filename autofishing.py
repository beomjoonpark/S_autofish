import pyautogui as pag
import time
from PIL import Image
from PIL import ImageGrab
from PIL import ImageChops
from PIL import ImageStat
import cv2
import sys
import numpy as np
from random import randint
from playsound import playsound


centinal_emot = { #centinal D's emot 
    'x' : 181,
    'y' : 478
}
detector = { #fish pole blue gauge detection
    'x' : 866+25,
    'y' : 143
}
exclm_mark = { #when fish is caught
    'xleft' : 169,
    'xright' : 175,
    'yleft' : 337,
    'yright' : 348
}
crank_button = {
    'tl' : {   # tl stands for top left
        'x' : 1119, 
        'y' : 566
    },
    'center' : { #middle
        'x' : 1169,
        'y' : 613
    },
    'br' : { #br = bottom right
        'x' : 1219,
        'y' : 660
    }
}


main_button=pag.locateCenterOnScreen('main button.png')
if main_button is None:
    time.sleep(3)
    main_button=pag.locateCenterOnScreen('main button.png')

#print(main_button)
mblst=list(main_button)

difx = int(mblst[0]) - crank_button['center']['x']
dify = int(mblst[1]) - crank_button['center']['y']


gbx= detector['x'] + difx+55
gby= detector['y'] + dify


def randClc(x1, x2, xrad, yrad) : 
    xf = x1 + randint(-xrad, xrad)
    yf = x2 + randint(-yrad, yrad)
    pag.click(xf, yf)

def PixelCheck(x1,y1,x2,y2):
    im1=ImageGrab.grab((x1,y1,x2,y2))
    while 1:
       # time.sleep(0.03)
        im2=ImageGrab.grab((x1,y1,x2,y2))
        im=ImageChops.difference(im1,im2)
        stat=ImageStat.Stat(im)

        if stat.sum !=[0,0,0]:
            randClc(mblst[0], mblst[1], 15, 15)
            break
        else:
            pass


def pullPole() :
    im1=ImageGrab.grab((crank_button['tl']['x']+difx, crank_button['tl']['y']+dify, crank_button['br']['x']+difx, crank_button['br']['y']+dify))
    time.sleep(0.1)
    im2=ImageGrab.grab((crank_button['tl']['x']+difx, crank_button['tl']['y']+dify, crank_button['br']['x']+difx, crank_button['br']['y']+dify))
    im=ImageChops.difference(im1,im2)
    stat=ImageStat.Stat(im)
    if (stat.sum == [0,0,0]) :
        playsound('alarm.wav')
        

def pull():
    #줄을 계속 당겨주는 함수
    time.sleep(0.7)
    pag.mouseDown(main_button)
    time.sleep(2)
    pag.mouseUp(main_button)
    screen=ImageGrab.grab()
    
    gaugecolor=list(screen.getpixel((gbx,gby)))
    cnt=0
    xf = mblst[0] + randint(-15, 15)
    yf = mblst[1] + randint(-15, 15)
    while True:
        if gaugecolor == [51,119,84] : 
            #print('need to pull')
            pag.mouseUp()
            pag.mouseDown(xf, yf)
            time.sleep(0.1)
        elif gaugecolor == [255,255,255] or gaugecolor[0]>130 : 
            print('Fish caught')
            break
        elif gaugecolor == [104,241, 170] : 
            pag.mouseUp(xf, yf)
            #pullPole()
        else : 
            print('release by pixel mismatch')
            if cnt==0:
                pag.mouseUp(xf, yf)
            cnt = cnt+1
            #pullPole()
            if cnt>5 : 
                break
        screen = ImageGrab.grab()
        gaugecolor = list(screen.getpixel((gbx, gby)))

        
def bar_in():
    #버튼을 누르고, 파란색 바를 찾아서 찌를 던지는 함수
    randClc(mblst[0], mblst[1], 15, 15)
    
    bar=pag.locateCenterOnScreen('bar.png')
    while bar is None:
        bar=pag.locateCenterOnScreen('bar.png')
    
    bar_lst=list(bar)
    x1=bar_lst[0]-20
    y1=bar_lst[1]-2
    x2=bar_lst[0]+20
    y2=bar_lst[1]+2
    PixelCheck(x1,y1,x2,y2)
    
small=True

def timing():
    global small
    x1=exclm_mark['xleft'] + difx
    x2=exclm_mark['xright'] + difx
    y1=exclm_mark['yleft'] + dify
    y2=exclm_mark['yright'] + dify
    im1=ImageGrab.grab((x1,y1,x2,y2))
    while 1:
       # time.sleep(0.03)
        im2=ImageGrab.grab((x1,y1,x2,y2))
        im=ImageChops.difference(im1,im2)
        stat=ImageStat.Stat(im)

        if stat.sum !=[0,0,0]:
            img = ImageGrab.grab()
            color = list(img.getpixel((centinal_emot['x'] + difx, centinal_emot['y']+dify)))
            print(color)
            if color != [51, 136, 221] :
                print("Big Hit")
                randClc(mblst[0], mblst[1], 15, 15)
                playsound('alarm.wav')
                time.sleep(1)
                small=False
                break
            else:
                print("Normal Hit")
                randClc(mblst[0], mblst[1], 15, 15)
                time.sleep(1)
                small=True
                break
        else:
            pass
class label(Exception) : pass
while True:
    try:
        bar_in()
        time.sleep(4)
        timing()

        pull()
        time.sleep(3)
        con=pag.locateCenterOnScreen('cont.png')
        while con is None :
            print('continue missing error')
            con=pag.locateCenterOnScreen('cont.png')
        pag.click(con)
        pag.click(con)
        time.sleep(1)
   # except label:
   #     print("except")
    except :
        print("break")
        time.sleep(5)




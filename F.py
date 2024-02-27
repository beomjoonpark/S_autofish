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
from pynput.mouse import Listener

#coord dict
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
wood = { #the wood at the bottom right, patternquiz
    'x': 1249,
    'y': 610
}
swipe_zone = { #the white arrow
    'x' : 1003,
    'y' : 613
}
quiz = { #quiz
    'x1' : 131,
    'x2' : 1169,
    'y' : 265
}
block1 = { 
    'x' : 245,
    'y' : 626
}
red = { 
    'r' : 102,
    'g' : 0,
    'b' : 0
}
green = { 
    'r' : 170,
    'g' : 85,
    'b' : 17
}
blue = { 
    'r' : 34,
    'g' : 68,
    'b' : 170
}


fishcnt = 0
c_gate='open'
main_button=pag.locateCenterOnScreen('main button.png')
if main_button is None:
    time.sleep(3)
    main_button=pag.locateCenterOnScreen('main button.png')
#main_button=(1666, 791)
print(main_button)
mblst=list(main_button)

difx = int(mblst[0]) - crank_button['center']['x']
dify = int(mblst[1]) - crank_button['center']['y']

arrx = swipe_zone['x'] + difx
arry = swipe_zone['y'] + dify

gbx= detector['x'] + difx
gby= detector['y'] + dify

qzx1 = quiz['x1'] + difx
qzx2 = quiz['x2'] + difx
qzy = quiz['y'] + dify

blx = block1['x'] + difx
bly = block1['y'] + dify

woodx = wood['x'] + difx
woody = wood['y'] + dify

def on_click(x, y, button, pressed):
    global answer_lst, listener
    print('waiting for input')
    answer_lst.append("5%s5%s" % (x-difx, y-dify))
    if len(answer_lst)==6:
        listener.stop()
        
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
        
def cEB (block) :
    if block == [238, 102, 68] :
       return "R"
    elif block == [255, 204, 119] :
        return "G"
    elif block == [102, 119, 204] :
        return "B"
    else :
        print("color recog error")

def clickBlock(num) :
    xprime = blx + (num-1) * 128 
    pag.click(xprime, bly)
    time.sleep(0.2)

def checkBlock() :
    answer_lst=[]
    def on_click(x, y, button, pressed):
        print('waiting for input')
        answer_lst.append("%5s%5s" % (x-difx, y-dify))
        if len(answer_lst)==6:
            listener.stop()

    pag.mouseUp(main_button)
    time.sleep(1)
    img = ImageGrab.grab()
    colorArray=[]
    x=qzx1
    
    while x<qzx2:
        rgb=list(img.getpixel((x,605+dify)))
        a=max(rgb)
        if a>170:
            b=rgb.index(a)
            if b==0:
                colorArray.append('R')
            elif b==1:
                colorArray.append('G')
            elif b==2:
                colorArray.append('B')
            else:
                colorArray.append('None')
            x=x+110
        else:
            x=x+1

    colorArray.append(checkquiz(img))
    print(colorArray)
    tf=False
    f=open("./data/pattern.txt", "r")
    for line in f:
        
        if str(colorArray) in line:
            answer1=(int(line[80:84].strip())+difx, int(line[85:89].strip())+dify)
            answer2=(int(line[108:112].strip())+difx, int(line[113:117].strip())+dify)
            answer3=(int(line[136:140].strip())+difx, int(line[141:145].strip())+dify)
            tf=True
            pag.click(answer1)
            time.sleep(0.2)
            pag.click(answer2)
            time.sleep(0.2)
            pag.click(answer3)
            break
    f.close()
    
    if tf==False:
        playsound('alarm.wav')
        print("waiting for input")
        with Listener(on_click=on_click) as listener:
            listener.join()
        f=open("./data/pattern.txt", "a")
        f.write(str(colorArray) + " : " + str(answer_lst) + "\n")
        img.save("./data/"+str(colorArray) + ".png")
        f.close()
    img.save("./desk scr/"+str(colorArray) + " (" + str(mblst[0]) + ", " + str(mblst[1]) + ").png")

def checkquiz(screen):
    quizlist=[]
    x=qzx1
    cnt=0
    chain=1
    while x<qzx2:
        rgb=list(screen.getpixel((x,qzy)))
        a=max(rgb)

        if a>140:
            if cnt<5:
                chain=chain+1
                cnt=0
            else:
                chain=1
                cnt=0

            b=rgb.index(a)
            if chain!=1:
                del quizlist[-1]
            if b==0:
                quizlist.append('R'+str(chain))
            elif b==1:
                quizlist.append('G'+str(chain))
            elif b==2:
                quizlist.append('B'+str(chain))
            else:
                quizlist.append('None')
            x=x+130
        else:
            x=x+1
        cnt=cnt+1
    return quizlist



def swipe(color):
    global c_gate
    if color[0] > 200:
        pag.mouseUp()
        pag.mouseDown(mblst[0], mblst[1])
        time.sleep(0.02)
        pag.move(-150, 0, 0.3, pag.easeInQuad)
        print('swipe')
        c_gate='close'
        pag.mouseUp()
        time.sleep(0.7)

    else:
        pass


def ifBlock() :
    img = ImageGrab.grab()
    screencolor = list(img.getpixel((qzx,qzy)))
    print(screencolor)
    if screencolor == [0, 77, 112] :
        pag.mouseDown(mblst[0], mblst[1])
        pag.dragTo(mblst[0]-150, mblst[1], duration=0.3)
        print("Pulling fish pole")
    else :
        print("checkBlock")
        checkBlock()



def checkif() :
    ans_1 = pag.locateCenterOnScreen('ans_1.png')
    ans_2 = pag.locateCenterOnScreen('ans_2.png')
    ans_3 = pag.locateCenterOnScreen('ans_3.png')
    ans_4 = pag.locateCenterOnScreen('ans_4.png')
    if ans_1 is not None :
        return 1
    elif ans_2 is not None :
        return 2
    elif ans_3 is not None :
        return 3
    elif ans_4 is not None :
        return 4
    else :
        return 0



def pull():
    #줄을 계속 당겨주는 함수
    global c_gate
    c_gate='open'
    time.sleep(0.7)

    xi = mblst[0] + randint(-10, 10)
    yi = mblst[1] + randint(-50, -30)
    pag.mouseDown((xi,yi))
    time.sleep(2)
    pag.mouseUp()
    screen=ImageGrab.grab()
    
    gaugecolor=list(screen.getpixel((gbx,gby)))
    c = list(screen.getpixel((arrx,arry)))
    
    cnt=0

    gate='open'
    while True:
        xf = mblst[0] + randint(-10, 10)
        yf = mblst[1] + randint(-50, -30)

        
        if gaugecolor==[49, 121, 82]:      # need to pull
            if gate=='close':
                time.sleep(0.7)         # recoil cooldown of block quiz

            pag.mouseDown(xf, yf)

            if c_gate=='open':
                swipe(c)
                
            gate='open'                 # access to block quiz activated
            c_gate='open'               # access to swipe activated
            cnt=0                       # cnt reset
            
        elif gaugecolor == [255,255,255] or gaugecolor[0]>130 :  #fish caught
            if gate == 'open':
                print('Fish caught')
                break
            else: pass
        elif gaugecolor==[107, 243, 173] : # need to let go
            if gate=='close':
                time.sleep(0.7)         # recoil cooldown of block quiz
                
            pag.mouseUp(xf, yf)
            
            if c_gate=='open':
                swipe(c)
                
            gate='open'                 # access to block quiz activated
            c_gate='open'               # access to swipe activated
            cnt=0                       # cnt reset
            
        else :                      # pixel mismatch: 'block quiz' or 'fish caught'
            print('else')
            screen=ImageGrab.grab()
            rgbwood = list(screen.getpixel((woodx, woody)))
            print(rgbwood)
            if gate =='open' and (rgbwood[0]>70 and rgbwood[2]==41): # checking block quiz
                pag.mouseUp(xf, yf)
                print('check block')
                checkBlock()
                gate='close'
                
            else:
                print('release by pixel mismatch')  # pixel mismatch
                if cnt < 2:
                    pag.mouseUp(xf, yf)
                else:
                    playsound('alarm.wav')
                cnt = cnt+1
                
                if cnt>30 :

                    break
                
        screen=ImageGrab.grab()
        gaugecolor = list(screen.getpixel((gbx, gby)))  # checking tension
        if c_gate=='open':
            c = list(screen.getpixel((arrx,arry)))      # checking swipe
        
def bar_in():
    #버튼을 누르고, 파란색 바를 찾아서 찌를 던지는 함수
    randClc(mblst[0], mblst[1], 15, 15)

    bar=pag.locateCenterOnScreen('bar.png')
    while bar is None:
        macro_check=pag.locateCenterOnScreen('macrocheck.png')
        if macro_check is None:
            bar=pag.locateCenterOnScreen('bar.png')
        else:
            playsound('alarm.wav')
    
    bar_lst=list(bar)
    x1=bar_lst[0]-20
    y1=bar_lst[1]-2
    x2=bar_lst[0]+20
    y2=bar_lst[1]+2
    PixelCheck(x1,y1,x2,y2)

small = True

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
                #playsound('alarm.wav')
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

def execute() :
    bar_in()
    time.sleep(4)
    timing()
    pull()
    time.sleep(3)
    
    rank_up=pag.locateCenterOnScreen('rank_up.png')

    if rank_up is None:
        pass
    else:
        rl=list(rank_up)
        ra=rl[0]
        rb=rl[1]
        randClc(ra,rb,5,5)
        
    con=pag.locateCenterOnScreen('cont.png')
    while con is None :
        print('continue missing error')
        con=pag.locateCenterOnScreen('cont.png')
    conl= list(con)
    a=conl[0]
    b=conl[1]
    randClc(a,b,5,5)
    randClc(a,b,5,5)
    time.sleep(1.5)


try:
    while True :
        execute()
except KeyboardInterrupt:
    pass

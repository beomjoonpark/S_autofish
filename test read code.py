from PIL import Image
from PIL import ImageGrab
from PIL import ImageChops
from PIL import ImageStat
import pyautogui
import time
#y=534, x= 530~1700
time.sleep(5)
x=530
screen=ImageGrab.grab()
code = []
cnt=0
chain=1
while x<1700:
    rgb=list(screen.getpixel((x,534)))
    a=max(rgb)
    if a>170:
        print(cnt, chain)
        if cnt<35:
            chain=chain+1
            cnt=0
        else:
            chain=1
            cnt=0
            
        print(x)
        if rgb.index(a)==0:
            code.append('R'+str(chain))
        elif rgb.index(a)==1:
            code.append('G'+str(chain))
        elif rgb.index(a)==2:
            code.append('B'+str(chain))
        else:
            code.append('None')
        x=x+110
    else:
        x=x+1
    cnt=cnt+1

print(code)

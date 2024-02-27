from pynput.mouse import Listener


lst=[]
def on_click(x, y, button, pressed):
    print("clicked"+str(x)+','+str(y))
    lst.append((x,y))
    if len(lst)==6:
        listener.stop()

with Listener(on_click=on_click) as listener:
    listener.join()
    
print(lst)


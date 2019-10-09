import requests
import socket
import time
import threading
import io
import cv2
from PIL import Image

def imageproc(arr):
    frame = Image.open(arr) 

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    frame = cv2.resize(frame, (1600, 1200))

    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    boxes, weights = hog.detectMultiScale(frame, winStride=(8,8)
    #boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
    return boxes

class client:
    addr=None
    controller=False
    sock=None
    active=True
    def __init__(self,sock,addr,wd=False):
        self.sock=sock
        self.addr=addr
        if not sock:
            active=False
    def send(self,b):
        try:
            self.sock.send(b)
        except:
            self.active=False
            lprint("Address "+self.addr+" disconnected")
    def recv(self,size):
        try:
            resp=self.sock.recv(size)
        except:
            self.active=False
            lprint("Address "+self.addr+" disconnected")
def lprint(text,date=False):
    #Logger
    t=time.localtime()
    if date:
        print(time.strftime("---%D---", t))
        return
    print(time.strftime("[%H:%M:%S]: ", t)+text)
def watchdog(ip,port,Watchdog):
    #n-reverse
    #m-forward
    url="http://"+str(ip)+":"+str(port)+"/stream"
    r = requests.get(url, stream=True)
    a=0
    data=[]
    size=1024
    byte=bytearray()
    for chunk in r.iter_content(chunk_size=size):
        if chunk==b'-end-':
            if not Watchdog.active:
                return
            #Watchdog.send(b'n')
            byte=bytearray()
        else:
            byte.extend(chunk)
def server(ip,port,Watchdog,Controller):
    s = socket.socket()
    s.bind((ip, port))
    s.listen(2)
    lprint("",True)
    while True:
        sock, addr = s.accept()
        lprint("Connection from: "+str(addr))
        resp=sock.recv(1024)
        if resp==b'W':
            Watchdog.sock=sock
            Watchdog.addr=addr
            Watchdog.active=True
            lprint("Connection is a Watchdog")
            args=(addr[0],81,Watchdog,)
            t=threading.Thread(target=watchdog,args=args)
            t.start()
            continue
        elif resp==b'C':
            Controller.sock=sock
            Controller.addr=addr
            Controller.active=True
            while True:
                if not Controller.active:
                    break
                cmd=Controller.recv(1024)
                if cmd=="forward1":
                    Watchdog.send(b'm')
                elif cmd=="reverse1":
                    Watchdog.send(b'n')
        sock.close()
Watchdog=client(None,None)
Controller=client(None,None,True)
server("192.168.1.2",32,Watchdog,Controller)
print("Connected")


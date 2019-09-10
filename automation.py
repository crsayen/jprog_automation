import pyautogui, time, subprocess
from pyautogui import keyDown, keyUp, press
import socket, threading
from threading import Thread
from socket import (
    AF_INET,
    socket,
    SOCK_STREAM,
    SOCK_DGRAM,
    SOL_SOCKET,
    SO_BROADCAST,
    IPPROTO_UDP,
    SO_REUSEADDR,
)
import os
from os import path

pyautogui.FAILSAFE = True
here = path.abspath(path.dirname(__file__))
rcvd = ""

def click(image, timeout=None, double=False, alt=False):
    print("click({}, timeout={}, double={}, alt={})".format(image,timeout,double,alt))
    l = None
    start = time.time()
    while l is None:
        l = pyautogui.locateOnScreen(here + "\\images\\" + image + ".PNG")
        elapsed = time.time() - start
        if alt and l is None:
            l = pyautogui.locateOnScreen(here + "\\images\\" + image + "_alt.PNG")
        if timeout is not None and elapsed >= timeout:
            print("click: timeout: elapsed: {}".format(elapsed))
            break
    ret = l is not None
    if ret:
        for i in range(double + 1):
            pyautogui.click(l[0] + 5, l[1] + 10)
    return ret

def rx(sock):
    global rcvd
    while 1:
        data, address = sock.recvfrom(4096)
        rcvd = data.decode("utf-8")
        time.sleep(0.2)


def restart(kill=True):
    print("restarting")
    if rcvd == "pause":
            return
    if kill:
        os.system("taskkill /f /im  JProg_7361.exe")
        if rcvd == "pause":
            return
    subprocess.Popen(["C:/Users/model/Desktop/7361-NJ-Nissan_Kiks/JProg_7361.exe"])
    for t in [("interface", 10, False, True),("cleartoship", 10, False, False)]:
        print("trying to click {}".format(t[0]))
        if rcvd == "pause":
            print("pause")
            return
        click(t[0], timeout=t[1], double=t[2], alt=t[3])
    
def checkok(sock):
    sock.sendto(bytes("proceed", "utf-8"), address)
    for i in range(50):
        if rcvd in ["ok", "pause", "resume"]: 
            break
        time.sleep(0.1)
    if rcvd in ["pause", "resume"]:
        return False
    rcvd = ""
    return True

def main(sock):
    global rcvd
    restart(kill=False)
    while 1:
        if rcvd == "pause":
            print("paused")
            while rcvd == "pause":
                time.sleep(0.1)
        for i, step in enumerate([
            ("start",10, False),
            ("no",10, False),
            ("proceed",10, False),
            ("c_ok",20, True),
            ("proceed",10, False),
            ("e_ok",20, False)
        ]):
            if rcvd == "pause":
                break
            print(step[0])
            if i == 2:
                if not checkok(sock): break
            result = click(step[0], timeout=step[1], alt=step[2])
            print("click: {}: result: {}".format(step[0], result))
            if not result:
                restart()
                break

if __name__ == "__main__":
    address = ("192.168.7.2", 11000)
    sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    sock.bind(("", 11000))
    rxt = Thread(target=rx,args=([sock]))
    rxt.start()
    main(sock)

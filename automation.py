import pyautogui, time
from pyautogui import keyDown, keyUp, press
import os, path

pyautogui.FAILSAFE = True
here = path.abspath(path.dirname(__file__))

def click(image, timeout=None, double=False):
    l = None
    start = time.time()
    while l is None:
        l = pyautogui.locateOnScreen(here + "/images/" + image)
        elapsed = time.time() - startimport pyautogui, time
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
    l = None
    start = time.time()
    while l is None:
        l = pyautogui.locateOnScreen(here + "/images/" + image + ".PNG")
        elapsed = time.time() - start
        if alt and l is None:
            l = pyautogui.locateOnScreen(here + "/images/" + image + "_alt.PNG")
        if timeout is not None and elapsed >= timeout:
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


def restart():
    os.system("taskkill /f /im  JProg_7361.exe")
    keyDown("winleft"); press("d"); keyUp("winleft")
    click("showdesk", timeout=10, double=False)
    click("folder", timeout=10, double=True)
    click("exe", timeout=10, double=True, alt=True)
    click("runanyway", timeout=10, double=False)
    click("interface", timeout=10, double=False)
    click("cleartoship", timeout=10, double=False)


def main(sock):
    global rcvd
    while 1: 
        for i, step in enumerate([("start",10),("no",10),("proceed",10),("c_ok",20),("proceed",10),("e_ok",20)]):
            if i == 2:
                sock.sendto(bytes("proceed", "utf-8"), address)
                for i in range(50):
                    if rcvd == "ok": 
                        break
                    time.sleep(0.1)
                rcvd = "" if rcvd == "ok" else "restart"
            if rcvd == "restart" or not click(step[0], timeout=step[1]):
                restart()
                break

if __name__ == "__main__":
    address = ("192.168.7.2", 11005)
    sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    sock.settimeout(5)
    sock.bind(("", 11000))
    rxt = Thread(target=rx,args=([sock]))
    rxt.start()
    main(sock)



        if timeout is not None and elapsed >= timeout:
            break
    ret = l is not None
    if ret:
        for i in range(double + 1):
            pyautogui.click(l[0] + 5, l[1] + 10)
    return ret

def restart():
    os.system("taskkill /f /im  JProg_7361.exe")
    keyDown("winleft"); press("d"); keyUp("winleft")
    click("jprog_icon.PNG", timeout=10, double=True)
    click("interface.PNG", timeout=10, double=True)
    click("screw.PNG", timeout=10, double=True)
    click("arrow.PNG", timeout=10, double=True)
    click("cleartoship.PNG", timeout=10, double=True)

def main():
    while 1: 
        for step in [("start",10),("no",10),("proceed",10),("c_ok",20),("proceed",10),("e_ok",20)]:
            if not click(step[0] + ".PNG", timeout=step[1]):
                restart()

if __name__ == "__main__":
    main()



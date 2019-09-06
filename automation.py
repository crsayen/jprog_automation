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
        elapsed = time.time() - start
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



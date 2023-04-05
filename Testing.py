import re

import win32gui
from pynput.keyboard import Key

from Config import Config
from KeyBindTool.InputManager import inputManager
from KeyBindTool.ProcessManager import processManager
from KeyBindTool.Tkinter.tMain import tkParty
from KeyBindTool.keyBinder import basicBind


# This is main
pm = processManager()
im = inputManager(printKeys=False)
basicBind(im, pm, None)


def nextVid(**kwargs):
    import win32api

    pathToSet = Config().getPath('')
    print(pathToSet)
    DrivePath = pathToSet[0:3]
    print(DrivePath)
    try:
        volname, volsernum, maxfilenamlen, sysflags, filesystemtype = win32api.GetVolumeInformation(DrivePath)
        r = [volname, volsernum, maxfilenamlen, sysflags, filesystemtype]
        for t in r:
            print(t)
    except:
        print("failed")
        return


im.register(im.nextButton(), nextVid, name='Next Track')


tp = tkParty(im, pm)


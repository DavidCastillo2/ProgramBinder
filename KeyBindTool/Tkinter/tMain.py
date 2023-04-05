import tkinter as tk
from functools import partial
from tkinter import CENTER, RIGHT, LEFT
from tkinter.font import BOLD, Font

import win32gui
from pynput import keyboard

from KeyBindTool.RazerMacroSounds.RazerTkinter import RazerTk
from KeyBindTool.Tkinter.cleanText import cleanName
from KeyBindTool.Tkinter.helperFunctions import addMakeFrame, addBlackLine, nextRow
from KeyBindTool.keyBinder import keysToString


def getNewKeyFromUser():
    # Stop everything and wait for the user to press a key for new Keybind
    newButtons = []

    def getNewKeyBind(newKEY):
        nonlocal newButtons
        if newKEY not in newButtons:
            newButtons.append(newKEY)
        return newButtons

    def closeListener(newKEY):
        return False

    def for_canonical(f):
        return lambda k: f(listener2.canonical(k))

    with keyboard.Listener(
            on_press=for_canonical(getNewKeyBind),
            on_release=for_canonical(closeListener)) as listener2:
        listener2.join()
    return newButtons


class tkParty:

    def __init__(self, im, pm, ms):
        window = tk.Tk()
        self.window = window
        self.ms = ms
        self.im = im
        self.binds = {}
        self.pm = pm  # This object lets us know if we crashed/close
        self.keyBindsFrame = tk.Frame(master=self.window)  # KeyBindsFrame is our master for all things here
        self.keyBindsFrame.grid_columnconfigure(0, weight=1)
        self.keyBindsFrame.grid_columnconfigure(1, weight=1)
        self.keyBindsFrame.grid_columnconfigure(2, weight=1)
        self.keyBindsFrame.rowconfigure(2, minsize=0, weight=0)
        self.keyBindsFrame.pack()

        # Basic top text
        boldFont = Font(self.keyBindsFrame, size=12, weight=BOLD)
        defaultBindsText = [{"type": tk.Label, "text": 'KeyBind', "font": boldFont},
                            {"type": tk.Label, "text": 'Built-in Method', "font": boldFont, "anchor": 'w'},
                            {"type": tk.Label, "text": 'Set Custom Keybind', "font": boldFont}]
        addMakeFrame(defaultBindsText, self.keyBindsFrame)

        # Create Black Line Under Default Binds Text
        addBlackLine(self.keyBindsFrame)

        # Constantly Scan And Add New Keybindings
        self.updateTk()

        # Gap
        gap = tk.Frame(master=self.keyBindsFrame, height=30)
        gap.grid_rowconfigure(nextRow(self.keyBindsFrame))
        gap.grid(columnspan=3, row=nextRow(self.keyBindsFrame))

        # Custom Keybindings Label
        userBindsLabel = [{'type': tk.Label, 'text': 'KeyBind', 'font': boldFont},
                          {'type': tk.Label, 'text': 'Program Title', 'font': boldFont, 'anchor': 'w'},
                          {'type': tk.Label, 'text': 'Set Custom Keybind', 'font': boldFont}]
        addMakeFrame(userBindsLabel, self.keyBindsFrame)

        # Black Line Under User Binds Label
        addBlackLine(self.keyBindsFrame)

        # Add Razer
        self.razer = RazerTk(pm, self.window, ms)

        # Main Run
        window.mainloop()

    # Called every 500 milliseconds
    def updateTk(self):
        # Check if Backend Program died
        if self.pm.dead:
            self.window.quit()

        self.updateProgramNames()

        # Update KeyBind Stuff
        for key, val in self.im.binds.items():
            try:
                # Keybind is already on display
                temp = self.binds[key]
            except KeyError:
                # Means we don't have this keybind on display yet
                name = self.getFormattedName(vals=val)
                rebindButton = partial(self.changeKeyBind, key)
                newKeyBind = [{'type': tk.Label, 'text': key},
                              {'type': tk.Label, 'text': name, 'anchor': 'w'},
                              {'type': tk.Button, 'text': 'Click To Set Custom Keybind', 'command': rebindButton}]
                row = addMakeFrame(newKeyBind, self.keyBindsFrame)
                self.binds[key] = row

        # Call this after a time to see if any new keybindings exists
        self.window.after(500, lambda: self.updateTk())


    def getFormattedName(self, vals=None, rawText=None):
        # Get width of 2nd Column since that is where this text will go
        self.window.update()
        width = self.window.winfo_width()//3

        return cleanName(width, vals=vals, rawText=rawText)


    def changeKeyBind(self, key):
        # Get Tkinter Row involved with our Key
        row = self.binds[key].winfo_children()

        # Stop everything and wait for the user to press a key for new Keybind
        newKey = getNewKeyFromUser()

        # With our new User based input, put it in a form our program likes
        val = keysToString(newKey)

        if val == 'Key.esc' or val == '<27>':
            self.unhookProgram(key, self.binds[key])
            return
        # Rebind our button to our new button
        self.replaceBind(key, val)
        rebindButton = partial(self.changeKeyBind, val)
        row[2]['command'] = rebindButton
        row[0]['text'] = val
        return

    def replaceBind(self, oldKey, newKey):
        # Only replace the key with a Keybind we don't have already
        try:
            self.binds[newKey]
        except KeyError:
            vals = self.removeKeyBind(oldKey)
            self.addKeyBind(newKey, vals[0], vals[1], vals[2])
        return

    def removeKeyBind(self, key):
        oldVal = self.binds.pop(key)
        imVal = self.im.binds.pop(key)

        try:
            oldAfterEvent = self.im.afters[key]
        except KeyError:
            oldAfterEvent = None
        return oldVal, imVal, oldAfterEvent

    # Assumes we want to put our stuff in InputManager
    def addKeyBind(self, key, val1, val2, val3):
        self.binds[key] = val1
        self.im.binds[key] = val2
        if val3 is not None:
            self.im.afters[key] = val3

    # Called by updateTk() every 500 milliseconds
    def updateProgramNames(self):
        toDelete = []
        for key, val in self.binds.items():
            try:
                p = self.im.binds[key][1]['program']
                curName = win32gui.GetWindowText(p.gui)
                if curName != p.name:
                    p.name = curName
                    row = val.winfo_children()
                    row[1]['text'] = self.getFormattedName(rawText=p.name)
                    if p.name == '':
                        toDelete.append((key, val))
            except KeyError:
                continue
        for val in toDelete:
            self.unhookProgram(val[0], val[1])

    def unhookProgram(self, key, frame):
        self.removeKeyBind(key)
        frame.pack_forget()
        frame.destroy()

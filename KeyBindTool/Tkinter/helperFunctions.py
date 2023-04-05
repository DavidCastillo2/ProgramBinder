import tkinter as tk
from functools import partial
from tkinter.font import BOLD, Font


def nextRow(frame):
    curMax = -1
    for f in frame.winfo_children():
        try:
            if f.grid_info()['row'] > curMax:
                curMax = f.grid_info()['row']
        except KeyError:
            continue

    return curMax + 1


def addBlackLine(frame):
    blackLine = tk.Frame(master=frame, bg='black', height=4)
    blackLine.grid(columnspan=3, row=nextRow(frame), sticky='EW')
    gap = tk.Frame(master=frame, height=10)
    gap.grid_rowconfigure(nextRow(frame))
    gap.grid(columnspan=3, row=nextRow(frame))


def makeFrame(argsList, parentWindow):
    # Create our Frame and make it expandable
    holder = tk.Frame(master=parentWindow)
    holder.grid_columnconfigure(0, weight=1, uniform=True, pad=30)
    holder.grid_columnconfigure(1, weight=1, uniform=True, pad=30)
    holder.grid_columnconfigure(2, weight=1, uniform=True, pad=30)
    holder.grid(row=0, columnspan=3, sticky='EW')

    # Create Each Widget
    c = 0
    for a in argsList:
        # Make our Widgets have a Master of this Frame
        a['master'] = holder
        Type = a.pop('type')
        widget = Type(**a)
        widget.grid(column=c, row=0)
        c = c + 1
    return holder


def addMakeFrame(argsList, parentWindow):
    f = makeFrame(argsList, parentWindow)
    f.grid(columnspan=3, row=nextRow(parentWindow))
    return f

import re
from tkinter.font import Font


def cleanName(width, vals=None, rawText=None):
    weight = Font(weight='normal')

    if rawText is None:
        try:
            name = vals[1]['name']
        except KeyError:
            name = vals[1]['program'].name
    else:
        name = rawText

    textWidth = weight.measure(name)
    numNewLines = textWidth // width

    if numNewLines == 0:
        return name


    retVal = ''
    charChunkSize = len(name) // (numNewLines+1)
    curStart = 0
    while True:
        if curStart == len(name)-1:
            return retVal[0:-1]

        curChunk = name[curStart: curStart + charChunkSize]


        backUp = 0
        while True:
            if weight.measure(curChunk) >= width:
                backUp += 1
                curChunk = name[curStart: curStart + charChunkSize - backUp]
            else:
                break

        spaces = [m.start() for m in re.finditer(' ', curChunk)]

        if len(spaces) == 0 or spaces[len(spaces)-1] == 0:
            # This is a long line of text with no spaces, so we just do a harsh chop off
            retVal = retVal + curChunk + '\n'
            curStart = curStart + len(curChunk)-1
        else:
            # There are spaces we can use
            latestSpace = spaces[len(spaces)-1]
            curChunk = curChunk[0:latestSpace]
            retVal = retVal + curChunk + '\n'
            curStart = curStart + len(curChunk)


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)  # use start += 1 to find overlapping matches


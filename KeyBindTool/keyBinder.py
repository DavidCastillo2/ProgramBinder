import functools

from pynput import keyboard
from pynput.keyboard import Key


def basicBind(im, pm, ms):
    im.register(Key.pause, pm.closeAll, name='Close All')
    im.register(Key.home, pm.makeProgram, path='"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"',
                name='New Google Chrome', forceSearch=True, searchTerm='google')
    im.registerAfter(Key.home, keyFunction=im.nextButton, function=pm.toggleView)
    im.register(Key.end, pm.addCurWindow, name='Bind Current Window')
    im.registerAfter(Key.end, keyFunction=im.nextButton, function=pm.toggleView)

    # im.register(Key.page_up, createYoutube, name='New Youtube Music', pm=pm)  # Fucking ded

    # Collect events until release - Threaded task
    #      Can close this listener by Calling pynput.keyboard.Listener.stop from anywhere

    def for_canonical(f):
        return lambda k: f(listener.canonical(k))

    mm = MultikeyManager()
    listener = keyboard.Listener(
        on_press=for_canonical(functools.partial(mm.keyPressListenersOnPress, *(im, ms))),
        on_release=for_canonical(functools.partial(mm.keyPressListenersOnRelease, *(im, ms))))
    listener.start()


def keysToString(keys):
    retVal = ''
    for k in keys:
        try:
            if k.char is None:
                # print('special key pressed: {0}'.format(newButton))
                val = str(k)
            else:
                # print('Alphanumeric key pressed: {0} '.format(newButton.char))
                val = str(k.char)
        except AttributeError:
            # print('special key pressed: {0}'.format(newButton))
            val = str(k)
        retVal += val + " AND "
    return retVal[:-5]


def keyToString(key):
    try:
        if key.char is None:
            val = str(key)
        else:
            val = str(key.char)
    except AttributeError:
        val = str(key)
    return val


class MultikeyManager:
    def __init__(self):
        self.currentKeys = []
        return

    # Called on Key Pressed. Can add functions here to throw events
    def keyPressListenersOnPress(self, im, ms, key):
        # lambda k: key(listener.canonical(k))
        keyString = keyToString(key)
        if keyString not in self.currentKeys:
            self.currentKeys.append(keyString)
            im.press(keysToString(self.currentKeys))
        return

    # Called on Key Released. Can add functions here to throw events
    def keyPressListenersOnRelease(self, im, ms, key):
        # Modifier Keys such as NumLock are considered "pressed" when numpad is used sometimes
        try:
            self.currentKeys.remove(keyToString(key))
            ms.release(key)
        except ValueError:
            ms.release(key)
        return

class inputManager:
    def __init__(self, printKeys=False):
        self.binds = {}   # {key : Function, args}
        self.afters = {}  # {key : Function, args}
        self.print = printKeys
        return

    def empty(self, key):
        return

    # Main method triggered by any key press
    def press(self, keysString):
        try:
            if self.print:
                print(keysString + " Pressed")

            # Check if this key has a KeyBind
            vals = self.binds[keysString]

            # Keybind exists, run the code attacked to keybind
            retVal = vals[0](**vals[1], im=self)
            vals = self.afters[keysString]
            self.register(key=vals['keyFunction'](), function=vals['function'], program=retVal)
        except KeyError:
            pass

    def register(self, key, function, **kwargs):
        try:
            # We already have this keybind, this is an illegal move!
            catch = self.binds[str(key)]
            raise TypeError
        except KeyError:
            # We don't have this bind, so we make it
            self.binds[str(key)] = [function, kwargs]

    def registerAfter(self, keyInitial, **kwargs):
        self.afters[str(keyInitial)] = kwargs

    def nextButton(self):
        for i in range(97, 105 + 1):
            try:
                temp = self.binds['<' + str(i) + '>']
            except KeyError:
                return '<' + str(i) + '>'
        return None





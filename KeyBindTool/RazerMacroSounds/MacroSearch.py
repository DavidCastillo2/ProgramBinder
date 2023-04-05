import time


class MacroSearch:
    def __init__(self):
        self.prevKeys = []
        self.activeMacros = {}
        self.prevMacros   = {}
        self.maxDelay = 0.1
        return

    def release(self, key):
        try:
            self.prevKeys.append((key, time.time()))
        except KeyError:
            pass


    # Check over the space of a second and see if any keys have been pressed a lot
    def checkForPattern(self):
        viable  = {}
        count   = {}
        curTime = time.time()

        # Count times a key has been pressed
        curIndex = 0
        while curIndex < len(self.prevKeys):
            key, keyTime = self.prevKeys[curIndex]

            # Check if a key is new enough to be counted, otherwise delete
            if keyTime <= curTime - 1:
                del self.prevKeys[curIndex]
                continue

            # Check if a key is new enough to make a Macro Active be Viable
            if keyTime + self.maxDelay >= curTime:
                viable[key] = keyTime

            # Append to Count of Key
            try:
                count[key] += 1
            except KeyError:
                count[key] = 1
            curIndex += 1


        # Figure out if a macro is running
        pressesRequiredToTrigger = 1 // self.maxDelay
        self.prevMacros = self.activeMacros
        self.activeMacros = {}
        for key, lastTime in viable.items():
            if count[key] >= pressesRequiredToTrigger:
                self.activeMacros[key] = self.Macro(count[key], curTime-lastTime)

        return


    class Macro:
        def __init__(self, cps, d):
            self.clicksPerSecond = cps
            self.delay = d
            return


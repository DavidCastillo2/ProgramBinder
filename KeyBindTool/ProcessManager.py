import pythoncom
import win32com.client
import win32con
import win32gui
import win32process

from KeyBindTool.processCreator import Process, generalMake


class processManager:
    def __init__(self):
        self.programs = {}
        self.programNums = {}
        self.dead = False
        self.extraEnds = []  # This is a list of function to be run during closeAll()
        return

    def getNames(self):
        return self.programs.keys()

    def getProgram(self, name):
        return self.programs[name]

    def addCurWindow(self, **kwargs):
        # Get current program and add it to our list
        p = Process(None, win32gui.GetForegroundWindow())
        p.name = str(win32gui.GetWindowText(p.gui))
        self.add_HWND_program(p)
        return p

    # Main method to create a program
    def makeProgram(self, path, forceSearch=False, searchTerm=None, **kwargs):
        p = generalMake(path, forceSearch=forceSearch, searchTerm=searchTerm)
        self.addProgram(p)
        p.name = win32gui.GetWindowText(p.gui)
        return p

    def addProgram(self, p, **kwargs):
        try:
            supposedToBeNone = self.programs[str(p.gui)]
            assert (1 == 0)
            return -1
        except KeyError:
            # We do not have this program yet, add to list
            self.programs[str(p.gui)] = p
            return 1

    def add_HWND_program(self, p):
        try:
            # Program already exists
            n = self.programs[str(p.gui)]
        except KeyError:
            # Add Program to our list
            self.programs[str(p.gui)] = p

    def makeTop(self, program, **kwargs):
        p = self.programs[str(program.gui)]

        # Make Focus (same as clicking on a program where it now receives all inputs)
        if win32gui.GetForegroundWindow() != p.gui:
            # Magic fix for multiThreading??
            pythoncom.CoInitialize()
            strComputer = "."
            objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
            objSWbemServices = objWMIService.ConnectServer(strComputer, "root\cimv2")

            # Normal send keys to wake up
            shell = win32com.client.Dispatch("WScript.Shell")
            shell.SendKeys('')
            win32gui.SetForegroundWindow(p.gui)

        # Make the Program Un-minimized
        if win32gui.IsIconic(p.gui) == 1:
            # Magic fix for multiThreading??
            pythoncom.CoInitialize()
            strComputer = "."
            objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
            objSWbemServices = objWMIService.ConnectServer(strComputer, "root\cimv2")

            # Normal send keys to wake up
            shell = win32com.client.Dispatch("WScript.Shell")
            shell.SendKeys('')
            win32gui.ShowWindow(p.gui, win32con.SW_RESTORE)

    def makeBottom(self, program, **kwargs):
        p = program.gui
        win32gui.CloseWindow(p)
        return

    def closeAll(self, name=None, **kwargs):
        self.dead = True
        for n, process in self.programs.items():
            try:
                if process.prc_info is None:
                    pass
                else:
                    win32process.TerminateProcess(process.prc_info[0], -1)
            except Exception as e:
                pass
        for f in self.extraEnds:
            f()

    def toggleView(self, program, **kwargs):
        # Program is Minimized, Maximize it!
        if win32gui.IsIconic(program.gui) == 1:
            self.makeTop(program)
        # Program is NOT the focus, Make it the Focus!
        elif win32gui.GetForegroundWindow() != program.gui:
            self.makeTop(program)
        # Program is Focus, Send it to Background!
        else:
            self.makeBottom(program)


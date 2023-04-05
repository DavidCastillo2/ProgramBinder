from KeyBindTool.InputManager import inputManager
from KeyBindTool.ProcessManager import processManager
from KeyBindTool.RazerMacroSounds.MacroSearch import MacroSearch
from KeyBindTool.Tkinter.tMain import tkParty
from KeyBindTool.keyBinder import basicBind


# This is main
pm = processManager()
im = inputManager(printKeys=True)
ms = MacroSearch()
basicBind(im, pm, ms)
tp = tkParty(im, pm, ms)

# Current Run Configuration
# pyinstaller --onefile --paths=D:\env\Lib\site-packages --noconsole --add-binary "./src/chromedriver.exe;./src" --uac-admin --icon=app.ico main.py

# Run Configuration that shows console
# pyinstaller --onefile --paths=D:\env\Lib\site-packages --uac-admin --add-binary "./src/chromedriver.exe;./src" main.py

# DEPRECATED
# pyinstaller --onefile --paths=D:\env\Lib\site-packages --noconsole --uac-admin --icon=app.ico main.py


# TODO: Modifier Keys such as NumLock are considered "pressed" when numpad is used sometimes?? Lenovo Problem??
# TODO: When Listening for New Key from user, it can activate other macros. Deal with keys in chunks?

# TODO: The sendKeys inside of ProcessManager.makeTop(), those keys are being caught by InputManager
# TODO: Keybindings are currently allowed to overlap
# TODO: Manage a youtube tab for just music, have a Next Song, Fullscreen, Mute, etc bind
# TODO: Can keybind the same window multiple times :/

'''
hwnd = win32gui.GetForegroundWindow()2222
_, pid = win32process.GetWindowThreadProcessId(hwnd)
path = psutil.Process(pid).exe()
'''



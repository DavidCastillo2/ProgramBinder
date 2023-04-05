import time

import win32con
import win32gui
import win32process


class Process:
    def __init__(self, prc, guiHWND):
        self.name = None  # Just for organization
        self.prc_info = prc  # Core Process, used for Termination and Thread management
        self.gui = guiHWND  # Used by win32gui - referred to as hwnd
        return

    def __repr__(self):
        retVal = "Name: '" + str(self.name) + "'\n"
        retVal = retVal + "\thwnd (GUI): " + str(self.gui)
        retVal = retVal + "\tprcInfo:    " + str(self.prc_info)
        return retVal


# http://timgolden.me.uk/pywin32-docs/win32process__CreateProcess_meth.html
# The result of win32process.CreateProcess:
#   is a tuple of (hProcess, hThread, dwProcessId, dwThreadId)
#   dwProcessId = PID

# DEPRECATED
def _createChrome():
    startupInfo = win32process.STARTUPINFO()
    prc_info = win32process.CreateProcess(None, '"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"', None,
                                          None, True, win32con.CREATE_NEW_CONSOLE, None, 'c:\\', startupInfo)
    return prc_info


# DEPRECATED
def _createNotepad():
    startupInfo = win32process.STARTUPINFO()
    prc_info = win32process.CreateProcess(None, "Notepad.exe", None,
                                          None, True, win32con.CREATE_NEW_CONSOLE, None, 'c:\\', startupInfo)
    return prc_info


# Main Make for all programs
def generalMake(path, forceSearch=False, searchTerm=None):

    # Get all current Windows
    prev = []
    if forceSearch:
        assert(searchTerm is not None)
        prev = getAllWindows()

    # Start the requested program
    startupInfo = win32process.STARTUPINFO()
    prc_info = win32process.CreateProcess(None, path, None,
                                          None, True, win32con.CREATE_NEW_CONSOLE, None, 'c:\\', startupInfo)

    # Find New Window and Return It
    return getNewestProgram(prev, searchTerm, prc_info, forceSearch)


# Find New Window and Return It
def getNewestProgram(prev, searchTerm, prc_info, forceSearch=False):
    if forceSearch:
        after = getAllWindows()
        val = _getNewWindows(after, prev, searchTerm.lower())
        while val is None:
            after = getAllWindows()
            val = _getNewWindows(after, prev, searchTerm.lower())
        return Process(prc_info, val)
    else:
        val = _getWindow(prc_info)
        while val is None:
            val = _getWindow(prc_info)

        return Process(prc_info, val)


def _getWindow(process):
    """
    :rtype: Value For win32gui Calls FROM process PID
    """
    result = None

    def callback(hwnd, _):
        nonlocal result
        ctid, cpid = win32process.GetWindowThreadProcessId(hwnd)
        if cpid == process[2]:
            result = hwnd
            return False
        return True

    try:
        win32gui.EnumWindows(callback, None)
    except Exception as e:
        if str(e).find("(0, 'EnumWindows', 'No error message is available')") == -1:
            raise e
    return result


def _getUsefulWindows(arr1, searchTerm):
    retVal = []
    for a in arr1:
        text = win32gui.GetWindowText(a).lower()
        if text.find(searchTerm) != -1:
            retVal.append(a)
    return retVal


def _getNewWindows(array1, array2, searchTerm):
    arr1 = _getUsefulWindows(array1, searchTerm)
    arr2 = _getUsefulWindows(array2, searchTerm)
    retVal = []
    for a in arr1:
        found = False
        for b in arr2:
            if a == b:
                found = True
                break
        if not found:
            retVal.append(a)

    if len(retVal) == 0:
        return None
    assert(len(retVal) == 1)
    return retVal[0]


def getAllWindows():
    def enum_window_titles():
        def callback(handle, data):
            nonlocal titles
            titles.append(handle)

        titles = []
        win32gui.EnumWindows(callback, None)
        return titles

    return enum_window_titles()




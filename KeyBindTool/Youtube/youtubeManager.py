import os
import sys

import win32con
import win32gui
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, \
    ElementClickInterceptedException, NoSuchWindowException, InvalidArgumentException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from Config import Config
import KeyBindTool.processCreator as pc


class youManager:

    def __init__(self):
        self.driver = None
        self.visible = True
        self.dead = False
        self.retail = False
        self._setup()
        return

    def _setup(self):
        if self.driver is None:
            chromeOptions = Options()
            if not self.visible:
                chromeOptions.add_argument('--headless')
            # chromeOptions.add_argument("user-data-dir=c:\\Users\\NokiaPhone\\AppData\\Local\\Google\\Chrome\\User Data\\")  # Fucks everything ; -;

            if self.retail:
                def resource_path(relative_path):
                    try:
                        base_path = sys._MEIPASS
                    except Exception:
                        base_path = os.path.dirname(__file__)
                    return os.path.join(base_path, relative_path)

                path = resource_path('./src/chromedriver.exe')  # For .exe - use
            else:
                path = Config().getPath('src/chromedriver.exe')  # For in IDE - use

            previous = pc.getAllWindows()
            try:
                self.driver = webdriver.Chrome(executable_path=path, chrome_options=chromeOptions)
            except InvalidArgumentException:
                process = pc.getNewestProgram(previous, 'chrome', prc_info=None, forceSearch=True)
                win32gui.PostMessage(process.gui, win32con.WM_CLOSE, 0, 0)
                self.driver = webdriver.Chrome(executable_path=path)
            self.driver.get('https://www.youtube.com/')

    def togglePausePlay(self, **kwargs):
        self.sendKeys(' ')
        return False

    def nextVideo(self, **kwargs):
        self.sendKeys('N')

    def volumeDown(self, **kwargs):
        self.sendToPlayer(Keys.ARROW_DOWN)

    def volumeUp(self, **kwargs):
        self.sendToPlayer(Keys.ARROW_UP)

    def toggleFullScreen(self, **kwargs):
        self.sendKeys('f')

    def sendToPlayer(self, keys, **kwargs):
        try:
            if self._ifPlayer():
                try:
                    element = self.driver.find_element_by_id('movie_player')
                except NoSuchElementException:
                    return False
                if element is not None:
                    try:
                        element.send_keys(keys)
                        return True
                    except ElementNotInteractableException or ElementClickInterceptedException:
                        return False
            return False
        except NoSuchWindowException:
            self.dead = True
            return False

    def sendKeys(self, keys):
        try:
            if self._ifPlayer():
                element = self._root()
                if element is not None:
                    element.send_keys(keys)
                    return True
        except NoSuchWindowException:
            self.dead = True
            return False
        return False

    def _ifPlayer(self):
        try:
            self.driver.find_element_by_class_name('html5-video-container')
            return True
        except NoSuchElementException:
            return False

    def _root(self):
        return self.driver.find_element_by_xpath("/*")

    def close(self):
        self.driver.close()
        return


def createYoutube(im, pm, **kwargs):
    previous = pc.getAllWindows()
    ym = youManager()
    process = pc.getNewestProgram(previous, 'chrome', prc_info=None, forceSearch=True)
    pm.addProgram(process)
    massBind(im, pm, ym, process)
    return process


def massBind(im, pm, ym, process):
    im.register(im.nextButton(), ym.toggleFullScreen, name='Toggle Fullscreen')
    im.register(im.nextButton(), ym.togglePausePlay, name='Pause/Play')
    im.register(im.nextButton(), ym.volumeUp, name='Volume Up +')
    im.register(im.nextButton(), ym.volumeDown, name='Volume Down -')
    im.register(im.nextButton(), ym.nextVideo, name='Next Video')
    im.register(im.nextButton(), pm.toggleView, program=process)
    pm.extraEnds.append(ym.close)

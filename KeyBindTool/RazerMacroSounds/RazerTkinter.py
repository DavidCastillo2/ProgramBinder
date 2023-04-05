import tkinter as tk
from tkinter import CENTER, RIGHT, LEFT
from tkinter.font import BOLD, Font

from KeyBindTool.Tkinter.helperFunctions import nextRow, addMakeFrame, addBlackLine


class RazerTk:
    def __init__(self, pm, tkMain, ms):
        self.activeMacros = {}
        self.pm = pm
        self.window = tkMain
        self.razerWindow = tk.Frame(master=self.window)
        self.razerWindow.grid_columnconfigure(0, weight=1)
        self.razerWindow.grid_columnconfigure(1, weight=1)
        self.razerWindow.grid_columnconfigure(2, weight=1)
        self.razerWindow.rowconfigure(2, minsize=0, weight=0)
        self.razerWindow.pack()
        self.ms = ms

        # Gap
        gap = tk.Frame(master=self.razerWindow, height=120)
        gap.grid_rowconfigure(nextRow(self.razerWindow))
        gap.grid(columnspan=3, row=nextRow(self.razerWindow))

        # Basic top text
        boldFont = Font(self.razerWindow, size=12, weight=BOLD)
        defaultBindsText = [{"type": tk.Label, "text": 'Macro Key', "font": boldFont},
                            {"type": tk.Label, "text": 'Clicks Per Second', "font": boldFont, "anchor": 'w'},
                            {"type": tk.Label, "text": 'Delay', "font": boldFont}]
        addMakeFrame(defaultBindsText, self.razerWindow)

        # Create Black Line Under Default Binds Text
        addBlackLine(self.razerWindow)

        self.update()
        return


    def update(self):
        self.ms.checkForPattern()
        self.checkMacros()

        self.window.after(500, lambda: self.update())
        return


    def checkMacros(self):
        for key, macro in self.ms.activeMacros.items():
            try:
                # Macro is on display
                self.activeMacros[key]
            except KeyError:

                # We don't have this macro on display
                newMacro = [{'type': tk.Label, 'text': str(key)},
                            {'type': tk.Label, 'text': str(macro.clicksPerSecond), 'anchor': 'w'},
                            {'type': tk.Label, 'text': '%0.5f' % macro.delay}]
                row = addMakeFrame(newMacro, self.razerWindow)
                self.activeMacros[key] = row

        # Update out macro text based on newest information
        self.updateText()


    def updateText(self):
        toDelete = []
        for key, macroRow in self.activeMacros.items():
            try:
                # This macro still exists. Update Text
                macro = self.ms.activeMacros[key]
                row = macroRow.winfo_children()
                row[1]['text'] = str(macro.clicksPerSecond)
                row[2]['text'] = '%0.5f' % macro.delay
            except KeyError:
                # This macro has finished. Remove it from display
                toDelete.append((key, macroRow))

        for key, row in toDelete:
            row.grid_forget()
            row.destroy()
            del self.activeMacros[key]

        return

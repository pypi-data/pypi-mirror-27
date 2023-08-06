#!/usr/bin/env python3

import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import pkgutil as pkg

class Expander(Frame):
    """Container capable of hiding its child

       Options:
           - text --- The text to be shown in the button
           - expanded --- Whether the child should be shown (defaults to True)

       Property:
           - button --- The inner Button widget
           - frame --- The inner Frame widget

       Forms of access:
           >>> from witkets import Expander
           >>> expander = Expander(text='Advanced Options')
           >>> expander['expanded'] = False
           >>> expander.config(text='Basic Options')
    """
    
    def __init__(self, master=None, text='', expanded=True, **kw):
        """Constructor
           - text --- Label text
           - content --- The widget to be expanded or collapsed
           - expanded --- Whether the child should be shown
        """
        Frame.__init__(self, master, **kw)
        arrow_right_data = pkg.get_data('witkets', 'data/xbm/arrow-right-16.xbm')
        self._arrow_right = BitmapImage(data=arrow_right_data)
        arrow_down_data = pkg.get_data('witkets', 'data/xbm/arrow-down-16.xbm')
        self._arrow_down = BitmapImage(data=arrow_down_data)
        self.button = tk.Button(self, text=text, image=self._arrow_down, compound=LEFT)
        self.button['anchor'] = W
        self.button.pack(fill=X)
        self.button['command'] = self._onToggle
        self.frame = Frame(self)
        self._expanded = expanded
        if expanded:
            self.button['image'] = self._arrow_down
            self.frame.pack()
        else:
            self.button['image'] = self._arrow_right

    def __setitem__(self, key, val):
        if key == 'text':
            self.button['text'] = val
        elif key == 'expanded':
            self._expanded = val
            self._update()
        else:
            Frame.__setitem__(self, key, val)

    def __getitem__(self, key):
        if key == 'text':
            return self.button['text']
        elif key == 'expanded':
            return self.expanded
        return Frame.__getitem__(self, key)

    def config(self, **kw):
        """Standard Tk config method"""
        for key in kw:
            if key in ('text', 'expanded'):
                self.__setitem__(self, key, kw[key])
                kw.pop(key, False)
        Frame.config(self, **kw)
        self._update()    

    def _update(self):
        if self._expanded:
            self.button['image'] = self._arrow_down
            self.frame.pack()
        else:
            self.button['image'] = self._arrow_right
            self.frame.pack_forget()
        
    def _onToggle(self):
        self._expanded = not self._expanded
        self._update()

if __name__ == '__main__':
    root = Tk()
    expander = Expander(root, text='Test')
    label = Label(expander.frame, text='Label')
    label.pack()
    expander.pack()
    root.mainloop()

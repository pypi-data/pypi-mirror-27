#!/usr/bin/env python3

from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *

class ThemedLabelFrame(LabelFrame):
    """A frame with a title label, both themed
        
       Options (all have default values):
          - title --- The text of the title label
          - labelstyle --- The style applied to the title label 
            Default value: 'BlkTitle.TLabel'
          - framestyle --- The style applied to the frame
            Default value: 'Blk.TFrame'
        
       Forms of access:
          >>> from witkets.themedlabelframe import ThemedLabelFrame
          >>> frm = ThemedLabelFrame(title='Test')
          >>> frm['title'] = 'Test 2'
          >>> frm.config(title = 'Test 3')
    """
    def __init__(self, master=None, title=' ', labelstyle='BlkTitle.TLabel',
                 framestyle='Blk.TFrame', **kw):
        self._varTitle = StringVar()
        self._varTitle.set(title)
        self._lblTitle = Label(master, textvariable=self._varTitle)
        self._lblTitle['style'] = labelstyle
        LabelFrame.__init__(self, master, labelwidget=self._lblTitle, **kw)
        self['style'] = framestyle
    
    def __setitem__(self, key, val):
        if key == 'title':
            self._varTitle.set(val)
        elif key == 'labelstyle':
            self._lblTitle['style'] = val
        elif key == 'framestyle':
            self['style'] = val
        else:
            LabelFrame.__setitem__(self, key, val)
            
    def config(self, **kw):
        """Standard Tk config method"""
        for key in kw:
            if key in ('title', 'labelstyle', 'framestyle'):
                if key == 'title':
                    self._varTitle.set(val)
                elif key == 'labelstyle':
                    self._lblTitle['style'] = val
                elif key == 'framestyle':
                    self['style'] = val
            kw.pop(key, False)
        LabelFrame.config(self, **kw)
        
if __name__ == '__main__':
    root = Tk()
    #Configuring styles
    from witkets.theme import Theme, WITKETS_DEFAULT_THEME
    s = Style()
    s.theme_use('clam')
    theme = Theme(s)
    theme.setDefaultFonts()
    theme.applyDefaultTheme()
    #Creating themed labelframe
    frm = ThemedLabelFrame(root)
    frm['title'] = 'Test'
    btn = Button(frm, text='test')
    btn.pack()
    frm.pack(padx=15, pady=15)
    root.mainloop()

#!/usr/bin/env python3

from enum import Enum
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename, askdirectory, asksaveasfilename

class FileChooserAction(Enum):
    """File chooser actions (OPEN, SAVE or SELECT_FOLDER)"""
    OPEN = 'open'
    SAVE  = 'save'
    SELECT_FOLDER = 'select-folder'

class FileChooserEntry(Frame):
    """Entry and button intended to choose a file or directory
    
       The chosen path can be accessed either through the :code:`get` method or
       by a Tk StringVar set via the *textvariable* option.
       
       Options:
         - textvariable --- Tk StringVar used to stock the filepath
         - buttontext --- Choose button text
         - dialogtitle --- Dialog window title
         - action --- FileChooserAction (OPEN, SAVE or SELECT_FOLDER)
         - format --- File Formats (applies only to OPEN or SAVE actions)
         - All :code:`Frame` widget options
         
       Attributes:
         - button --- The "Choose" button
         - entry --- The entry displaying the selected filename

    """

    def __init__(self, master, textvariable=None, buttontext='Choose...', 
                 dialogtitle='Choose...', action=FileChooserAction.OPEN, **kw):
        if 'format' in kw:
            self._format = kw['format']
            kw.pop('format', False)
        else:
            self._format = [('All files', '*.*')]
        Frame.__init__(self, master, **kw)
        #Variables
        self._varEntry = StringVar()
        self._var = textvariable if textvariable else StringVar(value='')
        self._dialogtitle = dialogtitle
        self._action = action
        #Widgets
        self.entry = Entry(self, state='disabled')
        self.entry['state'] = 'disabled'
        self.entry['textvariable'] = self._varEntry
        self.entry['style'] = 'ReadOnlyEntry.TEntry'
        self.entry['width'] = 30
        self.entry.pack(side=LEFT, fill=X, expand=1)
        self.button = Button(self, text=buttontext)
        self.button['command'] = self._choose
        self.button.pack(side=LEFT)
        self._var.trace('w', self._update)
            
    def __setitem__(self, key, val):
        if key == 'textvariable':
            self._var = val
            self._var.trace('w', self._update)
        elif key == 'buttontext':
            self.button['text'] = val
        elif key in ('format', 'dialogtitle', 'action'):
            self.__setattr__('_' + key, val)
        else:
            Frame.__setitem__(self, key, val)
            
    def __getitem__(self, key):
        if key == 'textvariable':
            return self._var
        elif key == 'buttontext':
            return self.button['text']
        elif key in ('format', 'dialogtitle', 'action'):
            return self.__getattr__('_' + key)
        else:
            return Frame.__getitem__(self, key)
            
    def config(self, **kw):
        """Tk standard config method"""
        if 'textvariable' in kw:
            self._var = kw['textvariable']
            kw.pop('textvariable', False)
        if 'buttontext' in kw:
            self.button['text'] = kw['buttontext']
            kw.pop('buttontext', False)
        baseKw = {}
        for key in kw:
            if key in ('format', 'dialogtitle', 'action'):
                self.__setattr__('_' + key, kw[key])
            else:
                baseKw[key] = kw[key]
        Frame.config(self, **baseKw)
        
    def get(self):
        """Gets the current selected file path"""
        return self._var.get()
        
    def _choose(self):
        """Choose button callback"""
        if self._action == FileChooserAction.OPEN:
            path = askopenfilename(parent=self, filetypes=self._format,
                                   title=self._dialogtitle)
        elif self._action == FileChooserAction.SAVE:
            path = asksaveasfilename(parent=self, filetypes=self._format, 
                                     title=self._dialogtitle)
        else:
            path = askdirectory(parent=self, title=self._dialogtitle)
        self._var.set(path)
        self._update()
        
    def _update(self, event=None, *args):
        """Update label"""
        lbl = self._var.get()
        width = self.entry['width']
        lbl = lbl if len(lbl) < width else '...' + lbl[-(width - 4):]
        self.entry['state'] = 'normal'
        self._varEntry.set(lbl)
        self.entry['state'] = 'disabled'
        
if __name__ == '__main__':
    root = Tk()
    Label(root, text='Open, save as and select folder: ').pack()
    chooser = FileChooserEntry(root)
    chooser2 = FileChooserEntry(root, buttontext='Escolher')
    chooser2['action'] = FileChooserAction.SAVE
    chooser2['dialogtitle'] = 'Salvar como...'
    chooser3 = FileChooserEntry(root, action=FileChooserAction.SELECT_FOLDER)
    chooser3.config(buttontext='Choisir...', dialogtitle='Je veux un dossier')
    chooser.pack()
    chooser2.pack()
    chooser3.pack()
    root.mainloop()
    


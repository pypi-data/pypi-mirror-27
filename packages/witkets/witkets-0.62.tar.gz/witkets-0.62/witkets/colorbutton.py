#!/usr/bin/env python3

from tkinter import *
from tkinter.ttk import *
from tkinter.colorchooser import askcolor

class ColorButton(Canvas):
    """A button to launch color selection dialog
    
    This widget mocks GtkColorButton from the Gtk toolkit. It is "a button
    which displays the currently selected color an allows to open a color
    selection dialog".
    
    Options:
      - color --- Selected/displayed color
      - textvariable --- Tk StringVar to stock color
      - All :code:`Canvas` widget options (notably width and height)
    
    Forms of access:
      >>> from tkinter import *
      >>> from witkets.colorbutton import ColorButton
      >>> ...
      >>> btn = ColorButton(root, color='#008')
      >>> currColor = btn['color']
      >>> varColor = StringVar()
      >>> btn.config(textvariable = varColor)
    
    """

    def __init__(self, master, color='#CCC', textvariable=None, **kw):
        if 'width' not in kw:
            kw['width'] = 25
        if 'height' not in kw:
            kw['height'] = 25
        Canvas.__init__(self, master, **kw)
        if not textvariable:
            self._var = StringVar()
        else:
            self._var = textvariable
        self._var.set(color)
        self._var.trace('w', self._redraw)
        self._rect = None
        self._redraw()
        self.bind('<Button-1>', self._showDialog)
        
    #######################################################################
    # Inherited Methods
    #######################################################################
        
    def __setitem__(self, key, val):
        if key == 'color':
            self._var.set(val)
        elif key == 'textvariable':
            self._var = val
            self._var.trace('w', self._redraw)
        else:
            Canvas.__setitem__(self, key, val)
        self._redraw()
        
    def __getitem__(self, key):
        if key == 'color':
            return self._var.get()
        elif key == 'textvariable':
            return self._var
        else:
            return Canvas.__getitem__(self, key)
            
    def config(self, **kw):
        """Tk standard config method"""
        if 'color' in kw:
            self._var.set(kw[key])
            kw.pop(key, False)
        if 'textvariable' in kw:
            self._var = kw[key]
            self._var.trace('w', self._redraw)
            kw.pop(key, False)
        Canvas.config(self, **kw)

    def _redraw(self, *args):
        w, h = int(self['width']), int(self['height'])
        if self._rect:
            self.delete(self._rect)
        self._rect = self.create_rectangle(0, 0, w, h, fill=self._var.get())
                
    def _showDialog(self, event=None):
        newColor = askcolor(color=self._var.get())[1]
        if newColor:
            self._var.set(newColor)
            self._redraw()

#######################################################################            
# Test script
#######################################################################
            
if __name__ == '__main__':
    root = Tk()
    Label(root, text='Color Button Example --> click it!').pack()
    a = ColorButton(root, color='red')
    var = StringVar()
    a['textvariable'] = var
    var.set('#00F')
    a.pack()
    root.mainloop()
    
    

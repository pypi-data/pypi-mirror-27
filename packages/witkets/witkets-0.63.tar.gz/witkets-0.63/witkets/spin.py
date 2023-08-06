#!/usr/bin/env python3

import tkinter as tk
import tkinter.ttk as ttk

class Spin(ttk.Frame):
    """Spin Box with features such as custom number formatting and 
       orientation.
        
       Options (all have default values):
          - circular --- Toggles circular increments and decrements
          - from --- Minimum numeric value
          - orientation --- Either tk.HORIZONTAL (default) or tk.VERTICAL 
            (constructor only)
          - numberformat --- The format applied to the number (default: '%d')
          - step --- Delta applied to the value when buttons are clicked
          - to --- Maximum numeric value
          - variable --- A Tk numeric variable to store the number
          - All :code:`Frame` widget options
    """
    def __init__(self, master=None, from_=0, to=100, step=1, numberformat='%d', 
                 variable=None, circular=False, orientation=tk.HORIZONTAL, **kw):
        ttk.Frame.__init__(self, master, **kw)
        self._widgetKeys = ('from', 'to', 'step', 'numberformat', 'variable', 
                            'circular')
        #Button plus
        self._buttonPlus = tk.Button(self, text='+', width=1)
        self._buttonPlus['command'] = self._handlePlus
        #Text and numeric variables
        self._textvariable = tk.StringVar()
        if not variable:
            self._var = tk.DoubleVar()
        else:
            self._var = variable
        self._var.trace('w', self._update)
        #Entry
        self.entry = ttk.Entry(self, textvariable=self._textvariable)
        self.entry['justify'] = tk.CENTER
        #Button minus
        self._buttonMinus = tk.Button(self, text='-', width=1)
        self._buttonMinus['command'] = self._handleMinus
        #Parameters (@TODO Add getattr and other access methods)
        self._minValue = from_
        self._maxValue = to
        self._step = step
        self._numberformat = numberformat
        self._circular = circular
        #Initial value
        self._var.set(self._minValue)
        #Orientation
        if orientation == tk.HORIZONTAL:
            self.entry.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)
            self._buttonMinus.pack(side=tk.LEFT, fill=tk.Y)
            self._buttonPlus.pack(side=tk.LEFT, fill=tk.Y)
        else:
            self._buttonPlus.pack(fill=tk.X)
            self.entry.pack(expand=1, fill=tk.BOTH)
            self._buttonMinus.pack(fill=tk.X)
            self._buttonPlus['relief'] = tk.FLAT
            self._buttonMinus['relief'] = tk.FLAT
        
    #######################################################################
    # Value read and write
    #######################################################################
        
    def get(self):
        """Sets the numeric value of the entry"""
        return self._var.get()
        
    def set(self, value):
        """Get the numeric value of the entry"""
        self._var.set(value)
        
    #######################################################################
    # Private Methods
    #######################################################################
    
    def _update(self, *args):
        val = self._var.get()
        self._textvariable.set(self._numberformat % val)
        
    def _handlePlus(self):
        nextValue = self._var.get() + self._step
        if nextValue < self._maxValue:
            self._var.set(nextValue)
        elif not self._circular:
            self._var.set(self._maxValue)
        else:
            self._var.set(self._minValue)
        
    def _handleMinus(self):
        nextValue = self._var.get() - self._step
        if nextValue > self._minValue:
            self._var.set(nextValue)
        elif not self._circular:
            self._var.set(self._minValue)
        else:
            self._var.set(self._maxValue)
            
    def _checkLimits(self):
        value = self._var.get()
        if not value:
            self._var.set(self._minValue)
        elif value < self._minValue:
            self._var.set(self._minValue)
        elif value > self._maxValue:
            self._var.set(self._maxValue)
            
    #######################################################################
    # Config methods
    #######################################################################
    
    def _handleWitketKey(self, key, val):
            if key == 'variable':
                self._var = val
                self._var.trace('w', self._update)
                self._checkLimits()
            elif key == 'from':
                self._minValue = val
                self._checkLimits()
            elif key == 'to':
                self._maxValue = val
                self._checkLimits()
            else:
                self.__setattr__('_' + key, val)
                self._update()

    def __setitem__(self, key, val):
        if key in self._widgetKeys:
            self._handleWitketKey(key, val)
        else:
            Frame.__setitem__(self, key, val)
        
    def __getitem__(self, key):
        if key in self._widgetKeys:
            if key == 'variable':
                return self._var
            elif key == 'from':
                return self._minValue
            elif key == 'to':
                return self._maxValue
            else:
                return self.__getattribute__('_' + key)
        else:
            return Frame.__getitem__(self, key)
            
    def config(self, **kw):
        """Standard Tk config method"""
        for key, val in kw.iteritems():
            if key in self._widgetKeys:
                self._handleWitketKey(key, val)
                kw.pop(key, False)
        Frame.config(self, **kw)


    
if __name__ == '__main__':
    root = tk.Tk()
    spin1 = Spin(root)
    spin1.pack(side=tk.LEFT, padx=15)
    spin1.set(10)
    spin1.entry['width'] = 2
    spin2 = Spin(root, orientation=tk.VERTICAL, numberformat='%06.3f')
    spin2.pack(side=tk.LEFT, padx=15)
    spin2.entry['width'] = 7
    spin2.set(3.238)
    root.mainloop()

#!/usr/bin/env python3

from collections import OrderedDict
from tkinter import *
from tkinter.ttk import *

class CardLayout(Frame):
    """Special container that displays only one child at a time
        
      Options
        - All :code:`Frame` widget options
    
    """
    def __init__(self, master=None, **kw):
        Frame.__init__(self, master, **kw)
        self._cards = OrderedDict()
        self._currentCard = None
        
    def add(self, widget, name):
        self._cards[name] = widget
        if not self._currentCard:
            widget.pack()
            self._currentCard = name
            
    def first(self):
        keys = list(self._cards.keys())
        self.show( keys[0] )
        
    def last(self):
        keys = list(self._cards.keys())
        self.show( keys[-1] )
            
    def next(self):
        keys = list(self._cards.keys())
        index = keys.index(self._currentCard)
        size = len(keys)
        newIdx = index + 1
        if newIdx > size - 1:
            newIdx -= size
        self.show(keys[newIdx])

    def previous(self):
        keys = list(self._cards.keys())
        index = keys.index(self._currentCard)
        size = len(keys)
        newIdx = index - 1
        if newIdx < 0:
            newIdx += size
        self.show(keys[newIdx])
                
    def show(self, name):
        for c in self._cards.values():
            c.pack_forget()
        self._cards[name].pack()
        self._currentCard = name
        
if __name__ == '__main__':
    def changeCard():
        global cards
        cards.next()

    root = Tk()
    cards = CardLayout(root)
    label1 = Label(cards, text='Some Card')
    label2 = Label(cards, text='Other Card')
    cards.add(label1, 'card1')
    cards.add(label2, 'card2')
    button = Button(root, text='Change Card')
    button.pack()
    button['command'] = changeCard
    cards.pack()
    root.mainloop()

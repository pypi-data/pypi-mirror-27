import tkinter as tk
from tkinter import font
import webbrowser

class LinkButton(tk.Button):
    """A button bound to a URL""" 
    def __init__(self, master=None, **kw):
        tk.Button.__init__(self, master, **kw)
        self._font = font.Font(self, self.cget("font"))
        self._font.configure(underline = True)
        self._visited = False
        self._updateFont()
        self['command'] = self.visitLink
        
    def visitLink(self):
        """Default button action: open URL in a Web browser"""
        webbrowser.open(self['text'])
        self._visited = True
        self._updateFont()
        
    def getVisited(self):
        """Checks whether this button has been clicked"""
        return self._visited
        
    def setVisited(self, visited):
        """Alters the visited state of this button"""
        self._visited = visited
        self._updateFont()
        
    def _updateFont(self):
        color = 'blue' if not self._visited else 'blueviolet'
        self.configure(fg = color, activeforeground = color)
        
        
if __name__ == '__main__':
    root = tk.Tk()
    link = LinkButton(root, text='http://www.google.com.br')
    link.setVisited(False)
    link.pack(padx=20, pady=20)
    root.mainloop()

from tkinter import *
from tkinter.ttk import *

class AccelLabel(Frame):
    """A label which displays an accelerator key on the right of the text
    
        Options:
            - All :code:`Frame` widget options
            
        Public attributes:
            - label --- Main label widget
            - accel --- Label containing the accelerator string
    """
    def __init__(self, master=None, label='', accel='', **kw):
        """Initializer
        
        Parameters:
            - master --- Parent widget
            - label --- Label text
            - accel --- Accelerator text
        """
        Frame.__init__(self, master, **kw)
        self.label = Label(self, text=label)
        self.label['justify'] = LEFT
        self.label.pack(side=LEFT, padx=(0, 30), expand=1, fill=X)
        self.accel = Label(self, text=accel)
        self.accel['justify'] = RIGHT
        self.accel.pack(side=RIGHT, fill=X)
        
if __name__ == '__main__':
    root = Tk()
    a = AccelLabel(root, label='Copy', accel='CTRL+C')
    a.pack(expand=1, fill=X, padx=20, pady=20)
    root.mainloop()

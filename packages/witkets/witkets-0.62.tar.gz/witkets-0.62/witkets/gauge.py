#!/usr/bin/env python3

from tkinter import *
from tkinter.ttk import *
from math import sqrt, sin, cos, pi, atan2

class Gauge(Canvas):
    """A widget for setting values by rotating a knob
    
    This widget is an alternative way of inputting numbers in a range.
    
    Options:
      - number --- The current value
      - numvariable --- Numeric variable to store the current value
      - maxvalue --- Maximum value (proportional to maximum angle)
      - minvalue --- Minimum value (proportional to minimum angle)
      - tickcount --- Number of ticks along the scale
      - startang --- Starting angle
      - endang --- Ending angle (must be greater than *startang*)
      - knobrelradius --- Knob radius relative to the total radius [0..1]
      - knobcolor --- Knob color (inner radius)
      - scalecolor --- Scale color (outer radius)
      - tickcolor --- Ticks color
      - cursorcolor --- Cursor color
      - cursorwidth --- Cursor line width
      - All :code:`Canvas` widget options (notably width and height)

    Forms of access:
      >>> from tkinter import *
      >>> from witkets.gauge import Gauge
      >>> root = Tk()
      >>> ...
      >>> gauge = Gauge(root)
      >>> gauge['width'] = gauge['height'] = 400
      >>> gauge.enableMouse()
      >>> gauge.config['cursorwidth'] = 5
      >>> gauge['cursorcolor'] = '#800000'
    
    """
    def __init__(self, master=None, number=0, numvariable=None,
                 maxvalue=100, minvalue=0, tickcount=20, startang=-60, 
                 endang=240, knobrelradius=0.75, knobcolor='#CCCCCC', 
                 scalecolor='#EEEEEE', tickcolor='#333333', 
                 cursorcolor='#333333', cursorwidth=2, **kw):
        self._widgetKeys = [
            'number', 'numvariable', 'maxvalue', 'minvalue', 'tickcount', 
            'startang', 'endang', 'knobrelradius', 'knobcolor', 'scalecolor', 
            'tickcolor', 'cursorcolor', 'cursorwidth' ]
        
        #Canvas init
        if 'width' in kw:
            kw['height'] = kw['width']
        elif 'height' in kw:
            kw['width'] = kw['height']
        else:
            kw['width'] = kw['height'] = 120
        if 'background' not in kw:
            kw['background'] = '#FFF'
        Canvas.__init__(self, master, **kw)
        
        #Widget-specific Properties
        if not numvariable:
            self._var = DoubleVar()
        else:
            self._var = numvariable
        self._minvalue = minvalue
        self._maxvalue = maxvalue
        self._tickcount = tickcount
        self._knobrelradius = knobrelradius
        self._knobcolor = knobcolor
        self._scalecolor = scalecolor
        self._tickcolor = tickcolor
        self._cursorcolor = cursorcolor
        self._cursorwidth = cursorwidth
        self._startang = startang
        self._endang = endang
        self._var.set(number)
        self._var.trace('w', self._redraw)

        #Mouse related
        self._motion = False

        #First draw
        self._reconfigure()

    def _reconfigure(self):
        """Reconfigures internal state and redraws everything"""
        self._height = int(self['height'])
        self._width = int(self['width'])
        self._xc, self._yc = self._width >> 1, self._height >> 1
        self.delete(ALL)
        self._draw_structure()
        self._draw_knob()

    #######################################################################
    # Helper methods
    #######################################################################

    def _radius_at(self, radians, a, b):
        """Evaluates the radius for a given angle"""
        return a*b / sqrt( (a*cos(radians))**2 + (b*sin(radians))**2 )

    def _get_limit_radians(self):
        """Corrects the angle interval.

            This function adds 360 degrees to the angle limits until 
            both are positive.

            The lower and upper limits are returned in radians.
        """
        angle1 = self._startang
        angle2 = self._endang
        while angle1 < 0:
            angle1 += 360
            angle2 += 360
        return (angle1 * pi/180, angle2 * pi/180)

    #######################################################################
    # Drawing Functions
    #######################################################################

    def _draw_structure(self):

        #Scale
        c = (1, 1, self._width - 1, self._height - 1)
        self.create_oval(fill=self._scalecolor, *c)
        
        #Center coords
        xc, yc = self._xc, self._yc #shortcut

        #Ticks
        angle, last_angle = self._get_limit_radians()
        step = (last_angle - angle) / (self._tickcount - 1)
        tick = 0
        while tick < self._tickcount:
            radius = self._radius_at(angle, a=xc, b=yc)
            x,y = int(radius * cos(angle)), int(radius * sin(angle))
            self.create_line(xc, yc, xc + x, yc - y, fill=self._tickcolor)
            angle += step
            tick += 1


    def _draw_knob(self):
        xc, yc = self._xc, self._yc

        #Knob
        topleft = 1 - self._knobrelradius       #default: 0.25
        bottomright = 1 + self._knobrelradius   #default: 1.75
        # xc and yc are also a and b (major and minor radius)
        c = ( xc * topleft, yc * topleft, xc * bottomright, yc * bottomright )
        self._knob = self.create_oval(fill=self._knobcolor, *c)

        #Cursor
        num = self._var.get()
        percent = (num - self._minvalue) / (self._maxvalue - self._minvalue)
        percent = 1 - percent # number raises counterclockwise direction

        start_angle, last_angle = self._get_limit_radians()
        angle = start_angle + percent * (last_angle - start_angle)
        radius = self._radius_at(angle,
            a=xc*self._knobrelradius, 
            b=yc*self._knobrelradius
        )
        x,y = int(radius * cos(angle)), int(radius * sin(angle))
        self._cursor = self.create_line(xc, yc, xc + x, yc - y, 
            fill=self._cursorcolor, width=self._cursorwidth)

    def _redraw(self, *args):
        self.delete(self._knob)
        self.delete(self._cursor)
        self._draw_knob()

    #######################################################################
    # Mouse Events
    #######################################################################

    def enableMouse(self):
        """Enable mouse events"""
        self.bind('<ButtonPress>', self._onClicked)
        self.bind('<Motion>', self._onMotion)
        self.bind('<ButtonRelease>', self._onRelease)
        
    def disableMouse(self):
        """Disables mouse events"""
        self.unbind('<ButtonPress>')
        self.unbind('<Motion>')
        self.unbind('<ButtonRelease>')

    def _mouse_update_value(self, event):
        """Mouse clicked callback"""
        xc, yc = self._xc, self._yc
        xrel = event.x_root - event.widget.winfo_rootx()
        yrel = event.y_root - event.widget.winfo_rooty()
        #Getting angle
        angle = - ( atan2(yrel - yc, xrel - xc) )
        #Normalizing interval
        min_angle, max_angle = self._get_limit_radians()
        while angle < min_angle:
            angle += 2*pi
        if angle > max_angle:
            return # invalid region
        #Getting corresponding Var value
        percent = (angle - min_angle) / (max_angle - min_angle)
        percent = 1 - percent # counterclockwise
        amplitude = self._maxvalue - self._minvalue
        self._var.set(self._minvalue + percent * amplitude)
    
    def _onClicked(self, event):
        """Mouse clicked callback"""
        self._mouse_update_value(event)
        self._motion = True
        
    def _onRelease(self, event):
        """Mouse button release callback"""
        self._motion = False
        
    def _onMotion(self, event):
        """Mouse motion callback"""
        if not self._motion:
            return
        self._mouse_update_value(event)

    #######################################################################
    # Inherited Methods
    #######################################################################

    def __setitem__(self, key, val):
        if key in self._widgetKeys:
            if key == 'number':
                self._var.set(val)
            elif key == 'numvariable':
                self._var = val
                self._var.trace('w', self._redraw)
            else:
                self.__setattr__('_' + key, val)
        else:
            Canvas.__setitem__(self, key, val)
        self._reconfigure()
        
    def __getitem__(self, key):
        if key in self._widgetKeys:
            if key == 'number':
                return self._var.get()
            elif key == 'numvariable':
                return self._var
            else:
                return self.__getattribute__('_' + key)
        else:
            return Canvas.__getitem__(self, key)
            
    def config(self, **kw):
        """Standard Tk config method"""
        for key in kw:
            if key in self._widgetKeys:
                if key == 'number':
                    self._var.set(kw[key])
                elif key == 'variable':
                    self._var = kw[key]
                    self._var.trace('w', self._redraw)
                else:
                    self[key] = kw[key]
                kw.pop(key, False)  
        Canvas.config(self, **kw)
        self._reconfigure()

if __name__ == '__main__':
    def test():
        label['text'] = gauge['number']
        root.after(50, test)

    root = Tk()
    label = Label(root)
    label.pack()
    gauge = Gauge(root)
    gauge['width'] = gauge['height'] = 200
    gauge.pack(expand=1, fill=BOTH)
    gauge.enableMouse()
    root.after(50, test)
    root.mainloop()

#!/usr/bin/env python3

from tkinter import *
from tkinter.ttk import *

'''Features:
    * xstep, ystep for grids (FIXME: Use world coords!)
    * xscale, yscale, xoffset, yoffset
    * auto scale + offset
    * paddings (top, bottom, left, right)
    * autoscroll on X axis
    * optional circle to highlight last point
Todo
    * Automatic offset (minimum value)
    * Performance issue: Shouldn't redraw everything everytime...
    * Configure number of digits in labels
    * Uniform access (plot['key'] for xoffset, yoffset, xrange, yrange)
    * Tests
    * _reconfigure
    
Tests
    * Change scale
    * Change width or height
    * Change offset
    * Change grid step
    * Change paddings
    * Change ranges
    * Change colors 
    * Change mode (autoscale, autoscroll...)  
'''

class Plot(Canvas):
    """Single-channel X-Y Plot
       
       Options (all have default values):
          - xstep --- Grid horizontal step size in world coordinates
          - ystep --- Grid vertical step size in world coordinates
          - xscale --- Screen scale factor for the horizontal axis
          - yscale --- Screen scale factor for the vertical axis
          - xoffset --- X offset (phase)
          - yoffset --- Y offset
          - padl --- Left padding (outside the plot grid)
          - padr --- Right padding (outside the plot grid)
          - padt --- Top padding  (outside the plot grid)
          - padb --- Bottom padding (outside the plot grid)
          - colorgrid --- Grid lines color
          - colorline --- Plot line color
          - autoscroll --- Whether the widget should scroll automatically on X
          - showcircle --- Whether the last point should be highlighted (circle)
          - xautorange --- Whether X-axis should be scaled to fit points extents
          - yautorange --- Whether Y-axis should be scaled to fit points extents
          - tickfont --- The font used in ticks (labels)
          - All :code:`Canvas` widget options
    """
    def __init__(self, master=None, xstep=20, ystep=20, xscale=1, yscale=1,
                 xoffset=0, yoffset=0, padl=30, padr=10, padt=10, padb=20,
                 colorgrid='#CCC', colorline='#000', autoscroll=True,
                 showcircle=True, xautorange=True, yautorange=True, 
                 xautoscale=False, yautoscale=True, tickfont='"Courier New" 6', 
                 **kw):
        self._plotkeys = { 
            'xstep': float, 'ystep': float, 'xscale': float, 'yscale': float, 
            'xoffset': float, 'yoffset': float, 'padl': int, 'padr': int, 
            'padt':int , 'padb': int, 'colorgrid': str, 'colorline': str,
            'autoscroll': bool, 'showcircle': bool, 'xautorange': bool, 
            'yautorange': bool, 'tickfont': str
        }
        Canvas.__init__(self, master, **kw)
        if 'background' not in kw:
            self['background'] = '#FFF'
        #User options
        self._xstep = xstep              #grid step X (screen coords)
        self._ystep = ystep              #grid step Y (screen coords)
        self._xscale = xscale            #multiplying factor for x
        self._yscale = yscale            #multiplying factor for y
        self._yoffset = yoffset          #offset for y
        self._xoffset = xoffset          #offset for x
        self._padl = padl                #padding left
        self._padr = padr                #padding right
        self._padt = padt                #padding top
        self._padb = padb                #padding bottom
        #Colors and fonts
        self._colorgrid = colorgrid
        self._colorline = colorline
        self._tickfont = tickfont
        #Real-time options
        self._showcircle = showcircle
        self._autoscroll = autoscroll
        self._xautorange = xautorange
        self._yautorange = yautorange
        #Points for plotting
        self._points = []                #X,Y pairs (world coords)
        #Geometry internal vars
        self.w = int(self['width'])      #width
        self.h = int(self['height'])     #height
        self._xmax = None                #maximum X world coords
        self._ymax = None                #maximum Y world coords
        self._ymin = None                #minimum Y world coords
        self._xmaxScr = self.w - self._padr #maximum X plot coords
        self._ymaxScr = self.h - self._padb #maximum Y screen coords (without bottom padding)
        #Canvas objects
        self._circleObj = None
        self._pointsObj = []     #canvas points
        self._ticksObj = []      #canvas ticks
        self._vlinesObj = []     #canvas grid vertical lines
        self._hlinesObj = []     #canvas grid horizontal lines
        self._debugObj = []
        #World <--> Screen coordinates conversion (Y-axis still inverted)
        self._xw2s = lambda x : (x - self._xoffset) * self._xscale + self._padl
        self._yw2s = lambda y : self._ymaxScr - (y + self._yoffset) * self._yscale
        self._xs2w = lambda x : (x - self._padl) / self._xscale + self._xoffset
        self._ys2w = lambda y : (self._ymaxScr - y)  / self._yscale - self._yoffset
        #Initial config
        self._draw()
        self.yview('scroll', 10, 'pages')
        self.bind('<Configure>', self.redraw)
        
    #######################################################################            
    # Inherited Methods
    #######################################################################
        
    def __setitem__(self, key, val):
        if key in self._plotkeys:
            if key == 'xoffset':
                self.setxoffset(val)
            elif key == 'yoffset':
                self.setyoffset(val)
            else:
                val = self._plotkeys[key](val)
                self.__setattr__('_' + key, val)
        else:
            Canvas.__setitem__(self, key, val)
            if key == 'width':
                self.w = int(val)
            elif key == 'height':
                self.h = int(val)
                
    def __getitem__(self, key):
        if key in self._plotkeys:
            if key =='yoffset':
                return self._ymin
            elif key == 'xoffset':
                return self._xmin
            return self.__getattribute__('_' + key)
        else:
            return Canvas.__getitem__(self, key)
            
    def config(self, **kw):
        baseKw = {}
        for key in kw:
            if key == 'xoffset':
                self.setxoffset(val)
            elif key == 'yoffset':
                self.setyoffset(val)
            elif key in self._plotkeys:
                self.__setattr__('_' + key, kw[key])    
            else:
                baseKw[key] = kw[key]
        Canvas.config(self, **baseKw)
        
        self.redraw()
        
    #######################################################################            
    # Drawing Methods
    #######################################################################
        
    def _drawGrid(self):
        """Draws grids and ticks """
        #Deleting existing entities
        for i in self._vlinesObj + self._hlinesObj + self._ticksObj:
            self.delete(i)
        self._vlinesObj.clear()
        self._hlinesObj.clear()
        self._ticksObj.clear()
        #Vertical lines and X ticks
        x = self._padl
        showTick = True
        while x <= self._xmaxScr:
            l = self.create_line(x, self._padt, x, self._ymaxScr, 
                                fill=self._colorgrid)
            self._vlinesObj.append(l)
            if showTick:
                tickX = self._xs2w(x)
                txt = str(int(round(tickX)))
                tick = self.create_text(x, self._ymaxScr + 4, 
                                        anchor='n', text=txt,
                                        font=self._tickfont)
                self._ticksObj.append(tick)
                showTick = False
            else:
                showTick = True            
            x += self._xstep * self._xscale
        #Horizontal lines and Y ticks
        y = self._ymaxScr
        while y >= self._padt:
            l = self.create_line(self._padl, y, self._xmaxScr, y, 
                                 fill=self._colorgrid)
            self._hlinesObj.append(l)
            if y != self._ymaxScr:
                tickY = self._ys2w(y)
                txt = str(int(round(tickY)))
                tick = self.create_text(self._padl - 2, y, anchor='e', text=txt,
                                        font=self._tickfont)
                self._ticksObj.append(tick)
                if self._autoscroll and self._xmaxScr > (self.w + self._padl):
                    x = self._xmaxScr - self.w + self._padl + self._padr
                    tick = self.create_text(x, y, anchor='e', text=txt,
                                            font=self._tickfont)
                    self._ticksObj.append(tick)
            y -= self._ystep * self._yscale

    def _deleteCurve(self):
        """Deletes all plot segments"""
        for i in self._pointsObj:
            self.delete(i)
        self._pointsObj.clear()
            
    def _drawPoints(self):
        """Draws the plot points"""
        self._deleteCurve()
        #Redrawing
        for i in range(1, len(self._points)):
            p1x = self._xw2s(self._points[i][0])
            p1y = self._yw2s(self._points[i][1])
            p0x = self._xw2s(self._points[i-1][0])
            p0y = self._yw2s(self._points[i-1][1])
            if p0x < self._padl or p0x > self._xmaxScr or \
               p0y > self._ymaxScr or p0y < self._padt:
                continue
            newObj = self.create_line(p0x, p0y, p1x, p1y, fill=self._colorline)
            if self._circleObj:
                self.delete(self._circleObj)
            if self._showcircle and i == len(self._points) - 1:
                self._circleObj = self.create_oval(p1x-4, p1y-4, p1x+4, p1y+4, 
                                                  fill=self._colorline)
            self._pointsObj.append(newObj)

    def _draw(self):
        """Draws the plot objects"""
        self._drawGrid()
        self._drawPoints()
        
    #######################################################################
    # Public API
    #######################################################################

    def addPoint(self, point, limit=0):
        """Adds a new point (x-y tuple) to the plot number (redraw is NOT triggered)"""
        self._points.append(point)
        if limit > 0 and len(self._points) > limit:

            self._points = self._points[-limit:] #"limit" last points
            
        if self._yautorange:
            if not self._ymax:
                self._ymax = point[1]
                self._ymin = point[1]
            elif (point[1] > self._ymax) and (point[1] < 1e9):
                self._ymax = point[1]
            elif (point[1] < self._ymin) and (point[1] > -1e9):
                self._ymin = point[1]
        if self._xautorange:
            if not self._xmax:
                self._xmax = point[0]
                self._xmin = point[0]
            elif (point[0] > self._xmax) and (point[0] < 1e9):
                self._xmax = point[0]
            elif (point[0] < self._xmin) and (point[0] > -1e9):
                self._xmin = point[0] 
                
    def clear(self):
        """Clears the plot"""
        self._points.clear()
        self.redraw()

    def redraw(self, *args):
        """Forces a redraw"""
        #Debug
        for o in self._debugObj:
            self.delete(o)
        l = self.create_line(self._xmaxScr, 0, self._xmaxScr, self.h, fill='red')
        self._debugObj.append(l)
        
        if self._xmax:
            self._xmaxScr = self._xw2s(self._xmax)
        if self._ymax and self._yautorange:
            self._ymaxScr = self._padt + (self._ymax - self._ymin) * self._yscale
        if self._ymin:
            self._yoffset = -self._ymin
        limitY = self._ymaxScr + self._padb
        self['scrollregion'] = (0, 0, self._xmaxScr + self._padr, limitY)
        self._draw()
        if self._autoscroll and self._xmaxScr > self.w:
            self.xview('scroll', 1, 'pages')
    
    def setxrange(self, xmin, xmax):
        """Sets X range"""
        self._xscale = (self.w - self._padl - self._padr) / (xmax - xmin)
        self._xmin = xmin
        self._xmax = xmax
        self._xoffset = xmin
        
    def setyrange(self, ymin, ymax):
        """Sets Y range"""
        self._yscale = (self.h - self._padt - self._padb) / (ymax - ymin)
        self._ymin = ymin
        self._ymax = ymax
        self._yoffset = -ymin
    
    def setyoffset(self, yoffset):
        """Offsets Y axis without changing scale"""
        yoffset = float(yoffset)
        self._ymin = yoffset
        self._yoffset = -self._ymin
        
    def setxoffset(self, xoffset):
        """Offsets X axis without changing scale"""
        xoffset = float(xoffset)
        self._xmin = xoffset
        self._xoffset = self._xmin

            
if __name__ == '__main__':
    from math import sin, pi, tan
    
    i = 0
    
    def toggleAutoScroll():
        plot['autoscroll'] = not plot['autoscroll']
    
    def test():
        global i
        plot.addPoint([i, 100 * sin(float(i)*pi/180) + 50], limit=1000)
        i += 1
        plot.redraw()
        if i < 5000:
            root.after(10, test)
            
    def test2():
        for i in range(-180, 1280):
            plot.addPoint([i, 100 * sin(float(i)*pi/180) + 50], limit=1000)
        plot.redraw()      
    
    root = Tk()
    plot = Plot(root, width=360, height=230, autoscroll=True, xautorange=True, 
                yautorange=False, yscale=1.0, xscale=0.5, ystep=30, xstep=30)
    hscroll = Scrollbar(root, orient='horizontal')
    hscroll.config(command=plot.xview)
    vscroll = Scrollbar(root, orient='vertical')
    vscroll.config(command=plot.yview)
    plot.config(xscrollcommand=hscroll.set)
    plot.config(yscrollcommand=vscroll.set)
    plot['background'] = '#FFF'
    plot.setyoffset(-70)
    plot['yscale'] = 0.5
    plot.setxoffset(0)
    button = Button(root, text='Automatic scrolling')
    button['command'] = toggleAutoScroll
    button.grid(row=2, column=0, columnspan=2)
    
    plot.redraw()
    vscroll.grid(row=0, column=0, sticky='ns')
    plot.grid(row=0, column=1, sticky='nsew')
    hscroll.grid(row=1, column=1, sticky='we')
    root.after(10, test)
    root.mainloop()

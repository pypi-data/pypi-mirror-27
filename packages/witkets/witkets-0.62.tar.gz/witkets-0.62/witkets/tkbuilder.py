#!/usr/bin/env python3

import sys
import ast
import xml.etree.ElementTree as ET
from tkinter import *
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText
from copy import copy
from witkets import Theme
from witkets import AccelLabel, ColorButton
from witkets import Expander, FileChooserEntry
from witkets import Gauge, ImageButton, ImageMap
from witkets import LED, LEDBar
from witkets import LinkButton, LogicSwitch
from witkets import NumericLabel 
from witkets import Plot, Scope
from witkets import PyText, PyScrolledText
from witkets import Ribbon
from witkets import Spinner, Spin
from witkets import Tank, Thermometer
from witkets import TimeEntry, Toolbar
from witkets import ToggleButton

_widget_classes = [
    #TK Base and TTK Overriden Widgets
    Button, Canvas, Checkbutton, Entry, Frame, Label, LabelFrame, 
    Listbox, Menu, Menubutton, Radiobutton, Scale, Scrollbar, 
    ScrolledText, Spinbox, Text,
    #TTK Exclusive
    Combobox, Notebook, Progressbar, Separator, Sizegrip, Treeview,
    #Witkets
    AccelLabel, ColorButton, Expander, FileChooserEntry, Gauge,
    ImageButton, ImageMap, LED, LEDBar, LinkButton, LogicSwitch,
    NumericLabel, Plot, Scope, PyText, PyScrolledText, Ribbon,
    Spinner, Spin, Tank, Thermometer, TimeEntry, Toolbar, ToggleButton
]

tag2tk = { cls.__name__.lower(): cls for cls in _widget_classes }

containers = [ 'root', 'frame', 'labelframe' ]

_specialHandlers = {
    'pack': {
        'padx': ast.literal_eval,
        'pady': ast.literal_eval,
        'expand': ast.literal_eval
    },
    'grid': {
        'padx': ast.literal_eval,
        'pady': ast.literal_eval
    }
}

class TkBuilder:
    def __init__(self, master):
        """Initializer
        
            :param master:
                Tk root where interface is going to be built
        """
        self._tree = None
        self._root = None
        self._master = master
        #if not hasattr(self._master, 'properties'):
        #    self._master.properties = []
        self.nodes = {}
        self.tkstyle = None
        self.theme = None

    def addTag(self, tag, cls, container=False):
        """Maps a tag to a class
        
            :param tag:
                XML tag name
            :type tag:
                str
            :param cls:
                Class to be instantiated when *tag* is found
            :type cls:
                Any subclass of tkinter.Widget
            :param container:
                Whether this Tk widget is a container to other widgets
        """
        tag2tk[tag] = cls
        if container:
            containers.append(tag)
        
    def _handleWidget(self, widgetNode, parent):
        """Handles individual widgets tags"""
        try:
            wid = widgetNode.attrib.pop('wid')
        except KeyError:
            print('Required key "wid" not found in %s' % widgetNode.tag, sys.stderr)
            return
        # Creating widget        
        tkClass = tag2tk[widgetNode.tag]
        if parent == self._root:
            parentNode = self._master
        else:
            parentWid = parent.attrib['wid']
            parentNode = self.nodes[parentWid]        
        self.nodes[wid] = tkClass(parentNode)
        # Mapping attributes
        self._handleAttributes(self.nodes[wid], widgetNode.tag, widgetNode.attrib)
    
    def _handleAttributes(self, widget, tagname, attribs):
        """Handles attributes, except TkBuilder related"""
        attribs = self._getAttribsValues(tagname, attribs)
        for key,val in attribs.items():            
            if key.startswith('{editor}'): #skipping editor namespace
                continue
            try:
                widget[key] = val #@FIXME fails for Bool
            except KeyError:
                print('[warning] Invalid key "%s"' % key)

    def _getAttribsValues(self, tagname, attribs):
        # use types!!
        if tagname not in _specialHandlers:
            return attribs
        handlers = _specialHandlers[tagname]
        for a in attribs:
            if a in handlers:
                attribs[a] = handlers[a](attribs[a])
        return attribs
        
    def _handleContainer(self, container, parent):
        """Handles containers (<root>, <frame> and user-defined containers)"""
        if container != self._root:    
            try:
                attribs = copy(container.attrib)
                wid = attribs.pop('wid')
                tkClass = tag2tk[container.tag]
                if parent != self._root:
                    parentWid = parent.attrib['wid']
                    parentNode = self.nodes['wid']
                else:
                    parentNode = self._master
                self.nodes[wid] = tkClass(parentNode)
                self._handleAttributes(self.nodes[wid], container.tag, attribs)
            except KeyError:
                print('Required key "wid" not found in %s' % container.tag, sys.stderr)
                return
        for child in container:
            if child.tag in containers:
                self._handleContainer(child, container)
            elif child.tag == 'geometry':
                self.currParent = container
                self._handleGeometry(child)
            elif child.tag == 'style':
                self._handleStylesheet(child)
            elif child.tag in tag2tk.keys():
                self._handleWidget(child, container)
            else:
                print('Invalid tag: %s!' % child.tag, sys.stderr)
        if container == self._root:
            attribs = container.attrib
            self._handleAttributes(self._master, 'root', attribs)
        
    def _handleGeometry(self, geometry):
        """Handles the special <geometry> tag"""
        for child in geometry:
            attribs = copy(child.attrib)
            if child.tag in ('pack', 'grid', 'place'):
                # Getting widget ID
                try:
                    wid = attribs.pop('for')
                except KeyError:
                    #@TODO emit error
                    print('[geom] Required key "for" not found in %s' % child.tag, sys.stderr)
                    continue
                # Calling appropriate geometry method
                # FIXME add support for padx and pady tuples  
                if wid not in self.nodes:
                    print(self.nodes)
                attribs = self._getAttribsValues(child.tag, attribs)
                if child.tag == 'pack':
                    self.nodes[wid].pack(**attribs)
                elif child.tag == 'grid':
                    self.nodes[wid].grid(**attribs)
                elif child.tag == 'place':
                    self.nodes[wid].place(**attribs)
            else:
                print('Invalid geometry instruction %s' % child.tag, sys.stderr)    
                #@TODO emit error
                continue
                
    def _handleStylesheet(self, style):
        """Handles the special <style> tag"""
        self.tkstyle = Style()
        self.theme = Theme(self.tkstyle)
        if 'defaultfonts' in style.attrib and \
            style.attrib['defaultfonts'] != '0':
            self.theme.setDefaultFonts()
        if 'fromfile' in style.attrib:
            self.theme.applyFromFile(style.attrib['fromfile'])
        else:
            self.theme.applyFromString(style.text)

    def _parseTree(self):
        """Parses XML and builds interface"""
        if self._root.tag != 'root':
            msg = 'Invalid root tag! Expecting "root", but found %s'
            print(msg % self._root.tag, sys.stderr)
            return False
        self._handleContainer(self._root, self._master)
        return True

    def buildFile(self, filepath):
        """Build user interface from XML file"""
        self._tree = ET.parse(filepath)
        self._root = self._tree.getroot()
        self._parseTree()

    def buildString(self, contents):
        """Build user interface from XML string"""
        self._root = ET.fromstring(contents)
        self._parseTree()
    
if __name__ == '__main__':
    example = '''
        <root>
            <style defaultfonts="1">
                [SpockLabel.TLabel]
                    foreground=#088
                    background=#000
            </style>
            <label wid="lbl1" text="Cap. Kirk" background="red" />
            <frame wid="frm1">
                <label wid="lbl2" text="Bones" width="30" />
                <label wid="lbl3" text="Spock" style="SpockLabel.TLabel" />
                <geometry>
                    <grid for="lbl2" row="0" column="0" sticky="w" />
                    <grid for="lbl3" row="0" column="2" sticky="e"/>
                </geometry>
            </frame>
            <geometry>
                <pack for="lbl1" fill="y" expand="1" />
                <pack for="frm1" />
            </geometry>
        </root>
'''

    root = Tk()
    builder = TkBuilder(root)
    builder.buildString(example)
    root.mainloop()

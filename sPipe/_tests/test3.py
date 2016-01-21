#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os
import cmd

#from PyQt4 import QtCore, QtGui
from PySide import QtCore, QtGui


class fileBrowserUI(QtGui.QWidget):
  
    def __init__(self):
        super(fileBrowserUI, self).__init__()
        self.initUI()
        
    def initUI(self):
        # Create all widgets
        w = QtGui.QVBoxLayout(self)
        self.setLayout(w)
        
        print QtGui.qApp.allWidgets()

def main():
  
    app = QtGui.QApplication([])
    ex = fileBrowserUI()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()  
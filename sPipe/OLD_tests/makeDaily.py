#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os
import cmd
if not '/usr/local/lib/python2.7/site-packages' in sys.path:
    sys.path.append('/usr/local/lib/python2.7/site-packages')
    
    
#from PyQt4 import QtCore, QtGui
from PySide import QtCore, QtGui


class fileBrowserUI(QtGui.QWidget):
  
    def __init__(self):
        super(fileBrowserUI, self).__init__()
        self.initUI()
        
    def initUI(self):
        # Create all widgets
        
        self.pathLabel = QtGui.QLabel("Path :")
        self.pathField = QtGui.QLineEdit()
        self.pathButton = QtGui.QPushButton("Browse")
        
        self.sequenceLabel = QtGui.QLabel("Sequence :")
        self.sequenceBox = QtGui.QComboBox()
        self.sequenceBox.currentIndexChanged.connect(self.updateShot)
        
        self.shotLabel = QtGui.QLabel("Shot :")
        self.shotBox = QtGui.QComboBox()
        
        self.lutLabel = QtGui.QLabel("LUT :")
        self.lutBox = QtGui.QComboBox()
        
        self.frameRangeLabel = QtGui.QLabel("FrameRange :")
        self.startFrameRangeField = QtGui.QLineEdit()
        self.endFrameRangeField = QtGui.QLineEdit()
        
        self.elementLabel = QtGui.QLabel("Element :")
        self.elementField = QtGui.QLineEdit()
        
        self.commentLabel = QtGui.QLabel("Comment")
        self.commentField = QtGui.QTextEdit()
        
        self.newFolderButton = QtGui.QPushButton("New Folder")
        
        self.dailyButton = QtGui.QPushButton("Daily")
        self.cancelButton = QtGui.QPushButton("Cancel")
        self.cancelButton.clicked.connect(QtCore.QCoreApplication.instance().quit)

        
        # Place widget in the layout
        self.gridLayout = QtGui.QGridLayout(self)
        self.gridLayout.setSpacing(10)

        self.gridLayout.addWidget(self.pathLabel,0,0)
        self.gridLayout.addWidget(self.pathField,0,1)
        self.gridLayout.addWidget(self.pathButton,0,2)

        self.gridLayout.addWidget(self.sequenceLabel,1,0)
        self.gridLayout.addWidget(self.sequenceBox,1,1,1,2)
        
        self.gridLayout.addWidget(self.shotLabel,2,0)
        self.gridLayout.addWidget(self.shotBox,2,1,1,2)
        
        self.gridLayout.addWidget(self.lutLabel,3,0)
        self.gridLayout.addWidget(self.lutBox,3,1,1,2)
        
        self.gridLayout.addWidget(self.frameRangeLabel,4,0)
        self.gridLayout.addWidget(self.startFrameRangeField,4,1)
        self.gridLayout.addWidget(self.endFrameRangeField,4,2)
        
        self.gridLayout.addWidget(self.elementLabel,5,0)
        self.gridLayout.addWidget(self.elementField,5,1,1,2)
        
        self.gridLayout.addWidget(self.commentLabel,6,0)
        self.gridLayout.addWidget(self.commentField,6,1,1,2)
        
        self.gridLayout.addWidget(self.cancelButton,7,1)
        self.gridLayout.addWidget(self.dailyButton,7,2)
        
        self.getSequence()
        self.getLut()
        
        # Display windows
        self.setWindowTitle('Make Daily')
        self.setGeometry(300, 300, 500, 400)
        self.show()
    
    def getSequence(self):
        sequenceList = ["BB","FR","NC"]
        for sq in sequenceList:
            self.sequenceBox.addItem(sq)
    
    def getLut(self):
        lutList = ["none","linear","sRGB"]
        for lut in lutList:
            self.lutBox.addItem(lut)
    
    def updateShot(self, arg):
        shotList = ["BB0100","BB0200","FR0240","NC1010","NC2020","GB0200"]
        sq = self.sequenceBox.currentText()
        
        self.shotBox.clear()
        for sh in shotList:
            if sq in sh:
                self.shotBox.addItem(sh)
    
        

def main():
  
    app = QtGui.QApplication([])
    ex = fileBrowserUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()  
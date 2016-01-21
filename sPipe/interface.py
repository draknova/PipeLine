import math
import sys
import os

from PySide import QtCore, QtGui

from sPipe import nodeDef, panel
import pCore as pc

class ParameterPanel(QtGui.QWidget):
    def __init__(self):
        super(ParameterPanel,self).__init__()
        self.initUI()
    
    def initUI(self):
        self._mainMenu = MainMenu(self)
        
        self._layout = QtGui.QGridLayout()
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)
        self._layout.setSpacing(0)
        
        self._toolBar = QPanelToolBar()
        
        
        self._layout.addWidget(self._toolBar,1,0,1,1)
        self._layout.addWidget(self._mainMenu,0,0,1,2)
        
        #pan = QSplittedPanel()
        #pan = panel.JobPanel.JobPanel()
        pan = panel.NodePanel.NodePanel()
        self._layout.addWidget(pan,1,1)


class MainMenu(QtGui.QMenuBar):
    def __init__(self,parent=None):
        super(MainMenu,self).__init__(parent)    
        
        self.setNativeMenuBar(False)
        self.setFixedHeight(24)

        self._home = self.addMenu("Home")
        self._project = self.addMenu("Project")
        self._windows = self.addMenu("Windows")
        self._help = self.addMenu("Help")
        
        self._home.addAction("Home Screen")
        self._home.addAction("Show")
        self._home.addAction("Render")
        self._home.addAction("Daily")
        self._home.addAction("Review")
        
        self._project.addAction("Monster Trucks")
        self._project.addAction("Sputnik")
        self._project.addAction("Monster Trucks")
        self._project.addAction("Monster Trucks")
        
        self._windows.addAction("Node Editor")
        self._windows.addAction("Render Manager")
        self._windows.addAction("Console")
        self._windows.addAction("Script Editor")
        
        
        w = QtGui.QWidget()
        w.show()
        
        self._cornerWidget = QtGui.QWidget()
        self._cornerWidgetLayout = QtGui.QHBoxLayout()
        self._cornerWidget.setLayout(self._cornerWidgetLayout)
        self._cornerWidgetLayout.setContentsMargins(1,1,1,1)
        button = QtGui.QLineEdit("Search")
        self._cornerWidgetLayout.addWidget(button)
        
        self.setCornerWidget(self._cornerWidget,QtCore.Qt.TopRightCorner)
            

class QSplittedPanel(QtGui.QSplitter):
    def __init__(self):
        super(QSplittedPanel, self).__init__()
        
        node = panel.NodePanel.NodePanel()
        console = panel.ConsolePanel.ConsolePanel()
        
        pan1 = QPanel([node,console])
        pan2 = panel.ConsolePanel.ConsolePanel()
        self.addWidget(pan1)
        self.addWidget(pan2)
        
        self.setSizes([500,150])


class QPanel(QtGui.QWidget):
    def __init__(self,widgets=None):
        super(QPanel,self).__init__()
        self.setAcceptDrops(True)
        
        self._tabBar = None
        self._widgets = list()
        
        self.initUI()
        
        # Add widget a creation
        if widgets != None:
            for i,w in enumerate(widgets):
                #self.addPanel(w, ("Tab %i"%(i)), i)
                pass
        
        else:
            i = panel.NodePanel.NodePanel()
            j = QtGui.QTextEdit("Tab 2")
            #self.addPanel(i, "Node Editor", 0)
            #self.addPanel(j, "Tab", 1)
            pass
        
        # Set to first tab
        #self.setCurrentTab(0)
        pass
        
    def initUI(self):
        self._layout = QtGui.QGridLayout()
        self.setLayout(self._layout)
        self._layout.setContentsMargins(5,5,5,5)
        self._layout.setSpacing(0)

        self._tabBar = QPanelTabBar()
        
        _mainWidget = QtGui.QTextEdit()
        
        self._layout.addWidget(self._tabBar,0,0)
        self._layout.addWidget(_mainWidget,1,0,1,4)

    def addPanel(self, widget, tabName="New Tab", index=None):        
        i = self._tabBar.count() - 1
        if index != None:
            if index < i:
                i = index
        
        if i < 0:
            i = 0   
             
        self._tabBar.insertTab(i,tabName)
        self._widgets.insert(i, widget)
        self._layout.addWidget(widget,1,0,1,4)
        self.setCurrentTab(i)
    
    def deleteTab(self, index):
        if self._tabBar.currentIndex >= index:
            self.setCurrentTab(index-1)
        self._tabBar.removeTab(index)
        w = self._widgets.pop(index)
        self._layout.removeWidget(w)
        
        if index == 0:
            self.setCurrentTab(0)
        
    
    def setCurrentTab(self,id):
        self._tabBar.setCurrentIndex(id)
        for item in self._widgets:
            item.hide()
        self._widgets[id].show()


    def dragEnterEvent(self, e):
        print e
    
    def dropEvent(self, e):
        print e


class QPanelTabBar(QtGui.QFrame):
    def __init__(self):
        super(QPanelTabBar,self).__init__()

        
        self.initUI()
    
    def initUI(self):
        self._layout = QtGui.QHBoxLayout()
        self.setLayout(self._layout)
        self._layout.setContentsMargins(10,0,10,10)
        self._layout.setSpacing(5)
        
        self._tabs = QtGui.QTabBar()
        #self._tabs.setTabsClosable(True)
        self._tabs.addTab("Tab1")
        self._tabs.addTab("Tab2")
        self._tabs.addTab("Tab3")
        
        icnPath = "/Users/draknova/Documents/workspace/sPipe/bin/images/icons"
        addIcone = QtGui.QIcon(QtGui.QPixmap("%s/add.png"%(icnPath)))
        panelIcone = QtGui.QIcon(QtGui.QPixmap("%s/list.png"%(icnPath)))
        
        self._addButton = QtGui.QPushButton(addIcone,"")
        
        self._panelButton = QtGui.QPushButton(panelIcone,"")
        
        self._layout.addWidget(self._tabs)
        self._layout.addWidget(self._addButton)
        self._layout.addStretch()
        self._layout.addWidget(self._panelButton)
        
        
        
        
        
class QQPanelTabBar(QtGui.QTabBar):
    def __init__(self):
        super(QPanelTabBar,self).__init__()
        self.setMovable(False)
        self.setTabsClosable(True)
        self.setUsesScrollButtons(True)
        self.setExpanding(True)
        
        self.setFixedHeight(20)
        
        self.currentChanged.connect(self.changeTab)
        self.tabCloseRequested.connect(self.deleteTab)

        self.initUI()
    
    def initUI(self):
        add = self.addTab("+")
        addTabWidget = self.tabButton(add,QtGui.QTabBar.LeftSide)
        addTabWidget.hide()
        print self.tabSizeHint(add)

    def changeTab(self, index):
        if index == self.count()-1:
            if self.parent() != None:
                t = QtGui.QTextEdit("New Tab")
                self.parent().addPanel(t,"New Tab")
        if self.parent() != None:
            self.parent().setCurrentTab(index)
    
    def deleteTab(self, index):
        if self.parent() != None:
            self.parent().deleteTab(index)    

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.changeTab( self.tabAt(event.pos()) )
        elif event.button() == QtCore.Qt.RightButton:
            print "Pop Menu"


class QPanelToolBar(QtGui.QWidget):
    def __init__(self):
        super(QPanelToolBar,self).__init__()
        
        self.setFixedWidth(40) 
        
        self.initUI()
    
    def initUI(self):
        l = QtGui.QVBoxLayout(self)
        l.setContentsMargins(0,0,0,0)
        w = QtGui.QFrame(self)
        l.addWidget(w)
        
        self._layout = QtGui.QVBoxLayout()
        #self.setLayout(self._layout)
        w.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)
        
        icnPath = "/Users/draknova/Documents/workspace/sPipe/bin/images/icons/"
        
        icn1 = QtGui.QIcon(QtGui.QPixmap("%s/home.png"%(icnPath)))
        icn2 = QtGui.QIcon(QtGui.QPixmap("%s/server.png"%(icnPath)))
        icn3 = QtGui.QIcon(QtGui.QPixmap("%s/database.png"%(icnPath)))
        icn4 = QtGui.QIcon(QtGui.QPixmap("%s/network.png"%(icnPath)))
        icn5 = QtGui.QIcon(QtGui.QPixmap("%s/settings.png"%(icnPath)))
        b1 = QtGui.QPushButton(icn1,"")
        b2 = QtGui.QPushButton(icn2,"")
        b3 = QtGui.QPushButton(icn3,"")
        b4 = QtGui.QPushButton(icn4,"")
        b5 = QtGui.QPushButton(icn5,"")
        
        
        self._layout.addWidget(b1)
        self._layout.addWidget(b2)
        self._layout.addWidget(b3)
        self._layout.addWidget(b4)
        self._layout.addWidget(b5)
        self._layout.addStretch()

def main():
    app = QtGui.QApplication([])
    ui = ParameterPanel()
    f = open(pc.CSSPATH,"r")
    s = f.read()
    f.close()
    app.setStyleSheet(s)
    
    
    ui.setGeometry(0,0,800,800)
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
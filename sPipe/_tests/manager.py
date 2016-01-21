#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, time, math
import SocketServer, socket
import sqlite3
import cmd
from Finder.Finder_items import item
if not '/usr/local/lib/python2.7/site-packages' in sys.path:
    sys.path.append('/usr/local/lib/python2.7/site-packages')
    
    
#from PyQt4 import QtCore, QtGui
from PySide import QtCore, QtGui

from bin.Panel.NodePanel import *
import nodeDef


class sRenderManagerUI(QtGui.QMainWindow):
    def __init__(self):
        super(sRenderManagerUI, self).__init__()
        self.server = None
        
        self.database = "/Users/draknova/Desktop/database.db"
        
        self.start()

        
    def start(self):
        # Place widget in the layout
        self.generateMenu()

        self.mainWidget = QtGui.QWidget()
        self.mainWidget.setContentsMargins(0,0,0,0)
        self.setCentralWidget(self.mainWidget) 
        
        self.status = QtGui.QStatusBar()
        self.setStatusBar(self.status)
        
        # Define MainWidget Layout
        self.mainLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom,None)
        self.mainLayout.setSpacing(0)
        self.setLayout(self.mainLayout)
        
        
        # Create MainWidget Content
        self.generateShelveBar()

        self.sideSplitter = QtGui.QSplitter()
        self.sideSplitter.setOrientation(QtCore.Qt.Horizontal)

        self.mainSplitter = QtGui.QSplitter()
        self.mainSplitter.setOrientation(QtCore.Qt.Vertical)


        # Generate List
        self.jobList = JobList("jobs")
        self.taskList = JobList("tasks")
        self.jobList.refreshList()
        self.jobList.connectToList(self.taskList)

        #self.console = Console()
        #self.console.output("Test\nBlablabla")
        
        self.console = Console()
        self.nodePanel = NodePanel()
        self.parmPanel = ParameterPanel()
        
        tabArea1 = TabPanel()
        tabArea1.addTab(self.jobList,"Job List")
        tabArea1.addTab(self.taskList,"Task List")
        tabArea2 = TabPanel()
        tabArea2.addTab(self.nodePanel,"Node")
        tabArea2.addTab(self.console,"Console")
        tabArea3 = TabPanel()
        tabArea3.addTab(self.parmPanel,"Parameters")

        self.nodePanel.connectParameterPanel(self.parmPanel)
        
        
        # Asign Layout
        self.centralWidget().setLayout(self.mainLayout)
        
        self.mainLayout.addWidget(self.shelveBar)
        self.mainLayout.addWidget(self.sideSplitter)
        #self.mainSplitter.addWidget(self.jobList)
        #self.mainSplitter.addWidget(self.console)
        self.mainSplitter.addWidget(tabArea1)
        self.mainSplitter.addWidget(tabArea2)
        self.sideSplitter.addWidget(self.mainSplitter)
        self.sideSplitter.addWidget(tabArea3)
        
        
        self.setWindowTitle('sRender Manager')
        self.setGeometry(30, 30, 1200, 800)
        self.show()
        



 
    def generateMenu(self):
        self.menuBar = self.menuBar()
        self.menuBar.setNativeMenuBar(False)
        connectionMenu = self.menuBar.addMenu("&Connection")
        connectionMenu.addAction("Connect")
        connectionMenu.addAction("Disconnect")
        connectionMenu.addAction("Edit")
        
        quitAction = connectionMenu.addAction("Quit")
        connectionMenu.insertSeparator(quitAction)
        
        jobMenu = self.menuBar.addMenu("&Job")
        jobMenu.addAction("Create job")
        jobMenu.addAction("Edit job")
        jobMenu.addAction("Delete job")
        taskMenu = self.menuBar.addMenu("&Task")
        taskMenu.addAction("Create task")
        taskMenu.addAction("Edit task")
        taskMenu.addAction("Delete task")
        aboutMenu = self.menuBar.addMenu("&About")
        
        return
 
    def generateShelveBar(self):
        self.shelveBar = QtGui.QWidget()
        self.shelveBar.setFixedHeight(50)
        
        shelveBarLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight,self.shelveBar)
        shelveBarLayout.setSpacing(10)
        shelveBarLayout.setContentsMargins(0,0,0,0)

        hostLabel = QtGui.QLabel()
        hostLabel.setText("Host :")
        self.hostField = QtGui.QLineEdit()
        self.hostField.setText("127.0.0.1")
        self.hostField.setFixedWidth(120)
        
        portLabel = QtGui.QLabel()
        portLabel.setText("Port :")
        self.portField = QtGui.QLineEdit()
        self.portField.setText("9999")
        self.portField.setFixedWidth(80)
        
        self.connectButton = QtGui.QPushButton("Connect")
        self.connectButton.setFixedWidth(100)
        self.connectButton.clicked.connect(self.connectToServer)
        

        self.shelveBar.setLayout(shelveBarLayout)
        shelveBarLayout.addWidget(hostLabel)
        shelveBarLayout.addWidget(self.hostField)
        shelveBarLayout.addWidget(portLabel)
        shelveBarLayout.addWidget(self.portField)
        shelveBarLayout.addWidget(self.connectButton)
        shelveBarLayout.addStretch()
    
    
    def connectToServer(self):
        host = self.hostField.text()
        port = int(self.portField.text())
        
        print host
        print port
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.s.connect( (host, port) )
            self.console.output("Connection success")
            self.s.sendall("/jobList")
        
            data = self.s.recv(1024)
            print data
            self.s.close()
            
        except:
            self.console.warning("Connection failed !")    

  
class TabPanel(QtGui.QTabWidget):
    def __init__(self):
        super(TabPanel,self).__init__()
        self.setMovable(True)
        self.setTabsClosable(True)
        

class JobList(QtGui.QTreeWidget):
    def __init__(self, listType):
        super(JobList, self).__init__()
        self.setSortingEnabled(True)

        self.database = "/Users/draknova/Desktop/database.db"
        self.listType = listType

        self.generateList()
        self.connectedList = None
 
    
    def connectToList(self, listToConnect):
        self.connectedList=listToConnect


    def generateList(self):
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row
        header = conn.execute("SELECT * FROM %s"%(self.listType)).fetchone()
        
        listHeader = self.headerItem()   
        listHeader.setText(0,"id") 
        self.sortByColumn(0,QtCore.Qt.AscendingOrder)
        i=1
        for item in header.keys():
            if item in ["name", "user", "status"]:
                listHeader.setText(i,item)
                i+=1


    def refreshList(self, dbFilter=None):
        self.clear()
        listHeader = self.headerItem()

        data = "rowid,"
        for i in range(1,listHeader.columnCount()):
            data += listHeader.text(i)
            if i<listHeader.columnCount()-1:
                data += ","

        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row
        if dbFilter == None:
            jobList = conn.execute("SELECT %s FROM %s"%(data,self.listType)).fetchall()
        else:
            jobList = conn.execute("SELECT %s FROM %s WHERE %s"%(data,self.listType,dbFilter)).fetchall()
        
        for item in jobList:
            t = QtGui.QTreeWidgetItem(self)
            for i,h in enumerate(jobList[0].keys()):
                try:
                    t.setText(i,str(item[h]))
                except:
                    pass
    
    
    def mousePressEvent(self,event):
        pos = event.pos()
        selectedItem = self.itemAt(pos)
        
        for item in self.selectedItems():
            item.setSelected(False)
        
        if type(selectedItem) == QtGui.QTreeWidgetItem:
            selectedItem.setSelected(True)
        
        if event.button() == QtCore.Qt.RightButton:
            pos = QtGui.QCursor.pos()
            menu = QtGui.QMenu("Jobs")
            menu.addAction("Open")
            menu.addAction("Properties")
            menu.addSeparator()
            menu.addAction("Restart")
            menu.addAction("Stop")
            menu.addAction("Kill")
            menu.addSeparator()
            menu.addAction("Restart all error tasks")
            menu.addAction("Kill all running tasks")
            menu.addSeparator()
            menu.addAction("Delete")
            menu.exec_(pos)
        
        else:
            
            if self.listType == "jobs":
                if type(selectedItem) == QtGui.QTreeWidgetItem:
                    conn = sqlite3.connect(self.database)
                    h = conn.execute("SELECT tasks FROM jobs WHERE rowid=%s"%(selectedItem.text(0))).fetchone()
                    conn.close()
                    dbFilter = ("rowid IN %s"%(h[0])).replace("[","(").replace("]",")")
                    
                    self.connectedList.refreshList(dbFilter)
                else:
                    self.connectedList.refreshList("rowid=-1")



class Console(QtGui.QWidget):
    def __init__(self):
        super(Console, self).__init__()
        self.initUI()

    def initUI(self):
        self.setMinimumSize(50,100)

        self.menu = QtGui.QMenuBar()
        self.menu.addMenu("Test")
    
        self.layout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom,None)
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,0)
        
        
        self.console = QtGui.QTextEdit()
        self.console.setReadOnly(True)
        
        self.layout.addWidget(self.menu)
        self.layout.addWidget(self.console)
    
    def output(self, text):
        self.console.append(time.strftime("[%H:%M:%S] ", time.localtime()) +text) 
    
    def warning(self, text):
        self.console.append(time.strftime("[%H:%M:%S] ", time.localtime()) +text) 


class ParameterPanel(QtGui.QWidget):
    def __init__(self):
        super(ParameterPanel,self).__init__()
        self.parameterType="system"
        self.autorizedParameterType = list()   
        
        self.layout=None
        self.parameterWidget=None
        
        self.regenerateParameterType()
        
        self.initUI()
    
    def initUI(self):
        self.layout = QtGui.QFormLayout()
        self.setLayout(self.layout)

        self.reloadParameter()
    
    def reloadParameter(self):
        if self.parameterWidget != None:
            self.layout.removeWidget(self.parameterWidget)
            self.parameterWidget.close()
        
        if self.parameterType != None:
            self.parameterWidget = eval("nodeDef.%s.ParameterUI()"%(self.parameterType))
            self.layout.addWidget(self.parameterWidget)
        
    def setParameterType(self,type_):
        if type_ in self.autorizedParameterType:
            self.parameterType = type_   
            self.reloadParameter()
        
        

    def regenerateParameterType(self):
        self.autorizedParameterType = list()     
        
        path = os.getcwd()+"/nodeDef"
        for item in os.listdir(path):
            if item != "__init__.py" and not ".pyc" in item:
                self.autorizedParameterType.append(item[:-3])
        
        print self.autorizedParameterType
        content = "" 
        for item in self.autorizedParameterType:
            content += ("from %s import *\n"%(item))
            
        f = open(path+"/__init__.py","w")
        f.write(content)
        f.close()
        
        reload(nodeDef)
    
def main():
    app = QtGui.QApplication([])
    #style = QtGui.QStyle()
    #style = QtGui.QPlastiqueStyle()
    #app.setStyle(style)
    #f = open("style.css","r")
    #s = f.read()
    #f.close()
    #app.setStyleSheet(s)
    ui = sRenderManagerUI()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
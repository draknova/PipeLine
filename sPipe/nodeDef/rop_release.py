import os, sys
from PySide import QtCore, QtGui

class ParameterUI(QtGui.QWidget):
    def __init__(self):
        super(ParameterUI,self).__init__()
        self.initUI()      
        
    
    def initUI(self):
        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,0)
        
        self.releaseTypeLabel = QtGui.QLabel("Release Type :")
        self.releaseType = QtGui.QComboBox()
        self.releaseType.addItems(["2D","3D"])
        self.releaseType.currentIndexChanged.connect(self.currentIndexChanged)
        
        self.layout.addWidget(self.releaseTypeLabel,1,0)
        self.layout.addWidget(self.releaseType,1,2,1,2)
        
        
        a = QtGui.QListWidget()
        b = QtGui.QListWidget()
        
        self.elementForm()
        
        self.tab = QtGui.QTabWidget()
        self.tab.addTab(self.elementFormWidget,"Element")
        self.tab.addTab(b,"Email")
        #gesw = self.generateElementSelectionWidget()
        self.layout.addWidget(self.tab,2,0,10,4)
        
        self.elementFormLayout.addWidget(self.backButton,11,2)
        self.elementFormLayout.addWidget(self.nextButton,11,3)  
    
    
    def elementForm(self):
        self.elementFormWidget = QtGui.QWidget()
        
        self.elementFormLayout = QtGui.QGridLayout()
        self.elementFormWidget.setLayout(self.elementFormLayout)
        
        
        self.showList=QtGui.QComboBox()
        self.sqList=QtGui.QComboBox()
        self.shotList=QtGui.QComboBox()
        self.taskList=QtGui.QComboBox()
        
        self.userFilterLabel = QtGui.QLabel("User Filter")
        self.userFilter = QtGui.QLineEdit(str(os.getenv("USER")))
        
        self.renderList = QtGui.QListWidget()
        self.renderList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        
        self.generateList()
        
        self.backButton=QtGui.QPushButton("Back")
        self.nextButton=QtGui.QPushButton("Next")
        
        self.elementFormLayout.addWidget(self.showList,4,0)
        self.elementFormLayout.addWidget(self.sqList,4,1)
        self.elementFormLayout.addWidget(self.shotList,4,2)
        self.elementFormLayout.addWidget(self.taskList,4,3)
        self.elementFormLayout.addWidget(self.userFilterLabel,7,0)
        self.elementFormLayout.addWidget(self.userFilter,7,1,1,3)
        self.elementFormLayout.addWidget(self.renderList,6,0,1,4) 
        
        
    
    def generateList(self):
        self.showList.addItem("fom")
        self.sqList.addItems(["BB","EB","SB"])   
        self.shotList.addItems(["BB1015","EB2250","SB2200"])
        self.taskList.addItem("fx") 
        self.renderList.addItems(["Render1","Render2","Render3"])
        
    
    def currentIndexChanged(self,index):
        
        print self.releaseType.itemText(index)
    
    def filesUI(self):
        move = QtGui.QRadioButton("Move")
        copy = QtGui.QRadioButton("Copy")
        rename = QtGui.QRadioButton("Rename")
        pass
    


    
        
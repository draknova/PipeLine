from PySide import QtCore, QtGui

class ParameterUI(QtGui.QWidget):
    def __init__(self):
        super(ParameterUI,self).__init__()
        self.initUI()      
        
    
    def initUI(self):
        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        
        self.combo = QtGui.QComboBox()
        self.combo.addItems(["Files","Stats","Custom"])
        self.combo.currentIndexChanged.connect(self.currentIndexChanged)
        self.layout.addWidget(self.combo)
    
    def currentIndexChanged(self,index):
        
        print self.combo.itemText(index)
    
    def filesUI(self):
        move = QtGui.QRadioButton("Move")
        copy = QtGui.QRadioButton("Copy")
        rename = QtGui.QRadioButton("Rename")
        pass
    
    
        
from PySide import QtCore, QtGui

class ParameterUI(QtGui.QWidget):
    def __init__(self):
        super(ParameterUI,self).__init__()
        self.initUI()      
        
    
    def initUI(self):
        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        
        button = QtGui.QPushButton("Render")
        self.layout.addWidget(button,1,0)
'''
Created on Jan 27, 2016

@author: draknova
'''
import sys
from PySide import QtGui, QtCore

class ParameterPanelEdit(QtGui.QWidget):
    def __init__(self):
        super(ParameterPanelEdit, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        self._mainLayout = QtGui.QHBoxLayout(self)
        self.setLayout(self._mainLayout)
        
        self.parmTypeList = ParameterTypeList(self)
        self.parmTempList = ParameterTemplateList(self)
        self._mainLayout.addWidget(self.parmTypeList)
        self._mainLayout.addWidget(self.parmTempList)


class ParameterTypeList(QtGui.QListWidget):
    def __init__(self, parent = None):
        super(ParameterTypeList, self).__init__(parent)
        self.setDragEnabled(True)
        
        for t in ['int','float','string']:
            item = QtGui.QListWidgetItem(t, self)


        

        
class ParameterTemplateList(QtGui.QListWidget):
    def __init__(self, parent = None):
        super(ParameterTemplateList, self).__init__(parent)
        
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, e):
        for t in self.mimeTypes():
            if t in e.mimeData().formats():
                e.accept()
        
    def dropEvent(self, e):
        print e.mimeData().data(self.mimeTypes()[0])


def __main__():
    app = QtGui.QApplication(sys.argv)
    ui = ParameterPanelEdit()
    ui.setGeometry(100, 100, 300, 300)
    ui.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    __main__()
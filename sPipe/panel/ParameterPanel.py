import math
import sys
import os

from PySide import QtGui, QtCore

from sPipe.parameter import *
from sPipe.nodeDef.geo_locator import GEO_locator

class ParameterPanel(QtGui.QWidget):
    def __init__(self):
        super(ParameterPanel,self).__init__()
        self.initUI()
    
    def initUI(self):
        self._layout = QtGui.QVBoxLayout()
        self.setLayout(self._layout)
        self._layout.setContentsMargins(5,5,5,5)
        
        self.headerWidget = HeaderParameterPanel()
        self._layout.addWidget(self.headerWidget)
        
        self.parameterContainerWidget = QtGui.QWidget()
        self.parameterContainerWidgetLayout = QtGui.QGridLayout()
        self.parameterContainerWidget.setLayout(self.parameterContainerWidgetLayout)
        self._layout.addWidget(self.parameterContainerWidget)
        self._layout.addStretch()
        
    def displayParameterTemplateGroup(self, parameterTemplateGroup):
        for parm in parameterTemplateGroup.parameters():
            p = ParameterTemplateUI( parm )
            self.parameterContainerWidgetLayout.addWidget(p)

class HeaderParameterPanel(QtGui.QWidget):
    def __init__(self):
        super(HeaderParameterPanel,self).__init__()
        
        layout = QtGui.QHBoxLayout()
        self.setLayout(layout)
        
        self.nodeTypeLabel = QtGui.QLabel("<NodeDefaultType>")
        self.nodeNameField = QtGui.QLineEdit("<NodeDefaultName>")
        self.lockButton = QtGui.QPushButton("L")
        self.editInterfaceButton = QtGui.QPushButton("G")
        layout.addWidget(self.nodeTypeLabel)
        layout.addWidget(self.nodeNameField)
        layout.addWidget(self.lockButton)
        layout.addWidget(self.editInterfaceButton)
        


# This is the graphical aspect of the ParameterTemplate
class ParameterTemplateUI(QtGui.QFrame):
    def __init__(self, parameter, **kwargs):
        super(ParameterTemplateUI, self).__init__()
        self._parameter = parameter        
        self.initUI()

    
    def initUI(self):
        # Define Layout
        self._layout = QtGui.QHBoxLayout()
        self._layout.setContentsMargins(0,0,0,0)
        self._layout.setSpacing(5)
        self.setLayout(self._layout)
        
        # Create Elements
        self._label = QtGui.QPushButton(self._parameter.label())
        self._field = QtGui.QLineEdit(str(self._parameter.value()))
        self._slider = ParameterSlider()
        
        self._layout.addWidget(self._label)
        self._layout.addWidget(self._field)   
        self._layout.addWidget(self._slider)

        
class ParameterSlider(QtGui.QSlider):
    def __init__(self):
        super(ParameterSlider, self).__init__()
        self.setOrientation(QtCore.Qt.Horizontal)

        self.minValue = 0;
        self.maxValue = 1;
        
    def sliderChange(self, pos):
        v = self.value()
        v = (self.maxValue-self.minValue) * (float(self.value())/100.0) + self.minValue
        print v
        self.parent().setValue(v)
        self.update()


def main():
    app = QtGui.QApplication([])
    #style = QtGui.QStyle()
    #style = QtGui.QPlastiqueStyle()
    #app.setStyle(style)
    ui = ParameterPanel()
    ui.setGeometry(0,0,400,600)
    ui.show()
    
    p = GEO_locator()
    ui.displayParameterTemplateGroup(p.parmTemplateGroup())
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
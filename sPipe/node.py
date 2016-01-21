from PySide import QtCore, QtGui
from sPipe.connection import *
from sPipe.parameter import *
import json


class Node():
    def __init__(self, **kwargs):
        self._name =  kwargs['name'] if 'name' in kwargs.keys() else None
        self._type =  kwargs['type'] if 'type' in kwargs.keys() else "Null"
        self._inputs = list()
        self._position = [0,0]
        
    def __str__(self):
        d = dict()
        for v in vars(self):
            d[v[1:]] = eval("self.%s"%(v))
        return str(d)
        

class OPNode():
    def __init__(self, **kwargs):
        self._parmTemplateGroup = ParameterTemplateGroup()

    def parmTemplateGroup(self):
        return self._parmTemplateGroup
    
    def setParmTemplateGroup(self, newParmTemplateGroup):
        self._parmTemplateGroup = newParmTemplateGroup


class NodeUI(QtGui.QGraphicsItem):
    def __init__(self, _nodeType, name=""):
        super(Node,self).__init__()

        self._name=name
        self._nodeType=_nodeType
        self._inputs=list()
        self._outputs=list()
        
        self._parameters=list()
        
        self.x = 0
        self.y = 0
        
        self.setFlags(QtGui.QGraphicsItem.ItemIsSelectable)
        
        # Drawing attributes
        self.position=QtCore.QPointF()
        self.size=QtCore.QPointF(80,25)
        self.sceneScale=1
        
        self.inputConnector = Connector(self,True)
        self.outputConnector = Connector(self,False)

        self.setZValue(1000)
        
    
    def name(self):
        return self._name
    
    def setName(self,newName):
        self._name = self.checkForUniqueName(newName)
        return self._name

    def nodeType(self):
        return self._nodeType

    def setParameters(self,paramerterDict):
        for parameterName in paramerterDict.keys():
            p = Parameter(parameterName, paramerterDict[parameterName])
            self._parameters.append(p)
        
    def parameters(self):
        return self._parameters
    
    def parameter(self,name):
        for p in self._parameters:
            print p.name()
            if p.name() == name:
                
                return p

    def checkForUniqueName(self,newName):
        if self.scene() != None:
            for node in self.scene().items():
                if type(node) == Node:
                    if newName == node.name():
                        for i in range(1,len(newName)):
                            if not newName[-i:].isdigit():
                                if i > 1:
                                    newName = newName[:-i+1] + str(int(float(newName[-i+1:]))+1)
                                else:
                                    newName += "1"
                                break
    
            for node in self.scene().items():
                if type(node) == Node:
                    if newName == node.name():
                        newName = self.checkForUniqueName(newName)
        return newName
    
    def inputs(self):
        inputNodes = list()
        for inConnection in self._inputs:
            inputNodes.append(inConnection.inputNode)
        return inputNodes

    def outputs(self):
        outputNodes = list()
        for outConnection in self._outputs:
            outputNodes.append(outConnection.outputNode)
        return outputNodes
    
    def addInput(self,newInput):
        if type(newInput) == Node:
            newConnection = Connection(newInput,self)
            self._inputs.append(newConnection)
            newInput.addOutput(newConnection)
            return True
        elif type(newInput) == Connection:
            if not newInput in self._inputs:
                self._inputs.append(newInput)
            if not newInput in newInput.inputNode._outputs:
                newInput.inputNode.addOutput(newInput)
            return True
        else:
            return False

    def addOutput(self,newOutput):
        if type(newOutput) == Node:
            newConnection = Connection(self,newOutput)
            self._outputs.append(newConnection)
            newOutput.addInput(newConnection)
            return True
        elif type(newOutput) == Connection:
            if not newOutput in self._outputs:
                self._outputs.append(newOutput)
            if not newOutput in newOutput.outputNode._inputs:
                newOutput.outputNode.addInput(newOutput)
            return True
        else:
            return False
    
    
    def removeInput(self,removedConnection):
        while removedConnection in self._inputs:
            self._inputs.remove(removedConnection)

    def removeOutput(self,removedConnection):
        while removedConnection in self._outputs:
            self._outputs.remove(removedConnection)

    def delete(self):
        while len(self._inputs) > 0:
            self._inputs[0].delete()
        while len(self._outputs) > 0:
            self._outputs[0].delete()
        
        self.scene().removeItem(self)
    
    def boundingRect(self):
        self.rect = QtCore.QRectF(-self.size.x()/2,-self.size.y()/2,self.size.x(),self.size.y())
        return self.rect
    
    def paint(self,painter,option, widget):   
        blackPen = QtGui.QPen()
        whitePen = QtGui.QPen()
        blackPen.setWidth(1)
        whitePen.setWidth(1)
        blackPen.setColor(QtGui.QColor("black"))
        whitePen.setColor(QtGui.QColor("white"))
        
        if self.isSelected():
            gradient = QtGui.QLinearGradient(QtCore.QPointF(0, 0), QtCore.QPointF(0, 20))
            gradient.setColorAt(0, QtGui.QColor(220,170,50))
            gradient.setColorAt(0.3, QtGui.QColor(220,170,50))
            gradient.setColorAt(1, QtGui.QColor(170,150,40))
            #brush = QtGui.QBrush(gradient)
            #brush.setStyle(QtCore.Qt.LinearGradientPattern)
            brush = QtGui.QBrush(QtGui.QColor(220,160,50))
            
            
        else:
            gradient = QtGui.QLinearGradient(QtCore.QPointF(0, 0), QtCore.QPointF(0, 20))
            gradient.setColorAt(0, QtGui.QColor(55,55,55))
            gradient.setColorAt(0.3, QtGui.QColor(60,60,60))
            gradient.setColorAt(1, QtGui.QColor(50,50,50))
            #brush = QtGui.QBrush(gradient)
            #brush.setStyle(QtCore.Qt.LinearGradientPattern)
            #brush = QtGui.QBrush(QtGui.QColor(50,50,50))
            brush = QtGui.QBrush(QtGui.QColor(32,61,74))
            
            
        
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        font.setPointSize(14)
        
        
        painter.setBrush(brush)
        painter.setPen(blackPen)
        painter.setFont(font)
        
        painter.drawRoundedRect(self.rect,5,5)

        #pen.setColor(QtGui.QColor("white"))
        if self.scale > 0.75:
            painter.setPen(whitePen)
            painter.drawText(self.rect, QtCore.Qt.AlignCenter,self.name())

    
    def inputPos(self):
        x = self.pos().x()
        y = self.pos().y() - self.size.y()/2
        return QtCore.QPoint(x,y)
    
    def outputPos(self):
        x = self.pos().x()
        y = self.pos().y() + self.size.y()/2
        return QtCore.QPoint(x,y)
 
    
class Connector(QtGui.QGraphicsItem):
    def __init__(self, parent, isInput_):
        super(Connector,self).__init__()
        self.size=QtCore.QPoint(20,6)
        self.isInput_ = isInput_
        self.parent_ = parent
        
        self.setZValue(10000)
        
        self.setParentItem(parent)
        if self.isInput_:
            self.setPos(QtCore.QPoint(0,-parent.size.y()/2))
        else:
            self.setPos(QtCore.QPoint(0,parent.size.y()/2))
    
    def boundingRect(self):
        self.rect = QtCore.QRectF(-self.size.x()/2,-self.size.y()/2,self.size.x(),self.size.y())
        return self.rect
    
    def paint(self,painter,option, widget):
        pen = QtGui.QPen()
        pen.setWidth(1)
        brush = QtGui.QBrush()
        brush.setStyle(QtCore.Qt.SolidPattern)
        brush.setColor(QtGui.QColor("white"))
        
        painter.setBrush(brush)
        painter.drawRect(self.rect)

    def isInput(self):
        return self.isInput_
    
    def parent(self):
        return self.parent_
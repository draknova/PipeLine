"""
Connection

Graphic Element to connect elements together

"""

from PySide import QtCore, QtGui
from matplotlib.font_manager import path

class Connection(QtGui.QGraphicsItem):
    def __init__(self, inputNode, outputNode):
        super(Connection,self).__init__()
        
        self.setFlags(QtGui.QGraphicsItem.ItemIsSelectable)
        self.setSelected(False)
        
        self.inputNode=inputNode
        self.outputNode=outputNode
        
        self.angle=None
        self.length=None
        
        # angular : made of vertical and horizontal lines
        # diagonal : go straigh
        # bezier : do curves
        self.style = "bezier"
        
        self.setZValue(100)
        
        # Add the connection to the scene
        if self.inputNode.scene() != None and self.inputNode.scene() == self.outputNode.scene():
            self.inputNode.scene().addItem(self)
    
    def delete(self):
        "Print Deleting"
        self.inputNode.removeOutput(self)
        self.outputNode.removeInput(self)
        self.scene().removeItem(self)
        self.inputNode = None
        self.outputNode = None
    
    
    def boundingRect(self):  
        minx = min(self.inputNode.outputPos().x(), self.outputNode.inputPos().x()) - 20
        miny = min(self.inputNode.outputPos().y(), self.outputNode.inputPos().y()) - 20
        
        maxx = max(self.inputNode.outputPos().x(), self.outputNode.inputPos().x()) + 20
        maxy = max(self.inputNode.outputPos().y(), self.outputNode.inputPos().y()) + 20

        self.rect = QtCore.QRectF(minx,miny,maxx-minx,maxy-miny)
        return self.rect

    def shape(self):
        stroke = QtGui.QPainterPathStroker()
        stroke.setWidth(5)
        return stroke.createStroke(self.connectionPath)

    def paint(self,painter,option, widget):
        if self.inputNode == None or self.outputNode == None:
            self.scene().removeItem(self)
            return
        
        
        pen = QtGui.QPen()
        pen.setWidth(2)
        
        if self.isSelected():
            pen.setColor("yellow")
        else:
            #pen.setColor("white")
            pen.setColor(QtGui.QColor(139,161,164))
        painter.setPen(pen)

        #indexIn = self.outputNode.inputs().index(self) * 0
        #indexOut = self.inputNode.outputs().index(self) * 0
        indexIn= 0
        indexOut = 0

        if self.style == "angualar":
            
    
            p0 = self.inputNode.outputPos().__add__(QtCore.QPoint(indexOut,0))
            p1 = p0.__add__(QtCore.QPoint(0,10))
            
            p5 = self.outputNode.inputPos().__add__(QtCore.QPoint(indexIn,0))
            p4 = p5.__add__(QtCore.QPoint(0,-10))  
            
            x = p4.x() - p1.x() +indexOut
            if p1.y() > p4.y():
                x = 45
                if abs(p4.x()-p1.x()) > x*2:
                    x = (p4.x()-p1.x())/2
                
                elif p1.x() < p4.x():
                    x *= -1
    
            p2 = self.inputNode.outputPos().__add__(QtCore.QPoint(x,10))
            y = p4.y() - p2.y()
            p3 = p2.__add__(QtCore.QPoint(0,y))
            
            path = QtGui.QPainterPath(p0)
            path.lineTo(p1)
            path.lineTo(p2)
            path.lineTo(p3)
            path.lineTo(p4)
            path.lineTo(p5)
            
            self.connectionPath = path
            painter.drawPath(self.connectionPath)
            
            # Paint Arrow
            if abs(x) > 20:
                brush = QtGui.QBrush()
                brush.setColor(QtGui.QColor("white"))
                brush.setStyle(QtCore.Qt.SolidPattern)
                painter.setBrush(brush)
                size = 5
                if x < 0:
                    direction = -1
                else:
                    direction = 1
                arrow0 = p1.__add__(QtCore.QPoint(direction*size*2 + x/2,0))
                arrow1 = p1.__add__(QtCore.QPoint(x/2,-size))
                arrow2 = p1.__add__(QtCore.QPoint(x/2,size))
                
                arrowPath = QtGui.QPainterPath(arrow0)
                arrowPath.lineTo(arrow1)
                arrowPath.lineTo(arrow2)
                arrowPath.closeSubpath()
                
                painter.drawPath(arrowPath)
        
        elif self.style == "bezier":
            p0 = self.inputNode.outputPos().__add__(QtCore.QPoint(indexOut,0))
            p1 = self.outputNode.inputPos().__add__(QtCore.QPoint(indexIn,0))
            
            y = max(20,abs(p1.y()-p0.y())) * 0.5
            
            p2 = p0.__add__(QtCore.QPoint(0,y))
            p3 = p1.__add__(QtCore.QPoint(0,-y))
            
            path = QtGui.QPainterPath(p0)
            path.cubicTo(p2,p3,p1)
            self.connectionPath = path
            painter.drawPath(self.connectionPath)
        
        else:
            p0 = self.inputNode.outputPos().__add__(QtCore.QPoint(indexOut,0))
            p1 = self.outputNode.inputPos().__add__(QtCore.QPoint(indexIn,0))
            
            path = QtGui.QPainterPath(p0)
            path.lineTo(p1)
            
            self.connectionPath = path
            painter.drawPath(self.connectionPath)
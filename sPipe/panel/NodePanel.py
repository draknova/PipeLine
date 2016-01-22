import sys
import json
import os

from PySide import QtCore, QtGui

from sPipe.scene import OPScene
from sPipe.node import *
from sPipe.connection import *
import sPipe.pCore as pc
from sPipe.panel.ParameterPanel import ParameterPanel


# Main Widget :: Node editor
# Containt the Node View, menu bar and buttons
class QNodePanel(QtGui.QWidget):
    def __init__(self):
        super(QNodePanel,self).__init__()

        self._parameterPanel = None
        
        self.initUI()      

    def initUI(self):
        self._layout = QtGui.QGridLayout(None)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,5,0,5)
        self._layout.setSpacing(0)
        #self.setContentsMargins(10,10,10,10)
        
        
        self.view = NodeView()
        
        #n1 = self.view.createNode("Box")
        #n2 = self.view.createNode("Extrude")
        #n2.addInput(n1)
        
        self._parameterPanel = ParameterPanel()
        self.createMenuBar()


        
        self._layout.addWidget(self.view,1,0)
        self._layout.addWidget(self._parameterPanel,1,1)
        
        
        self.openFile("/Users/draknova/Documents/workspace/sPipe/sPipe/OLD_tests/job_01.json")

    def createMenuBar(self):
        self._menu = QtGui.QMenuBar(self)
        self._menu.setNativeMenuBar(False)
        
        fileMenu = self._menu.addMenu("File")
        fileMenu.addAction("New")
        fileMenu.addAction("Open", self.openFileBrowser)
        fileMenu.addAction("Save", self.saveToFile)
        fileMenu.addAction("Save As")
        fileMenu.addSeparator()
        fileMenu.addAction("Import")
        fileMenu.addAction("Export")
        
        nodeMenu = self._menu.addMenu("Node")
        nodeMenu.addAction("Create...")
        nodeMenu.addAction("Duplicate")
        nodeMenu.addAction("Delete")
        nodeMenu.addAction("Find...")
        
        self._menu.addAction("Save",self.saveToFile)
        
        self._layout.addWidget(self._menu)

    def parameterPanel(self):
        return self._parameterPanel
    
    def connectParameterPanel(self, widget):
        self.parameterPanel_ = widget        

    def openFileBrowser(self):
        fileBrowser = QtGui.QFileDialog(self)
        fileBrowser.setNameFilter("Json (*.json)")
        if fileBrowser.exec_():
            filesPath = fileBrowser.selectedFiles()
            if len(filesPath) > 0:
                self.openFile(filesPath[0])

    def openFile(self, filePath):
        f = open(filePath,"r")
        content = f.read()
        f.close()
        
        for node in json.loads(content):
            nodeType = node['type']
            nodeName = node['name']
            nodePosition = node['position']
            nodeParameters = node['parameters']
            
            n = self.view.createNode(nodeType, nodeName)
            n.setPos(nodePosition[0],nodePosition[1])
            n.setParameters(nodeParameters)
            
            for inputName in node['inputs']:
                # Look for the node with that name
                for existingNode in self.view.items():
                    if type(existingNode) == QNode:
                        if existingNode.name() == inputName:
                            n.addInput(existingNode)

    def saveToFile(self):
        filePath = "../job_02.json"
        
        sceneContent = list()
        for item in self.view.items():
            if type(item) == Node:
                n = dict()
                n['nodeType'] = item.nodeType()
                n['name'] = item.name()
                
                pos = item.pos()
                n['position'] = [pos.x(), pos.y()]
                
                inputs = list()
                for inputNode in item.inputs():
                    inputs.append( inputNode.name() )
                
                n['inputs'] = inputs
                n['parameters'] = dict()
                
                sceneContent.append(n)
        sceneFileContent = json.dumps(sceneContent, sort_keys=False, indent=4, separators=(',', ': '))
        print sceneFileContent
        


# View displaying node editor.
# It Contains the Scene, nodes and connection
# Most of the manipulations are done inside
class NodeView(QtGui.QGraphicsView):
    def __init__(self):
        super(NodeView,self).__init__()
        self._scene = OPScene()
        
        # Obsolete
        self.nodeList = list()
        
        # Variables
        self.clickedItem = None
        self.itemMode = None        # Define which item is selected

        self.mousePositionX = 0
        self.mousePositionY = 0
        
        self.mode = None
        
        # Configure QGraphics View
        self.setSceneRect(0, 0, -1, -1)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setMouseTracking(True)
        self.setRenderHints(QtGui.QPainter.Antialiasing)
        self.setViewportUpdateMode(QtGui.QGraphicsView.FullViewportUpdate)
        
        # Init QGraphic Scene
        self.sc = QtGui.QGraphicsScene()
        self.setScene(self.sc)
        self.sceneScale = 0.7
        
        # Paint the background
        brush = QtGui.QBrush()
        brush.setTransform(QtGui.QTransform().scale(0.75, 0.75))
        brush.setTextureImage(QtGui.QImage("/Users/draknova/Documents/workspace/sPipe/bin/images/gridTexture.jpg"))
        self.sc.setBackgroundBrush(brush)


    ######################
    ####### EVENTS #######
    ######################
    
    ### KEYBOARD EVENTS ##
    def keyReleaseEvent(self,event):
        if event.key() == QtCore.Qt.Key_Space:
            self.createNodeMenu()
            #node = self.createNode("Null")
            #node.setPos(self.mapToScene(self.mapFromGlobal(QtGui.QCursor.pos())))
        elif event.key() == QtCore.Qt.Key_Backspace:
            self.deleteNodes()
            
        elif event.key() == QtCore.Qt.Key_H:
            self.redifinePositions()
            
        elif event.key() == QtCore.Qt.Key_L:
            for item in self.sc.items():
                print item
        
        elif event.key() == QtCore.Qt.Key_Escape:
            self.mode = None
    
    ### MOUSE EVENTS ######
    def mousePressEvent(self,event):
        self.previousClickedItem = self.clickedItem
        self.clickedItem = self.itemAt(event.pos())
        
        self.mousePositionX = event.pos().x()
        self.mousePositionY = event.pos().y()
        self.mouseClickedPositionX = self.mousePositionX
        self.mouseClickedPositionY = self.mousePositionY
        
        if event.button() == QtCore.Qt.LeftButton:
            if type(self.clickedItem) == QNode:
                self.mode = "selection"
                self.selection(event)
            elif type(self.clickedItem) == Connector:
                self.mode = "connection"
                clickPos = self.mapToScene(event.pos())
                #print self.clickedItem.shape().contains(clickPos)
                #print self.clickedItem
                self.connection(event)
            elif type(self.clickedItem) == Connection:
                self.mode = "selection"
                self.selection(event)
            else:
                self.mode = "scene"

        elif event.button() == QtCore.Qt.RightButton:
            print "Right Click"
            
        else:
            self.itemMode=None
            for item in self.scene().items():
                if type(item) == Node:
                    item.setSelected(False)
    
    def mouseDoubleClickEvent(self,event):
        if event.button() == QtCore.Qt.LeftButton:
            clickedItem = self.itemAt(event.pos())
            if type(clickedItem) == Node:
                if type(self.parent()) == NodePanel:
                    if self.parent().parameterPanel() != None:
                        self.parent().parameterPanel().setParameterFromNode(clickedItem)
        
    def mouseReleaseEvent(self,event):
        if event.button() == QtCore.Qt.LeftButton:
            if self.mode == "selection":
                if event.pos().x() == self.mouseClickedPositionX and event.pos().y() == self.mouseClickedPositionY:
                    #self.selection(event)
                    pass
            
            if self.mode == "scene":
                if event.pos().x() == self.mouseClickedPositionX and event.pos().y() == self.mouseClickedPositionY:
                    for item in self.sc.selectedItems():
                        item.setSelected(False)
        
        
    def mouseMoveEvent(self,event):
        x = event.pos().x()
        y = event.pos().y()
        if self.mousePositionX != None and self.mousePositionY != None:
            movex = (self.mousePositionX - x) * (1/self.transform().m11())
            movey = (self.mousePositionY - y) * (1/self.transform().m11())
    
    
            if event.buttons() == QtCore.Qt.LeftButton:
                if self.mode == "selection":
                    for item in self.sc.selectedItems():
                        if type(item) == QNode:
                            posx = item.pos().x() - movex
                            posy = item.pos().y() - movey
                            item.setPos(posx,posy)
                
                if self.mode == "scene":
                    if event.modifiers() == QtCore.Qt.ALT:
                        posx = movex + self.sceneRect().x()
                        posy = movey + self.sceneRect().y()
                        self.setSceneRect(posx,posy,self.sceneRect().width(),self.sceneRect().height())
                    else:
                        for item in self.sc.selectedItems():
                            item.setSelected(False)
    
        self.mousePositionX = x
        self.mousePositionY = y
    
    def wheelEvent(self,event):
        sceneScale = 1 + event.delta()*0.01
        sceneScale = max(0.2/self.transform().m11(),sceneScale)
        sceneScale = min(2/self.transform().m11(),sceneScale)
        self.scale(sceneScale,sceneScale)
        


    #### SCENE MANIPULATION ##
    
    # Set selection based on modifiers
    def selection(self,event):
        clickPos = self.mapToScene(event.pos())
        clickedItem = self.sc.itemAt(clickPos)
        
        if event.modifiers() != QtCore.Qt.SHIFT and event.modifiers() != QtCore.Qt.CTRL:
            for item in self.scene().selectedItems():
                #if type(item) == Node:
                item.setSelected(False)
        
        if type(clickedItem) == QNode:
            if event.modifiers() == QtCore.Qt.CTRL:
                clickedItem.setSelected(False)
            else:
                clickedItem.setSelected(True)

        if type(clickedItem) == Connection:
            for item in self.scene().selectedItems():
                if type(item) == Connection:
                    item.setSelected(False)
            
            clickedItem.setSelected(True)

    def connection(self,event):
        if type(self.previousClickedItem) == Connector:
            if self.previousClickedItem != self.clickedItem:
                if self.previousClickedItem.isInput() != self.clickedItem.isInput():
                    if self.clickedItem.isInput():
                        self.clickedItem.parent().addInput(self.previousClickedItem.parent())
                    else:
                        self.previousClickedItem.parent().addInput(self.clickedItem.parent())

    # USER FUNCTIONS
    def update(self):
        self.nodeList = list()
        for item in self.items():
            if type(item) == Node: 
                self.nodeList.append(item)
        # Clear
        for item in self.items():
            self.sc.removeItem(item)
        
        # Draw Connections    
        for node in self.nodeList:
            print node.name()
            for input_ in node.inputs():
                c = Connection(input_,node)
                self.sc.addItem(c)
        
        # Draw Nodes
        for node in self.nodeList:
            self.sc.addItem(node)
    
    def createNodeMenu(self):
        menuEntry = QtGui.QGraphicsWidget()
        menuEntryLayout = QtGui.QHBoxLayout()
        menuEntry.setLayout(menuEntryLayout)
        
        menuEntry.setGeometry(0,0,100,100)
        
        menuEntryTextField = QtGui.QLineEdit()
        menuEntryLayout.addWidget(menuEntryTextField)
        
        
        menu = QtGui.QMenu("Create Node")
        menu.addAction("Node1")
        menu.addAction("Node2")
        menu.popup(QtGui.QCursor.pos())
        menu.setZValue(100000)
        print "Menu"
    
    def createNode(self, nodeType, nodeName="NewNode"):
        n = QNode(nodeType)
        self.scene().addItem(n)
        n.setName(nodeName)
        
        return n

    def deleteNodes(self):
        for item in self.sc.selectedItems():
            if type(item) == Node:
                item.delete()
            if type(item) == Connection:
                item.delete()

    # Auto placement nodes
    def redifinePositions(self):
        x=0
        y=0
        
        nodeList = list()
        for item in self.sc.items():
            if type(item) == Node:
                nodeList.append(item)

        self.movedNodes = list()
        for node in nodeList:
            print node.outputs()
            if len(node.outputs()) == 0:
                x = self.positionNode(node, x, y)
                x += 100
                y = 0
        
        for node in nodeList:
            if len(node.outputs()) == 0:
                #self.smoothPosition(node)
                pass
                
    
    def smoothPosition(self,node):
        minX = 0
        maxX = 0
        for i,input_ in enumerate(node.inputs()):
            x = input_.pos().x()
            if i != 0:
                minX = min(minX,x)
                maxX = max(maxX,x)
            else:
                minX = x
                maxX = x
        
        print node.name()
        for i,input_ in enumerate(node.inputs()):
            if len(node.inputs())>1:
                x = -((maxX-minX)/2)
                #x += i/(len(node.inputs())-1) * ((maxX-minX)/len(node.inputs()))
                self.offsetAbove(input_, x, 0)
            self.smoothPosition(input_)
            
    def offsetAbove(self,node,x,y):
        node.setPos(node.pos().x()+x,node.pos().y()+y)
        for input_ in node.inputs():
            self.offsetAbove(input_, x, y)

    def positionNode(self, node, x, y):
        moveY = 50
        moveX = 100
        
        if not node in self.movedNodes: 
            y -= moveY
            node.setPos(x,y)
            self.movedNodes.append(node)

        else:
            newY = 0
            for output_ in node.outputs():
                newY = min(output_.pos().y(),newY)
            newY -= moveY
            node.setPos(node.pos().x(),newY)
            
        for i,input_ in enumerate(node.inputs()):
            x += moveX*(i>0)
            x = self.positionNode(input_, x, y)
            
        return x


def main():
    app = QtGui.QApplication([])
    f = open(pc.CSSPATH,"r")
    s = f.read()
    f.close()
    app.setStyleSheet(s)
    ui = QNodePanel()
    ui.setGeometry(0,0,600,400)
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
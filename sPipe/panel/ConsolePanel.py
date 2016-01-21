import math
import time
import sys
import subprocess
import os
import json

if not '/usr/local/lib/python2.7/site-packages' in sys.path:
    sys.path.append('/usr/local/lib/python2.7/site-packages')

from PySide import QtCore, QtGui


# Main Widget :: Node editor
# Containt the Node View, menu bar and buttons
class ConsolePanel(QtGui.QWidget):
    def __init__(self):
        super(ConsolePanel,self).__init__()
        self.nodeList=list()
        
        self.parameterPanel_ = None
        
        self._initUI()      

    def _initUI(self):
        self._layout = QtGui.QGridLayout(None)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)
        
        self._menu = QtGui.QMenuBar(self)
        self._menu.setNativeMenuBar(False)
        _menuFile = self._menu.addMenu("File")
        _menuFile.addAction("Open...")
        _menuFile.addAction("Save")
        _menuFile.addAction("Save As...")
        _menuFile.addSeparator()
        _menuFile.addAction("Execute")
        _menuFile.addAction("Execute File...")
        
        _menuConsole = self._menu.addMenu("Console")
        _menuConsole.addAction("Show Everything")
        _menuConsole.addSeparator()
        _menuConsole.addAction("Show Only Error")
        _menuConsole.addAction("Show Only Warning")
        _menuConsole.addAction("Show Only Message")
        _menuConsole.addSeparator()
        _menuConsole.addAction("Clear")
        
        self._outputConsole = OutputConsole()
        self._inputConsole = InputConsole()
        
        self._layout.addWidget(self._menu,0,0)
        self._layout.addWidget(self._outputConsole,1,0)
        self._layout.addWidget(self._inputConsole,2,0)
              

class OutputConsole(QtGui.QTextEdit):
    def __init__(self):
        super(OutputConsole,self).__init__()
        self.setReadOnly(True)
        
        self.message("Hello World")
        self.warning("Carefull")
        self.error("May day")
    
    def output(self, document):
        self.append(document)
    
    def message(self,text):
        self.output( ('<p style="color:#CCC;">%s - %s</p>'%(self.timeReport(),str(text))) )
    
    def warning(self,text):
        self.output( ('<p style="color:Orange;">%s - WARNING : %s</p>'%(self.timeReport(),str(text))) )
    
    def error(self,text):
        self.output( ('<p style="color:Red;">%s - ERROR : %s</p>'%(self.timeReport(),str(text))) )
    
    def timeReport(self):
        return str(time.strftime("%H:%M:%S"))
    
    
    # To Read later :
    # http://www.cyberciti.biz/faq/python-run-external-command-and-get-output/
    def evalCmd(self, cmd):
        cmd = "for i in range(0,10000):\n\tprint i"
        tmpFilePath = ("/tmp/consolePanelScript_%i.py"%(time.time()))
        f = open(tmpFilePath,"w+")
        f.write(cmd)
        f.close()
        #try:
        #execfile(tmpFilePath)
        #p = subprocess.Popen(["python",tmpFilePath])
        
        cmd = ("python %s"%(tmpFilePath))
        #cmd = "/Applications/Calculator.app/Contents/MacOS/Calculator"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            (output, err) = p.communicate()
            self.message(output.replace("\n","</br>"))
            if p.poll() != None:
                break

        os.system("rm %s"%(tmpFilePath))
        #except:
        #    pass

class InputConsole(QtGui.QTextEdit):
    def __init__(self):
        super(InputConsole,self).__init__()
    
    
    def keyPressEvent(self,event):
        if event.key() == QtCore.Qt.Key_Return and event.modifiers() == QtCore.Qt.META:
            event.ignore()
        else:
            QtGui.QTextEdit.keyPressEvent(self,event)
    
    def keyReleaseEvent(self,event):
        #if event.keys()
        if event.key() == QtCore.Qt.Key_Return and event.modifiers() == QtCore.Qt.META:
            self.parent()._outputConsole.evalCmd(self.toPlainText())


def main():
    app = QtGui.QApplication([])
    f = open("../darkorange.stylesheet","r")
    s = f.read()
    f.close()
    app.setStyleSheet(s)
    ui = ConsolePanel()
    ui.setGeometry(0,0,600,400)
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
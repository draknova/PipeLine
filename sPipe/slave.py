#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os 
import time
import socket


if not '/usr/local/lib/python2.7/site-packages' in sys.path:
    sys.path.append('/usr/local/lib/python2.7/site-packages')
    
    
#from PyQt4 import QtCore, QtGui
from PySide import QtCore, QtGui

import PCore as pc


class sRenderSlave(QtCore.QThread):
    def __init__(self, parent):
        super(sRenderSlave, self).__init__()
        self.host = pc.HOSTSERVER
        self.port = pc.PORTSERVER
        self.waitTime = 5
        self.parent = parent
        self._quit= False
        
        # Status :
        # Wait - Wait for job
        # Run - Is calculating something
        # Error - Error when calculating
        # End - Finished a job
        self._status = "Wait"
        self._taskId = 0

    def run(self):
        self.parent.output("Slave started")
        
        requestTime = time.time() - self.waitTime
        while 1:
            # Wait for time before connecting again
            if self._quit == True:
                print "Stopping"
                break
            
            if time.time() > requestTime + self.waitTime:
                requestTime = time.time()
                
                # Establish Connection with server
                try:
                    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    self.s.connect( (self.host,self.port) )

                    # Send info to server about current status
                    if self._status == "Wait":
                        self.s.sendall("/requestTask")
                        
                    elif self._status == "Run":
                        
                        self.s.sendall("/run %i"%(self._taskId))
                        
                    elif self._status == "Error":
                        self.s.sendall("/error %i"%(self._taskId))
                    
                    elif self._status == "End":
                        self.s.sendall("/end %i"%(self._taskId))
                        
                    else:
                        self.s.sendall("/report")
                    
                    print 2
                    
                    # Wait for server reply
                    data = self.s.recv(1024)
                    
                    # Close Connection
                    self.s.close()
                
                    # Analize server reply and what to do next
                    self.analizeAnswer(data)
                
                except:
                    self.parent.output("Error Connecting to server")
            
            time.sleep(1)    
            
    def analizeAnswer(self,answer):
        print answer[:8]
        
        if answer[:8] == "/execute":
            # Change status
            self._status = "Run"
            self._taskId = int(float(answer[9:]))
            
            # Execute task
            self.parent.output("Executing task : %s"%(answer[9:]))
            #eval(answer[9:])
            #time.sleep(15)
            
            
            # If task end succesfuly
            if 1:
                self._status = "End"
                self.parent.output("Done")
            else:
                self._status = "Error"
                self.parent.output("Error")
    
        elif answer[:12] == "/waitForNext":
            self._status = "Wait"
            self.parent.output("Waiting for next job")
    
    
        
    def sendQuitSignal(self):
        self._quit = True



class sRenderSlaveUI(QtGui.QWidget):
    def __init__(self):
        super(sRenderSlaveUI, self).__init__()
        self._slaveThread = None
        self.start() 
        
    def start(self):
        # Place widget in the layout
        self.gridLayout = QtGui.QGridLayout(self)
        self.gridLayout.setSpacing(5)
        
        self.console = QtGui.QTextEdit()
        self.console.setReadOnly(True)
        
        self.startButton = QtGui.QPushButton("Start")
        self.stopButton = QtGui.QPushButton("Stop")
        self.quitButton = QtGui.QPushButton("Quit")
        
        self.startButton.clicked.connect(self.startSlave)
        self.stopButton.clicked.connect(self.stopSlave)
        self.quitButton.clicked.connect(self.quitRenderSlaveUI)
        
        self.gridLayout.addWidget(self.console,1,0,1,4)
        self.gridLayout.addWidget(self.startButton,2,0,1,1)
        self.gridLayout.addWidget(self.stopButton,2,1,1,1)
        self.gridLayout.addWidget(self.quitButton,2,3,1,1)
        
        self.setWindowTitle('sRender Slave')
        self.setGeometry(0, 0, 500, 400)
        self.show()

        self.startSlave()

    def startSlave(self):
        if self._slaveThread == None or self._slaveThread.isRunning() == False:
            self._slaveThread = sRenderSlave(self)
            self._slaveThread.start()
        else:
            self.output("Slave already started")
    
    def stopSlave(self):
        if self._slaveThread != None and self._slaveThread.isRunning() == True:
            self._slaveThread.sendQuitSignal()
            #self._slaveThread.terminate()
        else:
            self.output("Slave already stopped")

    def quitRenderSlaveUI(self):
        self.stopSlave()
        QtCore.QCoreApplication.instance().quit()
        

    def output(self, text):
        self.console.append(text)

def main():
    app = QtGui.QApplication([])
    ui = sRenderSlaveUI()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


slave = sRenderSlave()
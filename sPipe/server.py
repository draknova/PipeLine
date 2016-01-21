#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import time
import SocketServer

import sqlite3
from PySide import QtCore, QtGui

import pCore as pc

class serverHandler(SocketServer.BaseRequestHandler):  
    def handle(self):
        self.data = self.request.recv(1024).strip()
        answer = self.analyzeSignal(self.data)
        self.request.sendall(str(answer))

    def analyzeSignal(self, signal):
        print "Server : " + str(signal)
        if signal[:12] == "/requestTask":
            task = self.requestTask()
            return str(task)
        
        elif signal[:4] == "/end":
            self.setJobAsEnded(signal[5:])
            return "/waitForNext"
        
        else:
            return None
            
    def requestTask(self):
        # Connect to database
        conn = sqlite3.connect(pc.DATABASEPATH)
        conn.row_factory = sqlite3.Row  # Needed to get database as a array
        cur = conn.cursor()
        
        request = cur.execute("SELECT rowid FROM farm_tasks WHERE status='waiting' ORDER BY priority DESC LIMIT 1")


        try:
            for item in request:
                print item
                taskId = int(float(item[0]))
                cur.execute('UPDATE farm_tasks SET status="run" WHERE rowid=%s'%(taskId))
            conn.commit()
            conn.close()
            
            cmd = ("/execute %i"%(taskId))
            return cmd
        except:
            return "/waitForNext"
        
    
    def setJobAsEnded(self, jobId):
        conn = sqlite3.connect(pc.DATABASEPATH)
        conn.row_factory = sqlite3.Row  # Needed to get database as a array
        cur = conn.cursor()
        cur.execute('UPDATE farm_tasks SET status="end" WHERE rowid=%s'%(jobId))
        
        conn.commit()
        conn.close()
        
        pass        

class sRenderServer(QtCore.QThread):
    def __init__(self, parent):
        super(sRenderServer, self).__init__()
        self.host = pc.HOSTSERVER
        self.port = pc.PORTSERVER
        self.parent = parent
    
    def run(self):
        self.parent.output("Starting server...")
        SocketServer.TCPServer.allow_reuse_address = True
        self._serverThread = SocketServer.TCPServer((self.host,self.port),serverHandler)
        self._serverThread.serve_forever()
        self.exec_()
        
    def stopServer(self):
        self.parent.output("Stopping server...")
        #self._serverThread.server_close()
        self._serverThread.shutdown()


class sRenderServerUI(QtGui.QWidget):
    def __init__(self):
        super(sRenderServerUI, self).__init__()
        self._serverThread = None
        self.start()
        
    def start(self):
        # Place widget in the layout
        self.gridLayout = QtGui.QGridLayout(self)
        self.gridLayout.setSpacing(5)
        
        self.console = QtGui.QTextEdit()
        self.console.setReadOnly(True)
        
        self.startServerButton = QtGui.QPushButton("Start")
        self.stopServerButton = QtGui.QPushButton("Stop")
        self.quitButton = QtGui.QPushButton("Quit")
        
        
        self.startServerButton.clicked.connect(self.startServer)
        self.stopServerButton.clicked.connect(self.stopServer)
        self.quitButton.clicked.connect(self.quitRenderServerUI)
        
        self.gridLayout.addWidget(self.console,1,0,1,4)
        self.gridLayout.addWidget(self.startServerButton,2,0,1,1)
        self.gridLayout.addWidget(self.stopServerButton,2,1,1,1)
        self.gridLayout.addWidget(self.quitButton,2,3,1,1)
        
        self.setWindowTitle('sRender Server')
        self.setGeometry(0, 0, 500, 400)
        self.show()
        
        self.startServer()
 
 
    def output(self, text):
        self.console.append(text)
 
 
    def startServer(self):
        if self._serverThread == None or self._serverThread.isRunning() == False:
            self._serverThread = sRenderServer(self)
            self._serverThread.start()
        else:
            self.output("Server already started")
    
    def stopServer(self):
        if self._serverThread != None and self._serverThread.isRunning() == True:
            self._serverThread.stopServer()
            self._serverThread.terminate()
        else:
            self.output("Server already stopped")
        
    def quitRenderServerUI(self):
        self.stopServer()
        QtCore.QCoreApplication.instance().quit()
    
    
def main():
    app = QtGui.QApplication([])
    ui = sRenderServerUI()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
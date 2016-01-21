import time
import sqlite3

from PySide import QtCore, QtGui

import sPipe.pCore as pc

# Main Widget :: Node editor
# Containt the Node View, menu bar and buttons
class JobPanel(QtGui.QWidget):
    def __init__(self):
        super(JobPanel,self).__init__()
        
        self.database = pc.DATABASEPATH
        
        self.initUI()      

    def initUI(self):
        self._layout = QtGui.QGridLayout(None)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,5,0,5)
        self._layout.setSpacing(0)

        self._topBar = QtGui.QFrame()
        self._topBarLayout = QtGui.QHBoxLayout(self._topBar)
        
        self._refreshProgression = QtGui.QProgressBar()
        self._refreshProgression.setMinimum(0)
        self._refreshProgression.setMaximum(100)
        self._refreshProgression.setValue(10)
        
        self._refreshButton = QtGui.QPushButton("Refresh")
        
        self._filterLabel = QtGui.QLabel("Filter :")
        self._filterField = QtGui.QLineEdit()
        
        self._topBarLayout.addWidget(self._refreshProgression)
        self._topBarLayout.addWidget(self._refreshButton)
        self._topBarLayout.addWidget(self._filterLabel)
        self._topBarLayout.addWidget(self._filterField)

        self.generateJobList()
        
        self._layout.addWidget(self._topBar)
        self._layout.addWidget(self._jobList)
        
        self._autoRefresh = JobListAutoRefresh(self,self._refreshProgression)
        #autoRefresh.run()
        
        self._refreshButton.clicked.connect(self.startRefresh)

    def startRefresh(self):
        self._autoRefresh.start()
    def generateJobList(self):
        self._jobList = QtGui.QTreeWidget()
        self._jobList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self._jobList.setSortingEnabled(True)
        self._jobList.setRootIsDecorated(False)
        
        header = self._jobList.headerItem()
        for i,item in enumerate(["priority","name","user","status"]):
            header.setText(i,item)
    
        self.refreshJobList()
    
    def refreshJobList(self):
        self._jobList.clear()
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row  # Needed to get database as a array
        cur = conn.cursor()
        
        for jobInfo in cur.execute("select * from farm_tasks"):
            item = TreeWidgetItem()
            for i,e in enumerate(jobInfo):
                item.setText(i,str(e))
            self._jobList.addTopLevelItem(item)
            
        self._jobList.sortItems(0,QtCore.Qt.AscendingOrder)
 
 
class JobListAutoRefresh(QtCore.QThread):
    def __init__(self,parent,progressionBar):
        super(JobListAutoRefresh,self).__init__(parent) 
        self._progressionBar = progressionBar
        self._refreshTime = 5
        
    def run(self):
        print "Toto"
        refreshTime = float(time.time())
        #self.exec_()

        while 1:
            ratio = (float(time.time() - refreshTime) / self._refreshTime) * 100.0
            self._progressionBar.setValue(ratio)
            
            if time.time() > refreshTime + self._refreshTime:
                self.parent().refreshJobList()
                refreshTime = time.time()
            time.sleep(1)

# re-implement the QTreeWidgetItem
class TreeWidgetItem(QtGui.QTreeWidgetItem):
    def __lt__(self, otherItem):
        column = self.treeWidget().sortColumn()
        try:
            return float( self.text(column) ) > float( otherItem.text(column) )
        except ValueError:
            return self.text(column) > otherItem.text(column)
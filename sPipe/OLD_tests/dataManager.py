import os
import sqlite3


class DataManager():
    def __init__(self):
        self.jobPath = os.path.abspath(os.getcwd()+"/../jobs")
        self.databaseFile = os.path.abspath(os.getcwd()+"/../data/main.sqlite")
        
        self.defaultJobContent = ["PRODUCTS",
                                 "REFS",
                                 "TASKS",
                                 "TOOLS"                            
                                 ]
        
        self.defaultSqContent = ["PRODUCTS",
                                "REFS",
                                "TASKS",
                                "TOOLS"
                                ]            
        
        self.defaultShotContent = ["anim",
                                "comp",
                                "editing",
                                "fx",
                                "light",
                                "roto",
                                "track",
                                "plate"
                                ]
        
        self.defaultTaskContent = ["maya",
                                "houdini",
                                "nuke"
                                ]

    def checkFolderIntegrity(self,folder=None):
        if folder == None:
            folder = self.jobPath
        
        for item in os.listdir(folder):
            if os.path.isdir(folder+"/"+item):
                self.createDefaultFolder(folder+"/"+item)
                self.checkFolderIntegrity(folder+"/"+item)

    def createDefaultFolder(self,folder=None):
        depth = len(folder.replace(self.jobPath+"/","").split("/"))
        if depth == 1 : defaultFolderToCheck = self.defaultJobContent
        elif depth == 2 : defaultFolderToCheck = self.defaultSqContent
        elif depth == 3 : defaultFolderToCheck = self.defaultShotContent
        elif depth == 4 : defaultFolderToCheck = self.defaultTaskContent
        else : return
        
        for check in defaultFolderToCheck:
            if not os.path.isdir(folder+"/"+check):
                print "Creating "+folder+"/"+check
                os.makedirs(folder+"/"+check)
        return

    def buildArbo(self):
        conn = sqlite3.connect(self.databaseFile)
        cur = conn.cursor()
        
        for taskInfo in cur.execute("SELECT * FROM showTask"):
            path = self.jobPath
            defaultDepth = 5
            for i in range(1,5):
                path = path + "/" + taskInfo[i]
                if not os.path.isdir(path):
                    print "Creating " + path
                    os.makedirs(path)
                    self.createDefaultFolder(path)
                    defaultDepth -= 1
            
            path = self.jobPath
            for i in range(1,defaultDepth):
                path = path + "/" + taskInfo[i]
            self.checkFolderIntegrity(path)
            
        conn.close()

DataManager().buildArbo()
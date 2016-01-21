import sqlite3
import random
import math
import time
import sPipe.pCore as pc


jobName = ["Render","Render","Render","Render","Daily","Daily","Publish","Backup"]
userName = ["sebastien-m","alberto-r","piwi-q","jban-w","carlos-v","marie-d","guillaume-h","tom-l"]





def generateJob():
    jobStructure = ['Playblast','Sim',['IFD','Renders'],'Comp','Daily',['Publish','Sync','Email']]
    jobQuantity = [0.1,1,1,0.5,0.4,0.1]
    jobLenght = [10,100,[10,100],50,30,[15,10,5]]
    userName = ["sebastien-m","alberto-r","piwi-q","jban-w","carlos-v","marie-d","guillaume-h","tom-l"]

    job = None
    taskList = list()
    
    user = userName[random.randint(0,len(userName)-1)]
    
    # Generate serie of task base on the job structure
    firstTask = random.randint(0,len(jobStructure))
    lastTask = firstTask + random.randint(0, len(jobStructure)-firstTask)
    for i in range(firstTask, lastTask):
        quantity = int(math.floor( float(random.randint(1,100))*jobQuantity[i] ))
        
        if type(jobStructure[i]) != type(list()):
            tasks = [jobStructure[i]]
        else:
            tasks = jobStructure[i]
            
        
        dependancyStart = 0
        dependancyStop = 0
        
        for e, task in enumerate(tasks):
            
            
            for n in range(1,quantity+1):
                name = ("%s_%04d" % (task, n))
                
                t = {'name':name, 'user':user,'status':'wait','priority':0,'dependant':[dependancyStart,dependancyStop]}
                taskList.append(t)

            dependancyStart = dependancyStop
            dependancyStop = len(taskList)
    
    for i in taskList:
        print i
    
    
    
    return job, taskList


generateJob()

while 0:
    priority = random.randrange(0,100)
    jn = jobName[random.randint(0,len(jobName)-1)]
    ju = userName[random.randint(0,len(userName)-1)]
    
    
    try:
        conn = sqlite3.connect(pc.DATABASEPATH)
        conn.execute('INSERT INTO farm_tasks (priority, name, user, status) VALUES (%s,"%s","%s","waiting")'%(str(priority),jn,ju))
        conn.commit()
        conn.close()
        time.sleep(15)
    except:
        pass
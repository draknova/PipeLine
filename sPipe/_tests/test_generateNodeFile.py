import json

filePath = "job_01.json"
f = open(filePath,"r")
content = f.read()
f.close()
myStr = content.replace("\n","").replace("\t","")


n1 = {'type':'Box',
     'name':'Box 1',
     'position':[0.0,-100.0],
     'inputs':[],
     'parameters':{'Size':2,
                  'Subdive':4
                  }
     }
n2 = {'type':'Smooth',
     'name':'Smooth 1',
     'position':[50.0,-50.0],
     'inputs':['Box 1'],
     'parameters':{'Lvl':2}
     }
n3 = {'type':'Merge',
     'name':'Merge 1',
     'position':[0.0,0.0],
     'inputs':['Box 1','Smooth 1'],
     'parameters':{}
     }

toWrite = json.dumps([n1,n2,n3], sort_keys=False, indent=4, separators=(',', ': '))

f = open("./job_01.json","w")
f.write(toWrite)
f.close()
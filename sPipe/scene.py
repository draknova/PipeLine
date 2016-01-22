'''
Created on Jan 21, 2016

@author: draknova
'''
#from sPipe.node import OPNode


class OPScene():
    def __init__(self, **kwargs):
        self.opNodeList = list()
        return
    
    def addNode(self, newOPNode):
        self.opNodeList.append(newOPNode)
        return None
        
    def removeNode(self, removedOPNode):
        self.opNodeList.remove(removedOPNode)
        return None
        
    def insertNode(self, index, insertedOPNode):
        self.opNodeList.insert(index, insertedOPNode)
        return None
        
    def nodes(self):
        return self.opNodeList
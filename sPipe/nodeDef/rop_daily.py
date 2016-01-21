class TypeDefinition():
    def __init__(self):
        pass
    
    def exec_(self):
        # What it is doing
        os.system("vlc %s"%(self._fileSequence))
        
        
    def parameters(self):
        self._fileSequence = "/path/to/sequence"
        
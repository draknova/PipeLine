class MyClass():
    def __init__(self, **kwargs):
        self._name = kwargs['name'] if 'name' in kwargs.keys() else None
        self._label = kwargs['label'] if 'label' in kwargs.keys() else None
        print kwargs
        
    def me(self):
        print dir(self)
   
    def __str__(self):
        d = dict()
        for v in vars(self):
            d[v[1:]] = eval("self.%s"%(v))
        return str(d)

    
    
a = MyClass(name="MyName")
b = a
a._name = "test"
print a._name
print b._name
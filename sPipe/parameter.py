# The parameter itself
class ParameterTemplate():
    def __init__(self, **kwargs):    
        self._name = kwargs['name'] if 'name' in kwargs.keys() else None
        self._label = kwargs['label'] if 'label' in kwargs.keys() else self._name
        self._type = kwargs['type'] if 'type' in kwargs.keys() else "float"
        self._value = kwargs['value'] if 'value' in kwargs.keys() else 0.0
        self._hide = kwargs['hide'] if 'hide' in kwargs.keys() else False
        self._lock = kwargs['lock'] if 'lock' in kwargs.keys() else False
        self._join = kwargs['join'] if 'join' in kwargs.keys() else False
        self._defaultValue = kwargs['defaultValue'] if 'defaultValue' in kwargs.keys() else 0.0
        self._minValue = kwargs['minValue'] if 'minValue' in kwargs.keys() else 0.0
        self._maxValue = kwargs['maxValue'] if 'maxValue' in kwargs.keys() else 1.0
        self._expression = kwargs['expression'] if 'expression' in kwargs.keys() else None
        self._lockCondition = kwargs['lockCondition'] if 'lockCondition' in kwargs.keys() else None
        self._hideCondition = kwargs['hideCondition'] if 'hideCondition' in kwargs.keys() else None
        self._callback = kwargs['callback'] if 'callback' in kwargs.keys() else None
        self._helpcard = kwargs['helpcard'] if 'helpcard' in kwargs.keys() else None
        
    # Value return when object is call for print
    def __str__(self):
        d = dict()
        for v in vars(self):
            if v[0] == "_":
                d[v[1:]] = eval("self.%s"%(v))
        return str(d)
        
    def name(self):
        return self._name
    
    def setName(self, newName):
        self._name = newName
        return self._name
    
    def value(self):
        return self._value
    
    def setValue(self, newValue):
        self._value = newValue
        return self._value
    
    def eval(self):
        return self._value
    
    def label(self):
        return self._label
    
    def setLabel(self, newLabel):
        self._label = newLabel
    
    def setExpression(self, expression):
        return None
     
    def isExpression(self):
        if self._expression != "":
            return False
        else:
            return True
    
    def type(self):
        return self._type
    

class ParameterTemplateGroup():
    def __init__(self):
        self._parameterList = list()
        
    def parameters(self):
        return self._parameterList
    
    def addParameter(self, parameter):
        self._parameterList.append(parameter)
        
    def removeParameter(self, parameter):
        self._parameterList.remove(parameter)
        
    def insertParameter(self, index, parameter):
        self._parameterList.insert(index, parameter)


class IntParameterTemplate(ParameterTemplate):
    def __ini__(self, **kwargs):
        kwargs['type'] = 'int'
        super(FloatParameterTemplate, self).__init__(kwargs)
 
    
class FloatParameterTemplate(ParameterTemplate):
    def __ini__(self, **kwargs):
        kwargs['type'] = 'float'
        super(FloatParameterTemplate, self).__init__(kwargs)


class StringParameterTemplate(ParameterTemplate):
    def __ini__(self, **kwargs):
        kwargs['type'] = 'string'
        super(FloatParameterTemplate, self).__init__(kwargs)        
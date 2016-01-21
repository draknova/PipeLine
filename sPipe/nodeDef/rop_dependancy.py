from sPipe.node import OPNode
from sPipe.parameter import IntParameterTemplate

class ROP_Dependancy(OPNode):
    def __init__(self):
        OPNode.__init__(self)
        
    def __parameter__(self):
        dependancyParameter = IntParameterTemplate(name="dependancy", label="Dependancy", value="0")
        self._parmTemplateGroup.addParameter(dependancyParameter)
        
    def __exec__(self):
        print "Checking that my inputs are ended"
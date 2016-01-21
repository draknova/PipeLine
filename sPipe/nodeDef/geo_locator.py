from sPipe.node import OPNode
from sPipe.parameter import *

class GEO_locator(OPNode):
    def __init__(self, **kwargs):
        OPNode.__init__(self, name="Test")
        self.__parameter__()
        
    def __parameter__(self):
        tx = FloatParameterTemplate(name="tx",label="Translate X")
        ty = FloatParameterTemplate(name="ty",label="Translate Y")
        tz = FloatParameterTemplate(name="tz",label="Translate Z")
        self._parmTemplateGroup.addParameter(tx)
        self._parmTemplateGroup.addParameter(ty)
        self._parmTemplateGroup.addParameter(tz)
    
    def __exec__(self):
        # This define the action the geometry the operactor can do.
        print "Hello World"

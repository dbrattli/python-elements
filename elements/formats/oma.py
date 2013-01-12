from elements import Element, Attribute, SelfElement

class Parameter(Element):
    _tag = 'parm'

    name = Attribute()
    value = Attribute()

class Characteristic(Element):
    _tag = 'characteristic'

    type = Attribute()
    
    parm = Parameter()

    characteristic = SelfElement()
    
class WapProvisioningDoc(Element):
    _tag = 'wap-provisioningdoc'

    version = Attribute()
    characteristic = Characteristic()



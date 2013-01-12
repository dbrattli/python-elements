from elements import Elements

NS1 = "ns1"
NS2 = "ns2"

xml_string = """
<message xmlns="ns1">
  <datastore1 xmlns="ns2">
    <name>Contacts</name>
    <id>c085403c-eb41-11dc-a5cd-0017f2c50bd8</id>
   </datastore1>
  <datastore2 xmlns="ns2">
    <name>Calendar</name>
    <id>c8175380-eb41-11dc-a5cd-0017f2c50bd8</id>
   </datastore2>
</message>  
"""

class Datastore1(Elements):
    _tag = 'datastore1'
    _namespace = NS2

    _children = Elements._children.copy()

    _children['name'] = ('name', unicode)
    _children['id'] = ('id', unicode)

    def __init__(self, name=False, id=False, text=None):
        self.name = name
        self.id = id
        self.text = text

class Datastore2(Elements):
    _tag = 'datastore2'
    _namespace = NS2

    _children = Elements._children.copy()

    _children['{%s}name' % NS2] = ('name', unicode)
    _children['id'] = ('id', unicode)

    def __init__(self, name=False, id=False, text=None):
        self.name = name
        self.id = id
        self.text = text

class Message(Elements):
    _tag = 'message'
    _namespace = NS1

    _children = Elements._children.copy()
    _children['{%s}datastore1' % NS2] = ('datastores1', { 'name' : Datastore1 })
    _children['{%s}datastore2' % NS2] = ('datastores2', { '{%s}name' % NS2 : Datastore2 })
    
    def __init__(self, datastores1=False, datastores2=False, text=None):
        self.datastores1 = datastores1 or {}
        self.datastores2 = datastores2 or {}
        self.text = text

def test_dictionaries():
    global xml_string
    
    e = Message()
    e.from_string(xml_string)
    print e.datastores1

    assert e.datastores1['Contacts'].id == 'c085403c-eb41-11dc-a5cd-0017f2c50bd8'
    assert e.datastores2['Calendar'].id == 'c8175380-eb41-11dc-a5cd-0017f2c50bd8'
    print e.to_string()

if __name__ == '__main__':
	test_dictionaries()
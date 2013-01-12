from elements2 import Element, TextElement

NS1 = "ns1"
NS2 = "ns2"
NS3 = "ns3"

xml_string = """
<datastore xmlns="ns1">
    <name>Dag Brattli</name>
    <myname xmlns="ns3">Dag Brattli</myname>
</datastore>
"""

class Datastore(Elements):
  _tag = 'datastore'
  _namespaces = [NS1, NS2]

  name = TextElement()

class MyDatastore(Datastore):  

  my_name = TextElement(name="myname", namespace=NS3)

def test_namespaces():
    global xml_string
    
    e = MyDatastore()
    e.from_string(xml_string)
    print e
    assert e.name == 'Dag Brattli'
    assert e.my_name == 'Dag Brattli'
    
    xml_string = e.to_string()
    print xml_string
    e = MyDatastore()
    e.from_string(xml_string)

    assert e.name == 'Dag Brattli'
    assert e.my_name == 'Dag Brattli'

if __name__ == '__main__':
    test_namespaces()
from elements import Element, TextElement

NS1 = "ns1"
NS2 = "ns2"

xml_string = """
<datastore xmlns="ns1">
    <name>Dag Brattli</name>
    <myname xmlns="ns2">Dag Brattli</myname>
</datastore>
"""

class Datastore(Element):
  _tag = 'datastore'
  _namespace = NS1
  
  name = TextElement()#namespace=NS1)

class MyDatastore(Datastore):
    
    my_name = TextElement(tag="myname", namespace=NS2)

def test_namespaces():
    global xml_string

    e = MyDatastore()
    e.from_string(xml_string)
    
    print e.name
    assert e.name == 'Dag Brattli'
    
    print "##########################"
    print e.my_name
    return
    assert e.my_name == 'Dag Brattli'
    print "##########################"
    
    xml_string = e.to_string()
    e = MyDatastore()
    e.from_string(xml_string)

    assert e.name == 'Dag Brattli'
    assert e.my_name == 'Dag Brattli'

if __name__ == '__main__':
	test_namespaces()
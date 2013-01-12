from elements import Element, IntegerElement, Attribute

import sys
import logging

logging.basicConfig(level=logging.WARNING)

xml_string = """
<message version="1.2">
    <integer version="1.2">12</integer>
</message>
"""

class MyInteger(IntegerElement):
    version = Attribute()

class Message(Element):
    _tag = 'message'

    version = Attribute(default="1.5")
  
    myint = MyInteger(tag="integer")

def test_attributes():
    global xml_string
    e = Message()
    e.from_string(xml_string)
    print e.to_string()
    print e.myint
    
    assert type(e.myint) == int
    assert e.myint == 12
    
    print "################"
    print e['myint']
    print e['myint'].version
    print "################"
    assert type(e.version) == unicode
    assert e.version == "1.2"
    e.version = "1.3"
    print e.to_string()

    for val in [-1, 0, 1, 1000, 9999, sys.maxint]:
        e = Message()
        e.myint=val
        xml_string = e.to_string()
        print xml_string
        e = Message()
        e.from_string(xml_string) # Parse our own output
        assert e.myint == val
        assert e.version == "1.5"
        
if __name__ == '__main__':
	test_attributes()
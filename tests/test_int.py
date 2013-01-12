from elements import Element, IntegerElement

import sys

xml_string = """
<message>
    <integer>12</integer>
</message>
"""

class Message(Element):
    _tag = 'message'
  
    myint = IntegerElement(tag="integer")

def test_int():
    # e = Message()
    # e.myint=10
    # xml_string = e.to_string()
    # print xml_string    
    # return
    # 
    global xml_string
    e = Message.from_string(xml_string)

    assert e.myint == 12
    assert type(e.myint) == int

    for val in [-1, 0, 1, 1000, 9999, sys.maxint]:
        e = Message()
        xml_string = e.to_string()
        print "xml_string"
        print xml_string
        e.myint=val
        print e.myint
        xml_string = e.to_string()
        print "xml_string"
        print xml_string
        
        e = Message.from_string(xml_string) # Parse our own output
        assert e.myint == val
        
if __name__ == '__main__':
    test_int()
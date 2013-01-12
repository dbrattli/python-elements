from elements import Element, IntegerElement, ListElement

import sys

xml_string = """
<message>
    <integer>1</integer>
    <integer>2</integer>
    <integer>3</integer>
    <integer>4</integer>
</message>
"""

#
# >>> m = Message()
# >>> m.from_string()
# 
# >>> m.myints
# [IntegerElement(), ...]
#
# >>> m.myints[0].value
# 1

# >>> int(m.myints)
# 1

print "######################################"
class Message(Element):
  _tag = 'message'
 
  myints = ListElement(IntegerElement(tag="integer"))

def test_int_list():
    global xml_string
    e = Message.from_string(xml_string)
    print e.to_string()
    a = e.myints
    print "a=", a
    print a[0]
    assert e.myints == [1,2,3,4]
    assert isinstance(e.myints, list)

    # Contruct a new list
    val = [-1, 0, 1]
    e = Message()
    e.myints=val
    xml_string = e.to_string()
    print xml_string
    
    # Parse our own output
    e = Message.from_string(xml_string) 
    assert e.myints == val
        
if __name__ == '__main__':
    test_int_list()
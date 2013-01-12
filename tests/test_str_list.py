from elements import Element, TextElement, ListElement

import sys

xml_string = """
<message>
    <string>one</string>
    <string>two</string>
    <string>three</string>
    <string>four</string>
</message>
"""

class Message(Element):
    _tag = 'message'
  
    mystring = ListElement(TextElement(tag="string"))

def test_str_list():
    global xml_string
    e = Message.from_string(xml_string)
    
    print e.mystring
    assert e.mystring == ["one","two","three","four"]
    assert type(e.mystring) == list

    # Contruct a new list
    val = ["one", "two", "three"]
    e = Message()
    e.mystring=val
    xml_string = e.to_string()
    
    # Parse our own output
    e = Message.from_string(xml_string) 
    assert e.mystring == val
        
if __name__ == '__main__':
	test_str_list()
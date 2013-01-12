from elements import Element, BoolElement

xml_string1 = """
<message>
	<last/>
</message>
"""

xml_string2 = """
<message>
</message>
"""

class Message(Element):
  _tag = 'message'
  
  last = BoolElement(default=False)
  
def test_bool():
    e = Message.from_string(xml_string1)
    
    assert e.last == True
    assert type(e.last) == bool

    e = Message.from_string(xml_string2)

    assert e.last == False

    for truth in [True, False]:
        e = Message()
        e.last = truth
        xml_string = e.to_string()
        print xml_string
        e = Message.from_string(xml_string)
        
        print "e.last", e.last
        assert e.last == truth
        
if __name__ == '__main__':
	test_bool()
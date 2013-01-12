from elements import Element, TextElement

xml_string = """
<name>
    <firstname>Dag</firstname>
    <lastname>Brattli \xc3\xb8</lastname>
</name>
"""

class Name(Element):
  _tag = 'name'

  first_name = TextElement(tag="firstname")
  last_name = TextElement(tag="lastname")

def test_strings():
    e = Name.from_string(xml_string)
    
    print repr(e.first_name)
    assert e.first_name == 'Dag'
    #assert type(e.first_name) == str
    
    print repr(e.last_name)
    assert e.last_name == u'Brattli \xf8'
    assert type(e.last_name) == unicode
    
    # Now we parse our own output
    new_xml = e.to_string()
    e = Name.from_string(new_xml)

    print repr(e.first_name)
    assert e.first_name == 'Dag'
    #assert type(e.first_name) == str
    
    print repr(e.last_name)
    assert e.last_name == u'Brattli \xf8'
    assert type(e.last_name) == unicode

if __name__ == '__main__':
	test_strings()
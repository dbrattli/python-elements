from elements import Elements

# Import ElementTree API. You can override it by setting the ET class member
try:
    from xml.etree import cElementTree as ET
except ImportError:
    try:
        import cElementTree as ET
    except ImportError:
        from elementtree import ET


xml_string = """
<name>
	<middle>R</middle>
	<last>Brattli</last>
	<first>Dag</first>
</name>
"""

class Name(Elements):
    _tag = 'name'
    _children = Elements._children.copy()    
  
    _children['first'] = ('first', str)
    _children['middle'] = ('middle', str)
    _children['last'] = ('last', str)

    def __init__(self, first=None, middle=None, last=None, text=None):
        # This is the order we want on our output 
        self.first = None 
        self.middle = None
        self.last = None

        self.text = None

def test_strings():
    global xml_string
    e = Name()
    e.from_string(xml_string)
    
    ret = e.to_string()
    tree = ET.XML(ret)
    order = [elem.tag for elem in tree]
    assert order == ['first', 'middle', 'last']
    
if __name__ == '__main__':
	test_strings()
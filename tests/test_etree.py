import sys

from elements import Elements

try:
    from xml.etree import cElementTree as ET
except ImportError:
    try:
        import cElementTree as ET
    except ImportError:
        from elementtree import ET


xml_string = """
<message>
    <body format="html">
      <html xmlns="http://www.w3.org/1999/xhtml">
        <p>This is a test</p>
      </html>
    </body>
</message>
"""

class Message(Elements):
  _tag = 'message'
  _children = Elements._children.copy()    
  
  _children['body'] = ('body', ET.ElementTree)

  def __init__(self, body=False, text=None):
    self.body = body
    self.text = text

def test_etree():
    global xml_string
    e = Message()
    e.from_string(xml_string)
    
    root = e.body.getroot()
    assert ET.iselement(root)
    
    p = root.findtext("{http://www.w3.org/1999/xhtml}p")
    assert p == "This is a test"
    
    print e.to_string()

        
if __name__ == '__main__':
    test_etree()
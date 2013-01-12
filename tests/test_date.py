from elements2 import Element, DateElement, DateTimeElement

from datetime import datetime
import dateutil.tz

xml_string = """
<message>
	<date>2003-12-13T18:30:02Z</date>
</message>
"""

class Message(Element):
    _tag = 'message'
  
    date = DateTimeElement(tag="date")#, format='%Y-%m-%dT%H:%M:%S.000%Z')

def test_date():
    e = Message()
    e.from_string(xml_string)
    
    print repr(e.date)
    assert e.date == datetime(year=2003, month=12, day=13, hour=18, minute=30, second=2, tzinfo=dateutil.tz.tzutc())
    assert type(e.date) == datetime
    
    print e.to_string()

#    for date in [,]:
#       e = Message(last=truth)
#        xml_string = e.to_string()
#        e = Message()
#        e.from_string(xml_string)
#        assert e.last == truth
        
if __name__ == '__main__':
	test_date()
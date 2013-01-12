# python-elements

## What is Elements

Elements is a [http://www.python.org Python] library that provides simple parsing from XML to Python objects and back. It uses the well known [http://effbot.org/zone/element-index.htm ElementTree] API to parse XML into Python objects. !ElementTrees are very nice for parsing XML, but sometimes you want something even closer to Python. You want the XML to "magically" fill out your Python objects, and be able to access your values using dotted notation. This is what Elements does for you. Elements is similar to [http://codespeak.net/lxml/objectify.html lxml.objectify] and [http://www.xml3k.org/Amara2/Tutorial#TheXMLbindery Amara2 Bindery].

However, Elements does not work well for all kinds of XML documents. It's a compromise. It's very good for parsing XML over HTTP based protocols such as [http://en.wikipedia.org/wiki/Atom_(standard) Atom], but may not work well for you when the ordering of the elements is significant such as for XHTML or Apple Property Lists (PList). At first you might get the feeling of over-engineering when looking at Elements, but once your classes are defined, you will feel and enjoy the power of the this library. 

## History

Most of the idea, design and code has been taken from the [http://code.google.com/p/couchdb-python/ CouchDB Python Library]. They have made a fantastic implementation of their [http://code.google.com/p/couchdb-python/source/browse/couchdb/mapping.py Schema/Mapping] which is a higher-level API for mapping between CouchDB documents and Python objects. With Elements v2 we are using the same design to parse and generate XML documents.

Elements v1 was based on the Atom parser of the [http://code.google.com/p/gdata-python-client/ gdata-python-client library]. I really liked the idea and wanted to make it easy to use with other applications and for other XML formats as well. Elements v1 works well but the class declarations are quite verbose. 

## Source

To browse the Elements library source code, visit the (GitHub)[https://github.com/dbrattli/python-elements].

## Example

A simple example. Lets say you want to parse the following XML document:

```xml
<Example version="1.0">
    <Name>Dag Brattli</Name>
    <Age>39</Age>
    <Hacker/>
</Example>
```

With Elements you have to declare a Python class for storing the information you are interested in. Unspecified elements and attributes will be ignored by the parser.

```python
from elements import Element

class Example(Element):
    _tag = 'Example'

    version = TextAttribute()

    hacker = BoolElement(tag="Hacker")
    name = TextElement(name="Name")
    age = IntegerElement(name="Age"))    
```

Now you are ready for some action:

```python
>>> e = Example.from_string(example) # The XML doc above
>>> print e.name
Dag Brattli
>>> print e.age
39
>>> print e.hacker
True
```

Nice! There are many other and more advanced features ...

Enjoy

*Dag Brattli*
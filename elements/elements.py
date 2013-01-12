# -*- coding: utf-8 -*-
#
# Copyrigth (C) 2010 Dag Brattli
# Copyright (C) 2007-2009 Christopher Lenz (couchdb-python)
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

"""Mapping from raw XML documents to Python objects and vice versa.

>>> from elements import Element, TextElement, IntegerElement

To define a document schema, you declare a Python class inherited from
`Element`, and add any number of `LeafElement` attributes:

>>> class Person(Element):
...     name = TextElement()
...     age = IntegerElement()
...     added = DateTimeField(default=datetime.now)
>>> person = Person(tag='person', name='John Doe', age=42)
>>> person
<__main__.Person object at ...>
>>> person.age
42
>>> print person.to_string()
<person>
  <age>42</age>
  <added>2010-02-20T12:08:37Z</added>
  <name>John Doe</name>
</person>

You can then load XML data through your `Element` subclass, and conveniently 
access all attributes:

>>> xml_string = "<person>\
... <age>40</age>\
... <added>2010-02-20T13:08:38Z</added>\
... <name>Jane Doe</name>\
... </person>"
>>> person = Person.from_string(xml_string)
>>> person.name
u'Jane Doe'
>>> person.age
40
>>> person.added
datetime.datetime(...)

"""

from calendar import timegm
from datetime import date, datetime, time
from decimal import Decimal
from time import strptime, struct_time

import util

try:
    from xml.etree import cElementTree as ET
except ImportError:
    try:
        import cElementTree as ET
    except ImportError:
        try:
            from xml.etree import ElementTree as ET
        except ImportError:
            from elementtree import ElementTree as ET

class AttrList(list):
    def __getattr__(self, name):
        try:
            value = getattr(self[0], name)
        except IndexError:
            raise AttributeError
        return value

    def __setattr__(self, name, value):
        """Called when somebody wants to access the first item in the list
        directly as an attribute. Thus we forward the request to the first
        object in the list
        """
        try:
            setattr(self[0], name, value)
        except IndexError:
            raise AttributeError

class SuperElement(object):
    """A base class for Elements. Used to avoid circular reference in
    ElementsMeta:__new__(). This class should never be instantiated."""
    
class ElementsMeta(type):
    def __new__(cls, name, bases, d):
        
        fields = {}
        for base in bases:
            if hasattr(base, '_fields'):
                fields.update(base._fields)
        for attrname, attrval in d.items():
            if isinstance(attrval, SuperElement):
                # Fix children that haven't got a name and etree yet
                if not attrval._tag:
                    attrval._tag = attrname
                    attrval._etree = ET.Element(attrname)
                fields[attrname] = attrval

        d['_fields'] = fields
        return type.__new__(cls, name, bases, d)

class Element(SuperElement):
    __metaclass__ = ElementsMeta
    
    def __init__(self, tag=None, namespace=None, **values):
        if tag or not hasattr(self, "_tag"):
            self._tag = tag

        if namespace or not hasattr(self, "_namespace"):
            self._namespace = namespace

        self._etree = ET.Element(self._tag or self.__class__.__name__)

        # Set user supplied values or use defaults
        for attrname, field in self._fields.items():
            if attrname in values:
                setattr(self, attrname, values.pop(attrname))
            else:
                setattr(self, attrname, getattr(self, attrname))

    def get_qname(self, parent=None):
        if self._namespace:
            qname = "{%s}%s" % (self._namespace, self._tag)
        elif parent and parent._namespace:
            self._namespace = parent._namespace
            qname = "{%s}%s" % (parent._namespace, self._tag)
        else:
            qname = self._tag
        return qname
        
    def __getitem__(self, key):
        """Called when we are an object attribute"""
    
        # Return Element object
        obj = self._fields[key]
        qname = obj.get_qname(parent=self)
        elem = self._etree.find(qname)
        #obj.from_elementtree(elem)
        obj._etree = elem
        
        return obj
        
    def __setitem__(self, key, value):
        raise NotImplementedError
            
    def __get__(self, instance, owner):
        """Called when we are a class attribute"""
        
        if instance is None:
            return self

        ret = AttrList()
        qname = self.get_qname(parent=instance)
        elems = instance._etree.findall(qname)
        for elem in elems:
            if isinstance(self, SelfElement):
                new = instance.__class__(tag=self._tag,
                                         namespace=self._namespace)
            else:
                new = self.__class__(tag=self._tag,
                                     namespace=self._namespace)
#            new._fields.update(self._fields)
            #new.from_elementtree(elem)
            new._etree = elem
            ret.append(new)
            
        return ret

    def __set__(self, instance, value):
        """Called when we are a class attribute"""
        
        if value is not None:
             value = self._to_xml(value)
        
        qname = self.get_qname(parent=instance)
        elem = instance._etree.find(qname)
        if elem is None:
            elem = ET.Element(qname)
            instance._etree.append(elem)
        elem.text = value
        
    def _to_python(self, value):
        return value

    def _to_xml(self, value):
        return unicode(value)

    @classmethod
    def from_elementtree(cls, etree):
        instance = cls()
        instance._etree = etree
        return instance        

    def to_elementtree(self):
        return self._etree
    
    @classmethod
    def from_string(cls, xml_string, encoding=None):
        """Parse XML string into an Element object. Assumes the string
        is unicode or ascii. If not, specify the encoding"""
                
        if encoding:
            xml_string = xml_string.decode(encoding).encode('utf-8')
        
        tree = ET.fromstring(xml_string)
        return cls.from_elementtree(tree)
    
    @classmethod
    def from_file(cls, filename, encoding='utf-8'):
        """Parse XML file into an Element object. Assumes the content is 
        utf-8. If not, then specify the encoding"""
        
        f = open(filename)
        ret = cls.from_string(f.read(), encoding)
        f.close()
        return ret
     
    def to_string(self, encoding=None, indent=True, use_default_ns=True):
        """Convert this Elements object to XML string"""
        
        etree = self.to_elementtree()
        if indent:
            util.indent(etree)
        if use_default_ns:
            util.use_default_ns(etree)
        return ET.tostring(element=etree, encoding=encoding)

class SelfElement(Element):
    """Used when decaring an Element as the same class as its parent to
    avoid circular referencing.
    """

class LeafElement(Element):
    """Basic unit for mapping a piece of data between Python and XML.
    
    Instances of this class can be added to subclasses of `Element` to describe
    the schema of an element.
    """
    def __init__(self, tag=None, namespace=None, default=None, **values):
        Element.__init__(self, tag, namespace, **values)
        
        if default or not hasattr(self, "_default"):
            self._default = default
        
    def __get__(self, instance, owner):
        """Called when we are a class attribute"""
        
        if instance is None:
            return self
                
        qname = self.get_qname(parent=instance)
        value = instance._etree.findtext(qname)
        if value is not None:
            value = self._to_python(value)
        elif self._default is not None:
            default = self._default
            if callable(default):
                default = default()
            value = default

        return value
        
    def __set__(self, instance, value):
        if value is not None:
             value = self._to_xml(value)

        qname = self.get_qname(parent=instance)
        elem = instance._etree.find(qname)
        if elem is None:
            elem = ET.Element(qname)
            instance._etree.append(elem)
        elem.text = value
        
    def _to_python(self, value):
        return unicode(value)

TextElement = LeafElement

class Attribute(LeafElement):

    def __init__(self, name=None, namespace=None, default=None, **values):
        LeafElement.__init__(self, tag=name, namespace=namespace, **values)

    def __get__(self, instance, owner):
        """Called when we are a class attribute"""
        
        if instance is None:
            return self
        
        qname = self.get_qname()
        value = instance._etree.attrib.get(qname)
        if value is not None:
            value = self._to_python(value)
        elif self._default is not None:
            default = self._default
            if callable(default):
                default = default()
            value = default

        return self._to_python(value)
        
    def __set__(self, instance, value):
        if value is not None:
             value = self._to_xml(value)

        qname = self.get_qname()
        instance._etree.attrib[qname] = value
        
    def _to_python(self, value):
        return unicode(value)

    def _to_xml(self, value):
        return unicode(value)

TextAttribute = Attribute
                
class BoolElement(LeafElement):
    def _to_python(self, value):
        if not value is None:
            return True
        return False
        
    def _to_xml(self, value):
        return value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        qname = self.get_qname(parent=instance)
        value = instance._etree.find(qname)
        return self._to_python(value)

    def __set__(self, instance, value):
        if value is not None:
            value = self._to_xml(value)

        qname = self.get_qname(parent=instance)
        elem = instance._etree.find(qname)
        if (not elem is None) and not value:
            instance._etree.remove(elem)
        elif (elem is None) and value:
            elem = ET.Element(qname)
            instance._etree.append(elem)
        
class IntegerElement(LeafElement):
    _to_python = int

class FloatElement(LeafElement):
    _to_python = float

class DateElement(LeafElement):
    def _to_python(self, value):
        if isinstance(value, basestring):
            try:
                value = date(*strptime(value, '%Y-%m-%d')[:3])
            except ValueError, e:
                raise ValueError('Invalid ISO date %r' % value)
        return value

    def _to_xml(self, value):
        if isinstance(value, datetime):
            value = value.date()
        return value.isoformat()
 
class DateTimeElement(LeafElement):
    """Element for storing date/time values.

    >>> element = DateTimeElement()
    >>> element._to_python('2007-04-01T15:30:00Z')
    datetime.datetime(2007, 4, 1, 15, 30)
    >>> element._to_xml(datetime(2007, 4, 1, 15, 30, 0, 9876))
    '2007-04-01T15:30:00Z'
    >>> element._to_xml(date(2007, 4, 1))
    '2007-04-01T00:00:00Z'
    """

    def _to_python(self, value):
        if isinstance(value, basestring):
            try:
                value = value.split('.', 1)[0] # strip out microseconds
                value = value.rstrip('Z') # remove timezone separator
                timestamp = timegm(strptime(value, '%Y-%m-%dT%H:%M:%S'))
                value = datetime.utcfromtimestamp(timestamp)
            except ValueError, e:
                raise ValueError('Invalid ISO date/time %r' % value)
        return value

    def _to_xml(self, value):
        if isinstance(value, struct_time):
            value = datetime.utcfromtimestamp(timegm(value))
        elif not isinstance(value, datetime):
            value = datetime.combine(value, time(0))
        return value.replace(microsecond=0).isoformat() + 'Z'
    
class ListElement(LeafElement):
    def __init__(self, elem, tag=None, default=None):
        LeafElement.__init__(self, tag=tag, default=default or [])
        
        self.elem = elem

    def __get__(self, instance, owner):
        """Called when we are a class attribute"""
        
        if instance is None:
            return self
        
        qname = self.elem.get_qname(parent=instance)
        elems = instance._etree.findall(qname)
        return [self.elem._to_python(elem.text) for elem in elems]

    def __set__(self, instance, values):
        if values:
            values = self._to_xml(values)
        
        qname = self.elem.get_qname(parent=instance)
        for value in values:
            #elems = instance._etree.find(name) # FIXME: replace existing elements?
            elem = ET.Element(qname)
            instance._etree.append(elem)

            elem.text = value

    def _to_python(self, value):
        return self.Proxy(value, self.elem)

    def _to_xml(self, value):
        return [self.elem._to_xml(item) for item in value]

    class Proxy(list):

        def __init__(self, list, field):
            self.list = list
            self.field = field

        def __lt__(self, other):
            return self.list < other

        def __le__(self, other):
            return self.list <= other

        def __eq__(self, other):
            return self.list == other

        def __ne__(self, other):
            return self.list != other

        def __gt__(self, other):
            return self.list > other

        def __ge__(self, other):
            return self.list >= other

        def __repr__(self):
            return repr(self.list)

        def __str__(self):
            return str(self.list)

        def __unicode__(self):
            return unicode(self.list)

        def __delitem__(self, index):
            del self.list[index]

        def __getitem__(self, index):
            return self.field._to_python(self.list[index])

        def __setitem__(self, index, value):
            self.list[index] = self.field._to_xml(value)

        def __delslice__(self, i, j):
            del self.list[i:j]

        def __getslice__(self, i, j):
            return ListElement.Proxy(self.list[i:j], self.field)

        def __setslice__(self, i, j, seq):
            self.list[i:j] = (self.field._to_xml(v) for v in seq)

        def __contains__(self, value):
            for item in self.list:
                if self.field._to_python(item) == value:
                    return True
            return False

        def __iter__(self):
            for index in range(len(self)):
                yield self[index]

        def __len__(self):
            return len(self.list)

        def __nonzero__(self):
            return bool(self.list)

        def append(self, *args, **kwargs):
            if args or not isinstance(self.field, DictElement):
                if len(args) != 1:
                    raise TypeError('append() takes exactly one argument '
                                    '(%s given)' % len(args))
                value = args[0]
            else:
                value = kwargs
            self.list.append(self.field._to_xml(value))

        def count(self, value):
            return [i for i in self].count(value)

        def extend(self, list):
            for item in list:
                self.append(item)

        def index(self, value):
            return self.list.index(self.field._to_xml(value))

        def insert(self, idx, *args, **kwargs):
            if args or not isinstance(self.field, DictElement):
                if len(args) != 1:
                    raise TypeError('insert() takes exactly 2 arguments '
                                    '(%s given)' % len(args))
                value = args[0]
            else:
                value = kwargs
            self.list.insert(idx, self.field._to_xml(value))

        def remove(self, value):
            return self.list.remove(self.field._to_xml(value))

        def pop(self, *args):
            return self.field._to_python(self.list.pop(*args))

#
# Copyright (C) 2008 Dag Brattli, ObexCode
#
# Portions copyright 2007 Google Inc. (GData Python Client Library)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Import ElementTree API in mysterious ways
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

def indent(elem, level=0, spaces="  "):
    """In-place ElementTree indenter for pretty printing of ElementTrees.
    
    It's a modified version of ElementLib:indent() to get the output as I want
    it.
    """

    i = "\n" + level*spaces
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + spaces
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def use_default_ns(elem, default_ns=None):
    """In-place ElementTree namespace rewriter 
    
    Puts default namespaces in element attributes, and removes the namespace 
    uri from the tag name. This is very good for getting human readable output 
    for printing.
    """
    
    if elem.tag[0] == '{':
        ns, tag = elem.tag[1:].split("}", 1)
        if ns != default_ns:
            elem.attrib['xmlns'] = ns
            default_ns = ns
        elem.tag = tag
    for elem in elem:
        use_default_ns(elem, default_ns)
        
if __name__ == '__main__':
    import sys
    import copy
    f = open(sys.argv[1])
    e = ET.fromstring(f.read())
    e2 = copy.deepcopy(e)
    use_default_ns(e2)
    indent(e2)
    print "*** Default print output ***"
    print ET.tostring(e)
    print "*** Indented and namespace cleanup ***"
    print ET.tostring(e2)
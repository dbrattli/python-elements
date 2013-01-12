#!/usr/bin/env python
# encoding: utf-8
"""
test_atom.py

Created by Dag Brattli on 2008-03-02.
Copyright (c) 2008, Dag Brattli, All rights reserved.
"""

import sys
import os
import logging

from elements import atom

logging.basicConfig(level=logging.WARNING)

EXAMPLE_NAMESPACE = "http://schemas.example.com/example"

class MyUrl(atom.Link):
    _namespace = EXAMPLE_NAMESPACE
    _tag = "my_url"
    
    _children = atom.Link.copy_children()
    _attributes = atom.Link._attributes.copy()

    _namespace_aliases = atom.Link._namespace_aliases.copy()
    _namespace_aliases[EXAMPLE_NAMESPACE] = 'ex'

class MyEntry(atom.Entry):
    _children = atom.Entry.copy_children()
    _attributes = atom.Entry._attributes.copy()

    _namespace_aliases = atom.Entry._namespace_aliases.copy()
    _namespace_aliases[EXAMPLE_NAMESPACE] = 'ex'
    
    _children['{%s}my_url' % EXAMPLE_NAMESPACE] = ('my_url', MyUrl)
    
    def __init__(self, my_url=None, **kwargs):
        super(MyEntry, self).__init__(**kwargs)

        self.my_url = my_url

def test_atom():
    url = MyUrl(href="http://www.example.com")
    d = MyEntry(my_url=url)
    
    x = d.to_dict()
    assert(x['entry']['ex$my_url']['href'] == "http://www.example.com")

    j = d.to_json()
    
    entry = MyEntry()
    entry.from_dict(x)
    assert(entry.my_url.href == "http://www.example.com")

if __name__ == '__main__':
	test_atom()


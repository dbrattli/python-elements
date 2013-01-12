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

logging.basicConfig(level=logging.WARNING)

from elements import atom

def test_atom(filenames=None):
    filenames = filenames or ["tests/atom.xml", "tests/atom_old_app.xml"]
    for filename in filenames:
        data = open(filename).read()
        d = atom.Feed()
        d.from_string(data)
    
        print d.to_string()

        # Render as verbose dict
        x = d.to_dict()
        print x
        assert(x['feed']['title']['$t'] == "Example Feed")
        assert(x['feed']['entry'][0]['summary']['$t'] == "Some text.")
        assert(x['feed']['entry'][0]['link'][0]['href'] == "http://example.org/2003/12/13/atom03")
        assert(x['feed']['entry'][0]['app$control']['app$draft']['$t'] == "Testing Draft")

        # Render as compact dict
        y = d.to_dict(compact=True)
#        print y
        assert(y['feed']['title'] == "Example Feed")
        assert(y['feed']['entry'][0]['summary'] == "Some text.")
        assert(y['feed']['entry'][0]['link'][0]['href'] == "http://example.org/2003/12/13/atom03")
        assert(y['feed']['entry'][0]['app$control']['app$draft'] == "Testing Draft")

    #    j = d.to_json()
    #    print j
    
        # Parse verbose dict
        d = atom.Feed()
        d.from_dict(x)
        print d.to_string()
        assert(d.title.text == "Example Feed")
        assert(d.entry[0].summary.text == "Some text.")
        assert(d.entry[0].link[0].href == "http://example.org/2003/12/13/atom03")
        assert(d.entry[0].control.draft.text == "Testing Draft")
        
        # Parse compact dict
        d = atom.Feed()
        d.from_dict(y)
    ##    print d.to_string()
        assert(d.title.text == "Example Feed")
        assert(d.entry[0].summary.text == "Some text.")
        assert(d.entry[0].link[0].href == "http://example.org/2003/12/13/atom03")
        assert(d.entry[0].control.draft.text == "Testing Draft")

if __name__ == '__main__':
	test_atom(["atom.xml", "atom_old_app.xml"])


#!/usr/bin/env python
# encoding: utf-8
"""
test_oma.py

Created by Dag Brattli on 2008-03-02.
Copyright (c) 2008 Dag Brattli. All rights reserved.
"""

import sys
import os

from elements.formats import oma

def test_oma(filename="tests/oma.xml"):
    data = open(filename).read()
    d = oma.WapProvisioningDoc.from_string(data)
    
#    print d.to_string()
    print d.characteristic.parm.name
    print d.characteristic[1].characteristic.parm.name
    print d.to_string()

if __name__ == '__main__':
	test_oma("oma.xml")


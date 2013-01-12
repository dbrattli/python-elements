#!/usr/bin/python
#
# Copyright (C) 2008 Dag Brattli.
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


from distutils.cmd import Command
from distutils.command.build_ext import build_ext
try:
    from setuptools import setup, Extension, Feature
except ImportError:
    from distutils.core import setup, Extension
    Feature = None
import sys

setup(
    name='Elements',
    version='2.0.0',
    description='Python Elements XML Library',
    long_description = """\
The Python XML Elements library makes it easy to parse XML.
""",
    author='Dag Brattli',
    author_email='dbrattli@gmail.com',
    license='New BSD License',
    url='http://code.google.com/p/python-elements/',
    download_url = 'http://code.google.com/p/python-elements/downloads/list',
    zip_safe = True,

    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
	    'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: XML'
    ],
    test_suite='nose.collector',

    packages=['elements', 'elements.formats', 'tests'],
    package_dir = { 'elements':'elements', 'tests' : 'tests'}
)

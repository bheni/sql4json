#!/usr/bin/env python

from distutils.core import setup

setup(name='sql4json',
      version='0.3.0',
      description='Python SQL library and command line for querying JSON documents',
      author='Brian Hendriks',
      url='http://github.com/bheni/sql4json',
      packages=['sql4json', 'sql4json.boolean_expressions'],
      scripts=['bin/sql4json', 'bin/mpack2json']
)

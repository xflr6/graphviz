#!/usr/bin/env python
# try-examples.py - import graphviz here and run all scripts in the example dir

import glob
import io
import os

import graphviz  # noqa: F401

os.chdir('examples')
for filename in glob.iglob('*.py'):
    with io.open(filename, encoding='utf-8') as fd:
        code = fd.read()
    exec(code)

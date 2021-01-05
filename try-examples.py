#!/usr/bin/env python
# try-examples.py - import graphviz here and run all scripts in the example dir

import glob
import os
import warnings

import graphviz  # noqa: F401

os.chdir('examples')

for filename in glob.iglob('*.py'):
    with open(filename, encoding='utf-8') as fd:
        code = fd.read()
    try:
        exec(code)
    except Exception as e:
        warnings.warn(e)

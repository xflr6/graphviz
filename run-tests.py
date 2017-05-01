#!/usr/bin/env python
# run-tests.py

import sys
import platform

import pytest

ARGS = [
    #'--exitfirst',
    #'--pdb',
]

if 'idlelib' in sys.modules:
    ARGS.append('--color=no')

if platform.system().lower() == 'windows':
    ARGS.append('--capture=sys')

pytest.main(ARGS + sys.argv[1:])

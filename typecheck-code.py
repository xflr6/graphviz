#!/usr/bin/env python3

"""Run type checking with https://mypy-lang.org."""

import pathlib
import sys

import mypy.main

SELF = pathlib.Path(__file__)


print('run', [SELF.name] + sys.argv[1:])
args = sys.argv[1:]

print(f'mypy.main.main({args=}, clean_exit=True)')
try:
    mypy.main.main(args=args, clean_exit=True)
except SystemExit as e:
    print('FAILED:', e.code)
    status = e.code
else:
    print('PASSED.')
    status = None
sys.exit(status)

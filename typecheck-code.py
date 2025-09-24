#!/usr/bin/env python3

"""Run type checking with https://mypy-lang.org."""

import pathlib
import sys

import mypy.main

SELF = pathlib.Path(__file__)

ARGS = []


print('run', [SELF.name] + sys.argv[1:])
args = ARGS + sys.argv[1:]

print(f'mypy.main.main({args=}, clean_exit=True)')
try:
    mypy.main.main(args=args, clean_exit=True)
except SystemExit as e:
    exit = e
else:
    exit = SystemExit(0)

print('FAILED:' if exit.code else 'PASSED:', repr(exit))
sys.exit(exit.code)

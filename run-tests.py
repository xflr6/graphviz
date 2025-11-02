#!/usr/bin/env python3
# flake8: noqa

"""Run the tests with https://pytest.org."""

import pathlib
import platform
import sys

import pytest

SELF = pathlib.Path(__file__)

ARGS = [#'--skip-exe',
        #'--only-exe',
        #'--collect-only',
        #'--verbose',
        #'--pdb',
        #'--exitfirst',  # a.k.a. -x
        #'-W', 'error',
        #'--doctest-report none',
       ]

if platform.system() == 'Windows' and 'idlelib' in sys.modules:
    ARGS += ['-p', 'no:faulthandler']


print('run', [SELF.name] + sys.argv[1:])
args = ARGS + sys.argv[1:]

# https://docs.pytest.org/en/stable/reference/reference.html#pytest-main
print(f'pytest.main({args!r})')
if (returncode := pytest.main(args)):
    print('FAILED:', returncode)
else:
    print('PASSED.')
sys.exit(returncode)

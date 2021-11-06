#!/usr/bin/env python3
# flake8: noqa

import platform
import sys

import pytest

ARGS = [#'--skip-exe',
        #'--collect-only',
        #'--verbose',
        #'--pdb',
        #'--exitfirst',  # a.k.a. -x
        #'-W', 'error',
        #'--doctest-report none',
        #'--doctest-continue-on-failure',
        ]

if platform.system() == 'Windows':
    if 'idlelib' in sys.modules:
        ARGS += ['--capture=sys', '--color=no']

args = sys.argv[1:] + ARGS

print(f'pytest.main({args!r})')
sys.exit(pytest.main(args))

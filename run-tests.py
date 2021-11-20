#!/usr/bin/env python3
# flake8: noqa

"""Run the tests with https://pytest.org."""

import platform
import sys

import pytest

ARGS = [#'--skip-exe',
        #'--only-exe',
        #'--collect-only',
        #'--verbose',
        #'--pdb',
        #'--exitfirst',  # a.k.a. -x
        #'-W', 'error',
        #'--doctest-report none',
        #'--doctest-continue-on-failure',
        #'--cov-append',
        ]

if platform.system() == 'Windows' and 'idlelib' in sys.modules:
    ARGS += ['--capture=sys', '--color=no']


args = ARGS + sys.argv[1:]

print(f'pytest.main({args!r})')
sys.exit(pytest.main(args))

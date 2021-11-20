#!/usr/bin/env python3
# flake8: noqa

"""Run the tests with https://pytest.org."""

import doctest as doctest
from unittest import mock

import platform
import sys

NO_EXE = doctest.register_optionflag('NO_EXE')

ARGS = [#'--skip-exe',
        #'--only-exe',
        #'--collect-only',
        #'--verbose',
        #'--pdb',
        #'--exitfirst',  # a.k.a. -x
        #'-W', 'error',
        #'--doctest-report none',
        #'--cov-append',
        ]


class NoExeChecker(doctest.OutputChecker):

    def check_output(self, want, got, optionflags, *args, **kwargs) -> bool:
        if optionflags & NO_EXE:
            return True
        return super().check_output(want, got, optionflags, *args, **kwargs)


mock.patch.object(doctest, 'OutputChecker', new=NoExeChecker).start()
import pytest  # noqa: E402


if platform.system() == 'Windows' and 'idlelib' in sys.modules:
    ARGS += ['--capture=sys', '--color=no']


args = ARGS + sys.argv[1:]

print(f'pytest.main({args!r})')
sys.exit(pytest.main(args))

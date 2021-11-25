#!/usr/bin/env python3

"""Run code linting with https://flake8.pycqa.org."""

import platform
import subprocess
import sys

PYTHON = 'py' if platform.system() == 'Windows' else 'python'

CMD = [PYTHON, '-m', 'flake8']


cmd = CMD + sys.argv[1:]

print(f'subprocess.run({cmd!r})')
proc = subprocess.run(cmd)

print('', proc, sep='\n')
sys.exit(proc.returncode)

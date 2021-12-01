#!/usr/bin/env python3

"""Run code linting with https://flake8.pycqa.org."""

import pathlib
import platform
import subprocess
import sys

SELF = pathlib.Path(__file__)

PYTHON = 'py' if platform.system() == 'Windows' else 'python'

CMD = [PYTHON, '-m', 'flake8']


print('run', [SELF.name] + sys.argv[1:])
cmd = CMD + sys.argv[1:]

print(f'subprocess.run({cmd!r})')
try:
    proc = subprocess.run(cmd, check=True)
except subprocess.CalledProcessError as e:
    assert e.returncode != 0, f'non-zero returncode: {e}'
    print('FAILED:', e)
    sys.exit(e.returncode)
else:
    assert proc.returncode == 0, f'passed: {proc}'
    print('PASSED:', proc)
    sys.exit(proc.returncode)

#!/usr/bin/env python3
# flake8: noqa

"""Build the docs with https://www.sphinx-doc.org."""

import contextlib
import os
import pathlib
import sys
import webbrowser

from sphinx.cmd import build

SOURCE = pathlib.Path('docs')

TARGET = pathlib.Path('_build')

RESULT = SOURCE / TARGET / 'index.html'

DEFAULT_ARGS = ['-n', '-v', '.', str(TARGET)]

OPEN_RESULT = True

SKIP_OPEN_RESULT = '--no-open'


@contextlib.contextmanager
def chdir(path):
    cwd_before = os.getcwd()
    print(f'os.chdir({path})')
    os.chdir(path)
    try:
        yield path
    finally:
        print(f'os.chdir({cwd_before}')
        os.chdir(cwd_before)


args = sys.argv[1:]
if SKIP_OPEN_RESULT in args:
    OPEN_RESULT = False
    args = [a for a in args if a != SKIP_OPEN_RESULT]
if not args:
    args = DEFAULT_ARGS

with chdir(SOURCE):
    print(f'sphinx.cmd.build.main({args})')
    result = build.main(args)

print('', RESULT, sep='\n')

try:
    assert RESULT.stat().st_size, f'non-empty {RESULT}'
    if OPEN_RESULT:
        webbrowser.open(RESULT)
finally:
    sys.exit(result)

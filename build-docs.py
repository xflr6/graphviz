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
if not args:
    args = DEFAULT_ARGS

with chdir(SOURCE):
    print(f'sphinx.cmd.build.main({args})')
    result = build.main(args)

print('', RESULT, sep='\n')

try:
    assert RESULT.stat().st_size, f'non-empty {RESULT}'
    webbrowser.open(RESULT)
finally:
    sys.exit(result)

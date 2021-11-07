#!/usr/bin/env python3
# flake8: noqa

"""Build the docs with https://www.sphinx-doc.org."""

import contextlib
import os
import pathlib
import sys

from sphinx.cmd import build

SOURCE = pathlib.Path('docs')

TARGET = pathlib.Path('_build')

RESULT = SOURCE / TARGET / 'index.html'

ARGS = ['.', str(TARGET)]


@contextlib.contextmanager
def chdir(path):
    cwd_before = os.getcwd()
    os.chdir(path)
    try:
        yield path
    finally:
        os.chdir(cwd_before)


args = sys.argv[1:]
if not args:
    args += ARGS

print(f'os.chdir({SOURCE})')
with chdir(SOURCE):
    print(f'sphinx.cmd.build.main({args})')
    result = build.main(args)

print('', RESULT, sep='\n')

try:
    assert RESULT.stat().st_size, f'should be non-empty: {RESULT}'
finally:
    sys.exit(result)

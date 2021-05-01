#!/usr/bin/env python3

"""Import ``graphviz`` here and run all scripts in the ``examples/`` dir."""

import os
import pathlib
import warnings

import graphviz  # noqa: F401

EXAMPLES = pathlib.Path('examples')

os.chdir(EXAMPLES)

for path in pathlib.Path().glob('*.py'):
    code = path.read_text(encoding='utf-8')
    try:
        exec(code)
    except Exception as e:
        warnings.warn(e)

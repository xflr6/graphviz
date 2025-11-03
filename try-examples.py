#!/usr/bin/env python3

"""Import ``graphviz`` here and run all scripts in the ``examples/`` dir."""

import os
import pathlib
import sys
import unittest.mock
import warnings

import graphviz

SELF = pathlib.Path(__file__)

EXAMPLES = pathlib.Path('examples')

IO_KWARGS = {'encoding': 'utf-8'}

DEFAULT_FORMAT = 'pdf'


print('run', [SELF.name] + sys.argv[1:])
os.chdir(EXAMPLES)

graphviz.set_default_format(DEFAULT_FORMAT)

raised = []

with unittest.mock.patch.object(graphviz.graphs.BaseGraph, '_view') as mock_view:
    for path in pathlib.Path().glob('*.py'):
        print(path)
        code = path.read_text(**IO_KWARGS)

        try:
            exec(code)
        except Exception as e:
            raised.append(e)
            warnings.warn(e)
        else:
            if path.name.endswith('_recipe.py'):
                continue
            rendered = f'{path.stem}.gv.{DEFAULT_FORMAT}'
            assert pathlib.Path(rendered).stat().st_size, f'non-empty {rendered}'
            mock_view.assert_called_once_with(rendered,
                                              format=DEFAULT_FORMAT,
                                              quiet=False)
            mock_view.reset_mock()

if raised:
    print(*raised, sep='\n')
    sys.exit(f'FAILED: {len(raised)} example(s) raised an error (WARNING)')
print('PASSED: all examples passed without raising')

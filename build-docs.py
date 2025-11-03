#!/usr/bin/env python3

"""Build the docs with https://www.sphinx-doc.org."""

import pathlib
import sys
import webbrowser

import sphinx.cmd.build

SELF = pathlib.Path(__file__)

SOURCE = pathlib.Path('docs')

TARGET = SOURCE / '_build'

RESULT = TARGET / 'index.html'

BROWSER_OPEN = '--open'

SKIP_OPEN_RESULT = '--no-open'

DEFAULT_ARGS = [BROWSER_OPEN, '-W', '-n', '-v', str(SOURCE), str(TARGET)]

OPEN_RESULT = BROWSER_OPEN in DEFAULT_ARGS


print('run', [SELF.name] + sys.argv[1:])
args = sys.argv[1:]
if not args:
    args = DEFAULT_ARGS

if SKIP_OPEN_RESULT in args:
    open_result = None
    args = [a for a in args
            for name, value in [a.partition('=')[::2]]
            if name not in (SKIP_OPEN_RESULT, BROWSER_OPEN)]
elif any(a.partition('=')[0] == BROWSER_OPEN for a in args):
    open_result = RESULT

    values = {value for a in args
              for name, value in [a.partition('=')[::2]]
              if name == BROWSER_OPEN and value}
    if values:
        if len(values) != 1:
            raise ValueError(f'conflicting {BROWSER_OPEN}: {values}')
        (value,) = values
        if value:
            open_result = open_result.parent / value
    args = [a for a in args if a.partition('=')[0] != BROWSER_OPEN]
else:
    open_result = RESULT if 'doctest' not in args else None

if not args:  # no pytest args given
    args = [a for a in DEFAULT_ARGS
            if a != SKIP_OPEN_RESULT and a.partition('=')[0] != BROWSER_OPEN]

if args == ['-b', 'doctest']:
    args += ['-W', str(SOURCE), str(SOURCE / '_doctest')]

print(f'sphinx.cmd.build.main({args})')
if (returncode := sphinx.cmd.build.main(args)):
    print('', f'FAILED: returncode {returncode!r}', sep='\n')
    sys.exit(returncode)

if 'doctest' not in args:
    print('', f'index: {RESULT}', sep='\n')
    print(f'assert {RESULT!r}.stat().st_size')
    assert RESULT.stat().st_size, f'non-empty {RESULT}'
print('', 'PASSED.', sep='\n')

if open_result:
    print(f'webbrowser.open({open_result!r})')
    webbrowser.open(open_result)

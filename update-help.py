#!/usr/bin/env python3

"""Update the ``help()`` outputs  in ``docs/api.rst``."""

import contextlib
import difflib
import io
import operator
import pathlib
import re
import sys
import typing

import graphviz

ALL_CLASSES = [graphviz.Graph, graphviz.Digraph, graphviz.Source]

ARGS_LINE = re.compile(r'(?:class | \| {2})\w+\(')

WRAP_AFTER = 80

WRAP_SEARCH, WRAP_REPL = re.compile(r'(,)[ ](?!\*)'), r'\1\n{indent} '

INDENT = ' ' * 4

TARGET = pathlib.Path('docs/api.rst')

PATTERN = (r'''
           (
           \ {{4}}>>>\ help\(graphviz\.{cls_name}\).*\n)
           \ {{4}}Help\ on\ class\ {cls_name}
                  \ in\ module\ graphviz\.(?:graphs|sources):\n
           \ {{4}}<BLANKLINE>\n
           (?:.*\n)+?
           \ {{4}}<BLANKLINE>\n
           ''')

IO_KWARGS = {'encoding': 'utf-8'}


def get_help(obj) -> str:
    print(f'capture help() output for {obj}')
    with contextlib.redirect_stdout(io.StringIO()) as buf:
        help(obj)
    buf.seek(0)
    return ''.join(iterlines(buf))


def rpartition_initial(value: str, *, sep: str) -> typing.Tuple[str, str, str]:
    """Return (value, '', '') if sep not in value else value.rpartition(sep)."""
    _, sep_found, _ = parts = value.rpartition(sep)
    return reversed(parts) if not sep_found else parts


def iterlines(stdout_lines, *,
              line_indent: str = INDENT,
              wrap_after: int = WRAP_AFTER) -> typing.Iterator[str]:
    """Yield post-processed help() stdout lines: rstrip, indent, wrap."""
    for line in stdout_lines:
        line = line.rstrip() + '\n'
        line = line.replace("``'\\n'``", r"``'\\n'``")

        if len(line) > wrap_after and ARGS_LINE.match(line):
            line, *rest = rpartition_initial(line, sep=' -> ')

            indent = line_indent + ' ' * line.index('(')
            repl = WRAP_REPL.format(indent=indent)

            line, n_newlines = WRAP_SEARCH.subn(repl, line)
            print(len(line), 'character line wrapped into',
                  n_newlines + 1, 'lines')
            assert n_newlines, 'wrapped long argument line'

            line += ''.join(rest)

        yield line_indent + line


help_docs = {cls.__name__: get_help(cls) for cls in ALL_CLASSES}

print('read', TARGET)
target = target_before = TARGET.read_text(**IO_KWARGS)

for cls_name, doc in help_docs.items():
    print('replace', cls_name, 'PATTERN match')

    pattern = re.compile(PATTERN.format(cls_name=cls_name), flags=re.VERBOSE)

    target, found = pattern.subn(fr'\1{doc}', target, count=1)
    assert found, f'replaced {cls_name} section'

    target = target.replace(INDENT + '\n', INDENT + '<BLANKLINE>\n')

if target == target_before:
    print('unchanged (OK)')
    sys.exit(None)
else:
    print('write', TARGET)
    splitlines = operator.methodcaller('splitlines', keepends=True)
    target_before, target = map(splitlines, (target_before, target))
    print(len(target_before), 'lines before')
    print(len(target), 'lines after')

    with TARGET.open('w', **IO_KWARGS) as f:
        for line in target:
            f.write(line)

    for diff in difflib.context_diff(target_before, target):
        print(diff)

    message = f'changed {TARGET!r} (WARNING)'
    print(f'sys.exit({message!r})')
    sys.exit(message)

# graphviz - create dot, save, render, view

"""Assemble DOT source code and render it with Graphviz.

>>> import graphviz
>>> dot = graphviz.Digraph(comment='The Round Table')

>>> dot.node('A', 'King Arthur')
>>> dot.node('B', 'Sir Bedevere the Wise')
>>> dot.node('L', 'Sir Lancelot the Brave')

>>> dot.edges(['AB', 'AL'])

>>> dot.edge('B', 'L', constraint='false')

>>> print(dot)  #doctest: +NORMALIZE_WHITESPACE
// The Round Table
digraph {
    A [label="King Arthur"]
    B [label="Sir Bedevere the Wise"]
    L [label="Sir Lancelot the Brave"]
    A -> B
    A -> L
    B -> L [constraint=false]
}
"""

from .backend import (DOT_BINARY, UNFLATTEN_BINARY,
                      render, pipe, pipe_string, pipe_lines, pipe_lines_string,
                      unflatten, version, view,
                      RequiredArgumentError, ExecutableNotFound)
from .graphs import Graph, Digraph
from .parameters import ENGINES, FORMATS, RENDERERS, FORMATTERS
from .quoting import escape, nohtml
from .sources import Source

__all__ = ['ENGINES', 'FORMATS', 'RENDERERS', 'FORMATTERS',
           'DOT_BINARY', 'UNFLATTEN_BINARY',
           'Graph', 'Digraph',
           'Source',
           'escape', 'nohtml',
           'render', 'pipe', 'pipe_string', 'pipe_lines', 'pipe_lines_string',
           'unflatten', 'version', 'view',
           'RequiredArgumentError', 'ExecutableNotFound',
           'set_default_engine', 'set_default_format']

__title__ = 'graphviz'
__version__ = '0.18.2'
__author__ = 'Sebastian Bank <sebastian.bank@uni-leipzig.de>'
__license__ = 'MIT, see LICENSE.txt'
__copyright__ = 'Copyright (c) 2013-2021 Sebastian Bank'

#: :class:`set` of known layout commands used for rendering
#: (``'dot'``, ``'neato'``, ...)
ENGINES = ENGINES

#: :class:`set` of known output formats for rendering
#: (``'pdf'``, ``'png'``, ...)
FORMATS = FORMATS

#: :class:`set` of known output renderers for rendering
#: (``'cairo'``, ``'gd'``, ...)
RENDERERS = RENDERERS

#: :class:`set` of known output formatters for rendering
#: (``'cairo'``, ``'gd'``, ...)
FORMATTERS = FORMATTERS

#: :class:`pathlib.Path` of rendering command
#: (``Path('dot')``)
DOT_BINARY = DOT_BINARY

#: :class:`pathlib.Path` of unflatten command
#: (``Path('unflatten')``)
UNFLATTEN_BINARY = UNFLATTEN_BINARY


ExecutableNotFound = ExecutableNotFound


RequiredArgumentError = RequiredArgumentError


def set_default_engine(engine: str) -> str:
    """Change the default engine, return the old default value."""
    from . import parameters

    parameters.verify_engine(engine)

    old_default_engine = parameters.Parameters._engine
    parameters.Parameters._engine = engine
    return old_default_engine


def set_default_format(format: str) -> str:
    """Change the default format, return the old default value."""
    from . import parameters

    parameters.verify_format(format)

    old_default_format = parameters.Parameters._format
    parameters.Parameters._format = format
    return old_default_format

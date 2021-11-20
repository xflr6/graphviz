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
from .jupyter_integration import SUPPORTED_JUPYTER_FORMATS
from .parameters import ENGINES, FORMATS, RENDERERS, FORMATTERS
from .quoting import escape, nohtml
from .sources import Source

__all__ = ['ENGINES', 'FORMATS', 'RENDERERS', 'FORMATTERS',
           'DOT_BINARY', 'UNFLATTEN_BINARY',
           'SUPPORTED_JUPYTER_FORMATS',
           'Graph', 'Digraph',
           'Source',
           'escape', 'nohtml',
           'render', 'pipe', 'pipe_string', 'pipe_lines', 'pipe_lines_string',
           'unflatten', 'version', 'view',
           'RequiredArgumentError', 'ExecutableNotFound',
           'set_default_engine', 'set_default_format', 'set_jupyter_format']

__title__ = 'graphviz'
__version__ = '0.19.dev0'
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

#: :class:`set` of supported formats for ``Ipython.display``
#: (``'svg'``, ``'png'``, ...)
SUPPORTED_JUPYTER_FORMATS = SUPPORTED_JUPYTER_FORMATS

#: :class:`pathlib.Path` of rendering command
#: (``Path('dot')``)
DOT_BINARY = DOT_BINARY

#: :class:`pathlib.Path` of unflatten command
#: (``Path('unflatten')``)
UNFLATTEN_BINARY = UNFLATTEN_BINARY


ExecutableNotFound = ExecutableNotFound


RequiredArgumentError = RequiredArgumentError


def set_default_engine(engine: str) -> str:
    """Change the default engine, return the old default value.

    Args:
        engine: new default engine for all present and newly created instances.

    Returns:
        The old default engine.
    """
    from . import parameters

    parameters.verify_engine(engine)

    old_default_engine = parameters.Parameters._engine
    parameters.Parameters._engine = engine
    return old_default_engine


def set_default_format(format: str) -> str:
    """Change the default format, return the old default value.

    Args:
        format: new default format for all present and newly created instances.

    Returns:
        The old default format.
    """
    from . import parameters

    parameters.verify_format(format)

    old_default_format = parameters.Parameters._format
    parameters.Parameters._format = format
    return old_default_format


def set_jupyter_format(jupyter_format: str) -> str:
    """Change the default mimetype format for ``_repr_mimebundle_(include, exclude)``
        and return the old value.

    Args:
        jupyter_format: new display format for all present and newly created instances.

    Returns:
        The old default display format.
    """
    from . import jupyter_integration

    mimetype = jupyter_integration.get_jupyter_format_mimetype(jupyter_format)

    old_mimetype = jupyter_integration.JupyterIntegration._jupyter_mimetype
    old_format = jupyter_integration.get_jupyter_mimetype_format(old_mimetype)

    jupyter_integration.JupyterIntegration._jupyter_mimetype = mimetype
    return old_format

"""Execute rendering subprocesses and open files in viewer."""

from ._version import version
from .common import RequiredArgumentError
from .engines import ENGINES
from .execute import run_check, ExecutableNotFound
from .formats import FORMATS
from .formatters import FORMATTERS
from .graphviz import Graphviz
from .renderers import RENDERERS
from .rendering import (DOT_BINARY,
                        render,
                        pipe, pipe_string, pipe_lines, pipe_lines_string)
from .unflattening import UNFLATTEN_BINARY, unflatten
from .viewing import view, View

__all__ = ['DOT_BINARY', 'UNFLATTEN_BINARY',
           'ENGINES', 'FORMATS', 'RENDERERS', 'FORMATTERS',
           'RequiredArgumentError',
           'render', 'pipe', 'pipe_string', 'pipe_lines', 'pipe_lines_string',
           'unflatten',
           'Graphviz',
           'version', 'view',
           'View',
           'ExecutableNotFound']

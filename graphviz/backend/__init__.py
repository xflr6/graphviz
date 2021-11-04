"""Execute rendering subprocesses and open files in viewer."""

from ._common import RequiredArgumentError

from .engines import ENGINES
from .formats import FORMATS
from .formatters import FORMATTERS
from .renderers import RENDERERS

from .bases import Graphviz, View
from .execute import run_check, ExecutableNotFound
from .graphviz_version import version
from .rendering import (DOT_BINARY, render, pipe, pipe_string,
                        pipe_lines, pipe_lines_string)
from .unflattening import UNFLATTEN_BINARY, unflatten
from .viewing import view

__all__ = ['DOT_BINARY', 'UNFLATTEN_BINARY',
           'ENGINES', 'FORMATS', 'RENDERERS', 'FORMATTERS',
           'version',
           'render',
           'pipe', 'pipe_string',
           'pipe_lines', 'pipe_lines_string',
           'unflatten',
           'view',
           'RequiredArgumentError', 'ExecutableNotFound',
           'Graphviz', 'View']

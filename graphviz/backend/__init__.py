"""Execute rendering subprocesses and open files in viewer."""

from ._common import RequiredArgumentError

from .engines import ENGINES
from .formats import FORMATS
from .formatters import FORMATTERS
from .renderers import RENDERERS

from .execute import run_check, ExecutableNotFound
from .graphviz_version import version
from .rendering import (DOT_BINARY, render, pipe, pipe_string,
                        pipe_lines, pipe_lines_string)
from .unflattening import UNFLATTEN_BINARY, unflatten
from .viewing import view

from .mixins import Render, Pipe, Unflatten, View

__all__ = ['DOT_BINARY', 'UNFLATTEN_BINARY',
           'ENGINES', 'FORMATS', 'RENDERERS', 'FORMATTERS',
           'render',
           'pipe', 'pipe_string',
           'pipe_lines', 'pipe_lines_string',
           'unflatten',
           'version',
           'view',
           'RequiredArgumentError', 'ExecutableNotFound',
           'Render', 'Pipe', 'Unflatten', 'View']

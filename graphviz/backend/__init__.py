"""Execute rendering subprocesses and open files in viewer."""

from ._common import RequiredArgumentError

from .engines import ENGINES
from .formats import FORMATS
from .formatters import FORMATTERS
from .renderers import RENDERERS

from .dot_command import DOT_BINARY
from .execute import run_check, ExecutableNotFound
from .piping import pipe, pipe_string, pipe_lines, pipe_lines_string
from .rendering import render
from .unflattening import UNFLATTEN_BINARY, unflatten
from .upstream_version import version
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

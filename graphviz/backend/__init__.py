"""Execute rendering and unflattening subprocesses, open files in viewer."""

from ._common import RequiredArgumentError
from .dot_command import DOT_BINARY
from .execute import ExecutableNotFound
from .mixins import Render, Pipe, Unflatten, View
from .piping import pipe, pipe_string, pipe_lines, pipe_lines_string
from .rendering import render
from .unflattening import UNFLATTEN_BINARY, unflatten
from .upstream_version import version
from .viewing import view

__all__ = ['DOT_BINARY', 'UNFLATTEN_BINARY',
           'render',
           'pipe', 'pipe_string',
           'pipe_lines', 'pipe_lines_string',
           'unflatten',
           'version',
           'view',
           'RequiredArgumentError', 'ExecutableNotFound',
           'Render', 'Pipe', 'Unflatten', 'View']

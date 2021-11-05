"""Mixin classes used by Base subclasses to inherit backend functionality."""

import typing

# Hold and verify parameters.
from . import engines
from . import formats
from . import formatters
from . import renderers

#  Call backend functions.
from . import piping
from . import rendering
from . import unflattening
from . import viewing

__all__ = ['Render', 'Pipe', 'Unflatten', 'View']


class Graphviz(engines.Engine, formats.Format,
               renderers.Renderer, formatters.Formatter):
    """Parameters for calling ``backend.render()`` and ``backend.pipe``."""

    def __init__(self, format=None, engine=None, **kwargs):
        super().__init__(format=format, engine=engine, **kwargs)

    def _get_rendering_parameters(self, *,
                                  engine: typing.Optional[str] = None,
                                  format: typing.Optional[str] = None,
                                  renderer: typing.Optional[str] = None,
                                  formatter: typing.Optional[str] = None,
                                  **kwargs):
        if engine is None:
            engine = self._engine

        if format is None:
            format = self._format

        args = [engine, format]

        if renderer is None:
            renderer = self._renderer

        if formatter is None:
            formatter = self._formatter

        kwargs.update(renderer=renderer, formatter=formatter)

        return args, kwargs


class Render(Graphviz):

    _get_render_parameters = Graphviz._get_rendering_parameters

    @property
    def _render(_):
        """Simplify rendering.render mocking."""
        return rendering.render


class Pipe(Graphviz):

    _get_pipe_parameters = Graphviz._get_rendering_parameters

    @property
    def _pipe_lines(_):
        """Simplify rendering.pipe_lines mocking."""
        return piping.pipe_lines

    _pipe_lines_string = staticmethod(piping.pipe_lines_string)


class Unflatten:

    _unflatten = staticmethod(unflattening.unflatten)


class View:
    """Open filepath with its default viewing application
        (platform-specific)."""

    _view_darwin = staticmethod(viewing.view_darwin)

    _view_freebsd = staticmethod(viewing.view_freebsd)

    _view_linux = staticmethod(viewing.view_linux)

    _view_windows = staticmethod(viewing.view_windows)

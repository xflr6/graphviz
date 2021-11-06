"""Mixin classes used by Base subclasses to inherit backend functionality."""

import typing

from . import parameters
from . import piping
from . import rendering
from . import unflattening
from . import viewing

__all__ = ['Render', 'Pipe', 'Unflatten', 'View']


class Parameters(parameters.Engine, parameters.Format,
                 parameters.Renderer, parameters.Formatter):
    """Parameters for calling ``graphviz.render()`` and ``graphviz.pipe()``."""

    def __init__(self, format=None, engine=None, **kwargs):
        super().__init__(format=format, engine=engine, **kwargs)

    def _get_parameters(self, *,
                        engine: typing.Optional[str] = None,
                        format: typing.Optional[str] = None,
                        renderer: typing.Optional[str] = None,
                        formatter: typing.Optional[str] = None,
                        verify: bool = False,
                        **kwargs):
        if engine is None:
            engine = self._engine
        elif verify:
            self._verify_engine(engine)

        if format is None:
            format = self._format
        elif verify:
            self._verify_format(format)

        args = [engine, format]

        if renderer is None:
            renderer = self._renderer
        elif verify:
            self._verify_renderer(renderer)

        if formatter is None:
            formatter = self._formatter
        elif verify:
            self._verify_formatter(formatter)

        kwargs.update(renderer=renderer, formatter=formatter)

        return args, kwargs


class Render(Parameters):

    _get_render_parameters = Parameters._get_parameters

    @property
    def _render(_):
        """Simplify ``._render()`` mocking."""
        return rendering.render


class Pipe(Parameters):

    _get_pipe_parameters = Parameters._get_parameters

    @property
    def _pipe_lines(_):
        """Simplify ``._pipe_lines()`` mocking."""
        return piping.pipe_lines

    @property
    def _pipe_lines_string(_):
        """Simplify ``._pipe_lines_string()`` mocking."""
        return piping.pipe_lines_string


class Unflatten:

    @property
    def _unflatten(_):
        """Simplify ``._unflatten mocking."""
        return unflattening.unflatten


class View:
    """Open filepath with its default viewing application
        (platform-specific)."""

    _view_darwin = staticmethod(viewing.view_darwin)

    _view_freebsd = staticmethod(viewing.view_unixoid)

    _view_linux = staticmethod(viewing.view_unixoid)

    _view_windows = staticmethod(viewing.view_windows)

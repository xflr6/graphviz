import typing

from . import engines
from . import formats
from . import formatters
from . import renderers
from . import rendering
from . import unflattening
from . import viewing

__all__ = ['Graphviz', 'View']


class BaseGraphviz(engines.Engine, formats.Format,
                   renderers.Renderer, formatters.Formatter):

    def _get_rendering_kwargs(self, *,
                              format: typing.Optional[str] = None,
                              renderer: typing.Optional[str] = None,
                              formatter: typing.Optional[str] = None,
                              **kwargs):
        if format is None:
            format = self._format

        if renderer is None:
            renderer = self._renderer

        if formatter is None:
            formatter = self._formatter

        kwargs.update(format=format, renderer=renderer, formatter=formatter)
        return kwargs


class Render(BaseGraphviz):

    @staticmethod
    def _render(*args, **kwargs):
        """Simplify rendering.render mocking."""
        return rendering.render(*args, **kwargs)

    _get_render_kwargs = BaseGraphviz._get_rendering_kwargs


class Pipe(BaseGraphviz):

    @staticmethod
    def _pipe_lines(*args, **kwargs):
        """Simplify rendering.pipe_lines mocking."""
        return rendering.pipe_lines(*args, **kwargs)

    _pipe_lines_string = staticmethod(rendering.pipe_lines_string)

    _get_pipe_kwargs = BaseGraphviz._get_rendering_kwargs


class Unflatten:

    _unflatten = staticmethod(unflattening.unflatten)


class Graphviz(Render, Pipe, Unflatten):
    """Graphiz defaults."""

    def __init__(self, format=None, engine=None, **kwargs):
        super().__init__(format=format, engine=engine, **kwargs)


class View:
    """Open filepath with its default viewing application
        (platform-specific)."""

    _view_darwin = staticmethod(viewing.view_darwin)

    _view_freebsd = staticmethod(viewing.view_unixoid)

    _view_linux = staticmethod(viewing.view_unixoid)

    _view_windows = staticmethod(viewing.view_windows)

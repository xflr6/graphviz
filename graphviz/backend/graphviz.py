import typing

from . import engines
from . import formats
from . import renderers
from . import formatters
from .import rendering
from .import unflattening


class Graphviz(engines.Engine, formats.Format,
               renderers.Renderer, formatters.Formatter,
               unflattening.Unflatten):
    """Graphiz defaults."""

    @staticmethod
    def _pipe_lines(*args, **kwargs):
        """Simplify mocking ``pipe_lines``."""
        return rendering.pipe_lines(*args, **kwargs)

    @staticmethod
    def _pipe_lines_string(*args, **kwargs):
        return rendering.pipe_lines_string(*args, **kwargs)

    @staticmethod
    def _render(*args, **kwargs):
        """Simplify mocking ``render``."""
        return rendering.render(*args, **kwargs)

    def __init__(self, format=None, engine=None, **kwargs):
        super().__init__(format=format, engine=engine, **kwargs)

    def _get_backend_kwargs(self, *,
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

    _get_pipe_kwargs = _get_render_kwargs = _get_backend_kwargs

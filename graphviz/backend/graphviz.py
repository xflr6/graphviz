import typing

from .. import copying

from . import engines
from . import formats
from . import renderers
from . import formatters
from .import rendering
from .import unflattening


class Graphviz(copying.Copy,
               engines.Engine, formats.Format,
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

    def _copy_kwargs(self, **kwargs):
        """Return the kwargs to create a copy of the instance."""
        attr_kw = [('_engine', 'engine'), ('_format', 'format'),
                   ('_formatter', 'formatter')]
        ns = self.__dict__
        for attr, kw in attr_kw:
            assert kw not in kwargs
            if attr in ns:
                kwargs[kw] = ns[attr]
        return super()._copy_kwargs(**kwargs)

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

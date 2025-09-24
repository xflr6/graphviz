"""Mixin classes used to inherit parameter functionality."""

from typing import Optional

from . import engines
from . import formats
from . import renderers
from . import formatters

__all__ = ['Parameters']


class Parameters(engines.Engine, formats.Format,
                 renderers.Renderer, formatters.Formatter):
    """Parameters for calling ``graphviz.render()`` and ``graphviz.pipe()``."""

    def _get_parameters(self, *,
                        engine: Optional[str] = None,
                        format: Optional[str] = None,
                        renderer: Optional[str] = None,
                        formatter: Optional[str] = None,
                        verify: bool = False,
                        **kwargs):
        if engine is None:
            engine = self.engine
        elif verify:
            self._verify_engine(engine)

        if format is None:
            format = self.format
        elif verify:
            self._verify_format(format)

        if renderer is None:
            renderer = self.renderer
        elif verify:
            self._verify_renderer(renderer)

        if formatter is None:
            formatter = self.formatter
        elif verify:
            self._verify_formatter(formatter)

        kwargs.update(engine=engine, format=format,
                      renderer=renderer, formatter=formatter)
        return kwargs

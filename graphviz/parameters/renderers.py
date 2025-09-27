"""Rendering renderer parameter handling."""

from collections.abc import Set
from typing import Final

from . import base

__all__ = ['RENDERERS', 'verify_renderer', 'Renderer']

RENDERERS: Final[Set[str]] = {'cairo',  # $ dot -T:
                              'dot',
                              'fig',
                              'gd',
                              'gdiplus',
                              'map',
                              'pic',
                              'pov',
                              'ps',
                              'svg',
                              'tk',
                              'vml',
                              'vrml',
                              'xdot'}


REQUIRED: Final = False


def verify_renderer(renderer: str | None, *,
                    required: bool = REQUIRED) -> None:
    if renderer is None:
        if required:
            raise ValueError('missing renderer')
    elif renderer.lower() not in RENDERERS:
        raise ValueError(f'unknown renderer: {renderer!r}'
                         f' (must be None or one of {sorted(RENDERERS)})')


class Renderer(base.ParameterBase):
    """Rendering renderer parameter (no default)."""

    _renderer = None

    _verify_renderer = staticmethod(verify_renderer)

    def __init__(self, *, renderer: str | None = None, **kwargs) -> None:
        super().__init__(**kwargs)

        self.renderer = renderer

    def _copy_kwargs(self, **kwargs):
        """Return the kwargs to create a copy of the instance."""
        renderer = self._getattr_from_dict('_renderer')
        if renderer is not None:
            kwargs['renderer'] = renderer
        return super()._copy_kwargs(**kwargs)

    @property
    def renderer(self) -> str | None:
        """The output renderer used for rendering
            (``'cairo'``, ``'gd'``, ...)."""
        return self._renderer

    @renderer.setter
    def renderer(self, renderer: str | None) -> None:
        if renderer is None:
            self.__dict__.pop('_renderer', None)
        else:
            renderer = renderer.lower()
            self._verify_renderer(renderer)
            self._renderer = renderer

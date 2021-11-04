import typing

from .. import copying

from .common import RENDERERS

__all__ = ['Renderer']


class Renderer:

    _renderer = None

    def __init__(self, *, renderer: typing.Optional[str] = None, **kwargs):
        super().__init__(**kwargs)

        self.renderer = renderer

    def _copy_kwargs(self, **kwargs):
        """Return the kwargs to create a copy of the instance."""
        attr_kw = [('_renderer', 'renderer')]
        ns = self.__dict__
        for attr, kw in attr_kw:
            assert kw not in kwargs
            if attr in ns:
                kwargs[kw] = ns[attr]
        return super()._copy_kwargs(**kwargs)

    @property
    def renderer(self) -> typing.Optional[str]:
        """The output renderer used for rendering
            (``'cairo'``, ``'gd'``, ...)."""
        return self._renderer

    @renderer.setter
    def renderer(self, renderer: typing.Optional[str]) -> None:
        if renderer is None:
            self.__dict__.pop('_renderer', None)
        else:
           renderer = renderer.lower()
           if renderer not in RENDERERS:
               raise ValueError(f'unknown renderer: {renderer!r}')
           self._renderer = renderer

import typing

from .. import copying

__all__ = ['RENDERERS', 'Renderer']

RENDERERS = {'cairo',  # $ dot -T:
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


class Renderer(copying.Copy):

    _renderer = None

    def __init__(self, *, renderer: typing.Optional[str] = None, **kwargs):
        super().__init__(**kwargs)

        self.renderer = renderer

    def _copy_kwargs(self, **kwargs):
        """Return the kwargs to create a copy of the instance."""
        if '_renderer' in self.__dict__:
            kwargs['renderer'] = self._renderer
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

"""Rendering engine parameter handling."""

from .. import copying

__all__ = ['ENGINES', 'Engine']

ENGINES = {'dot',  # http://www.graphviz.org/pdf/dot.1.pdf
           'neato',
           'twopi',
           'circo',
           'fdp',
           'sfdp',
           'patchwork',
           'osage'}


class Engine(copying.Copy):
    """Rendering engine parameter with default."""

    _engine = 'dot'

    def __init__(self, engine=None, **kwargs):
        super().__init__(**kwargs)

        if engine is not None:
            self.engine = engine

    def _copy_kwargs(self, **kwargs):
        """Return the kwargs to create a copy of the instance."""
        if '_engine' in self.__dict__:
            kwargs['engine'] = self._engine
        return super()._copy_kwargs(**kwargs)

    @property
    def engine(self) -> str:
        """The layout engine used for rendering
            (``'dot'``, ``'neato'``, ...)."""
        return self._engine

    @engine.setter
    def engine(self, engine: str) -> None:
        engine = engine.lower()
        if engine not in ENGINES:
            raise ValueError(f'unknown engine: {engine!r}')
        self._engine = engine

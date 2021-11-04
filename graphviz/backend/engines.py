"""Execute rendering subprocesses and open files in viewer."""

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


class Engine:
    """Graphiz default engine."""

    _engine = 'dot'

    def __init__(self, engine=None, **kwargs):
        super().__init__(**kwargs)

        if engine is not None:
            self.engine = engine

    def _copy_kwargs(self, **kwargs):
        """Return the kwargs to create a copy of the instance."""
        attr_kw = [('_engine', 'engine')]
        ns = self.__dict__
        for attr, kw in attr_kw:
            assert kw not in kwargs
            if attr in ns:
                kwargs[kw] = ns[attr]
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

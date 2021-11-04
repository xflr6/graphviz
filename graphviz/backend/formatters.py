import typing

from .. import copying

__all__ = ['FORMATTERS', 'Formatter']

FORMATTERS = {'cairo',
              'core',
              'gd',
              'gdiplus',
              'gdwbmp',
              'xlib'}


class Formatter:

    _formatter = None

    def __init__(self, *, formatter: typing.Optional[str] = None, **kwargs):
        super().__init__(**kwargs)

        self.formatter = formatter

    def _copy_kwargs(self, **kwargs):
        """Return the kwargs to create a copy of the instance."""
        attr_kw = [('_formatter', 'formatter')]
        ns = self.__dict__
        for attr, kw in attr_kw:
            assert kw not in kwargs
            if attr in ns:
                kwargs[kw] = ns[attr]
        return super()._copy_kwargs(**kwargs)

    @property
    def formatter(self) -> typing.Optional[str]:
        """The output formatter used for rendering
            (``'cairo'``, ``'gd'``, ...)."""
        return self._formatter

    @formatter.setter
    def formatter(self, formatter: typing.Optional[str]) -> None:
        if formatter is None:
            self.__dict__.pop('_formatter', None)
        else:
            formatter = formatter.lower()
            if formatter not in FORMATTERS:
                 raise ValueError(f'unknown formatter: {formatter!r}')
            self._formatter = formatter

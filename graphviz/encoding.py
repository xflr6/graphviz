"""Default endoding: 'utf-8'."""

import codecs
import locale

from . import copying

__all__ = ['DEFAULT_ENCODING', 'Encoding']

DEFAULT_ENCODING = 'utf-8'


class Encoding(copying.Copy):
    """the default encoding for input and output."""

    _encoding = DEFAULT_ENCODING

    def __init__(self, encoding=DEFAULT_ENCODING, **kwargs):
        super().__init__(**kwargs)

        self.encoding = encoding

    def _copy_kwargs(self, **kwargs):
        """Return the kwargs to create a copy of the instance."""
        return super()._copy_kwargs(encoding=self._encoding, **kwargs)

    @property
    def encoding(self):
        """The encoding for the saved source file."""
        return self._encoding

    @encoding.setter
    def encoding(self, encoding):
        if encoding is None:
            encoding = locale.getpreferredencoding()
        codecs.lookup(encoding)  # raise early
        self._encoding = encoding

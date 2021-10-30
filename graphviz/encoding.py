"""Default endoding: 'utf-8'."""

import codecs
import locale

__all__ = ['Encoding']

DEFAULT_ENCODING = 'utf-8'


class Encoding:

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

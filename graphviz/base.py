"""Iterables of DOT source code lines (including final newline)."""

import codecs
import locale

__all__ = ['Base']

ENCODING = 'utf-8'


class Base:

    def _kwargs(self):
        ns = self.__dict__
        return {a[1:]: ns[a] for a in ('_format', '_engine', '_encoding')
                if a in ns}

    def __str__(self):
        """The DOT source code as string."""
        return self.source

    @property
    def source(self) -> str:
        """The generated DOT source code as string."""
        return ''.join(self)

    def __iter__(self):
        r"""Yield the generated DOT source line by line.

        Yields: Line ending with a newline (``'\n'``).
        """
        raise NotImplementedError('to be implemented by concrete subclasses')

    def copy(self):
        """Return a copied instance of the object.

        Returns:
            An independent copy of the current object.
        """
        kwargs = self._kwargs()
        return self.__class__(**kwargs)

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

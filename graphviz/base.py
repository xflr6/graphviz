"""Iterables of DOT source code lines (including final newline)."""

from . import copying

__all__ = ['Base']


class LineIterator:
    """Iterable of DOT Source code lines."""

    def __iter__(self):
        r"""Yield the generated DOT source line by line.

        Yields: Line ending with a newline (``'\n'``).
        """
        raise NotImplementedError('to be implemented by concrete subclasses')


# Common base interface for all exposed classes
class Base(LineIterator, copying.Copy):
    """LineIterator with ``.source`` attribute, that it returns for ``str()``."""

    @property
    def source(self) -> str:
        raise NotImplementedError('to be implemented by concrete subclasses')

    def __str__(self):
        """The DOT source code as string."""
        return self.source

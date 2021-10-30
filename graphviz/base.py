"""Iterables of DOT source code lines (including final newline)."""

__all__ = ['Base']


class SourceLineIterator:
    """Iterable of DOT Source code lines."""

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


class Base(SourceLineIterator):
    """Common base interface for all exposed classes."""

    def copy(self):
        """Return a copied instance of the object.

        Returns:
            An independent copy of the current object.
        """
        kwargs = self._kwargs()
        return self.__class__(**kwargs)

    def _kwargs(self):
        ns = self.__dict__
        return {a[1:]: ns[a] for a in ('_format', '_engine', '_encoding')
                if a in ns}

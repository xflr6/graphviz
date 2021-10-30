"""Save DOT code objects, render with Graphviz dot, and open in viewer."""

import locale
import logging
import os

from . import backend
from . import jupyter_integration
from . import rendering

__all__ = ['Source']


log = logging.getLogger(__name__)


class Source(jupyter_integration.JupyterSvgIntegration,
             rendering.Render):
    """Verbatim DOT source code string to be rendered by Graphviz.

    Args:
        source: The verbatim DOT source code string.
        filename: Filename for saving the source (defaults to ``'Source.gv'``).
        directory: (Sub)directory for source saving and rendering.
        format: Rendering output format (``'pdf'``, ``'png'``, ...).
        engine: Layout command used (``'dot'``, ``'neato'``, ...).
        encoding: Encoding for saving the source.

    Note:
        All parameters except ``source`` are optional. All of them
        can be changed under their corresponding attribute name
        after instance creation.
    """

    @classmethod
    def from_file(cls, filename, directory=None,
                  format=None, engine=None, encoding=backend.ENCODING):
        """Return an instance with the source string read from the given file.

        Args:
            filename: Filename for loading/saving the source.
            directory: (Sub)directory for source loading/saving and rendering.
            format: Rendering output format (``'pdf'``, ``'png'``, ...).
            engine: Layout command used (``'dot'``, ``'neato'``, ...).
            encoding: Encoding for loading/saving the source.
        """
        filepath = os.path.join(directory or '', filename)
        if encoding is None:
            encoding = locale.getpreferredencoding()
        log.debug('read %r with encoding %r', filepath, encoding)
        with open(filepath, encoding=encoding) as fd:
            source = fd.read()
        return cls(source, filename, directory, format, engine, encoding)

    def __init__(self, source, filename=None, directory=None,
                 format=None, engine=None, encoding=backend.ENCODING):
        super().__init__(filename, directory, format, engine, encoding)
        self._source = source  #: The verbatim DOT source code string.

    def _kwargs(self):
        result = super()._kwargs()
        result['source'] = self._source
        return result

    def __iter__(self):
        r"""Yield the DOT source code read from file line by line.

        Yields: Line ending with a newline (``'\n'``).
        """
        lines = self.source.splitlines(keepends=True)
        for line in lines[:-1]:
            yield line
        for line in lines[-1:]:
            suffix = '\n' if not line.endswith('\n') else ''
            yield line + suffix

    @property
    def source(self):
        """The DOT source code as string (read from file)."""
        return self._source

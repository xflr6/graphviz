"""Save DOT code objects, render with Graphviz dot, and open in viewer."""

import locale
import logging
import os
import typing

from .encoding import DEFAULT_ENCODING as ENCODING
from . import base
from . import files
from . import jupyter_integration
from . import rendering

__all__ = ['Source']


log = logging.getLogger(__name__)


class Source(jupyter_integration.JupyterSvgIntegration,
             rendering.Render,
             files.File,
             base.Base):
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
                  format=None, engine=None, encoding=ENCODING):
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
        return cls(source, filename, directory, format, engine, encoding,
                   loaded_from_path=filepath)

    def __init__(self, source, filename=None, directory=None,
                 format=None, engine=None, encoding=ENCODING, *,
                 loaded_from_path: typing.Optional[os.PathLike] = None):
        super().__init__(filename, directory, format, engine, encoding)
        self._loaded_from_path = loaded_from_path
        self._source = source  #: The verbatim DOT source code string.

    def _kwargs(self):
        result = super()._kwargs()
        result['source'] = self._source
        return result

    def __iter__(self):
        r"""Yield the DOT source code read from file line by line.

        Yields: Line ending with a newline (``'\n'``).
        """
        lines = self._source.splitlines(keepends=True)
        for line in lines[:-1]:
            yield line
        for line in lines[-1:]:
            suffix = '\n' if not line.endswith('\n') else ''
            yield line + suffix

    @property
    def source(self):
        """The DOT source code as string (read from file)."""
        return self._source

    def save(self, filename=None, directory=None,
             *, dry_run: typing.Optional[bool] = None):
        """Save the DOT source to file. Ensure the file ends with a newline.

        Args:
            filename: Filename for saving the source (defaults to ``name`` + ``'.gv'``)
            directory: (Sub)directory for source saving and rendering.
            dry_run: Skip file write (default: ``None``).
                By default skips if instance was loaded from the target path:
                ``.from_file(self.filepath)``.

        Returns:
            The (possibly relative) path of the saved source file.
        """
        if (dry_run is None
            and self._loaded_from_path
            and os.path.samefile(self._loaded_from_path, self.filepath)):
            dry_run = True

        return super().save(filename=filename, directory=directory,
                            dry_run=dry_run)
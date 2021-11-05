"""Save DOT source lines to a file."""

import logging
import os
import typing

from . import base
from . import encoding
from . import tools

__all__ = ['Save']

log = logging.getLogger(__name__)


class Save(encoding.Encoding, base.Base):
    """Save DOT source lines to file."""

    directory = ''

    _default_extension = 'gv'

    _mkdirs = staticmethod(tools.mkdirs)

    def __init__(self, filename=None, directory=None, **kwargs) -> None:
        super().__init__(**kwargs)

        if filename is None:
            name = getattr(self, 'name', None) or self.__class__.__name__
            filename = f'{name}.{self._default_extension}'
        self.filename = filename

        if directory is not None:
            self.directory = directory

    def _copy_kwargs(self, **kwargs):
        """Return the kwargs to create a copy of the instance."""
        assert 'directory' not in kwargs
        if 'directory' in self.__dict__:
            kwargs['directory'] = self.directory
        return super()._copy_kwargs(filename=self.filename, **kwargs)

    @property
    def filepath(self) -> str:
        return os.path.join(self.directory, self.filename)

    def save(self, filename=None, directory=None, *,
             skip_existing: typing.Optional[bool] = False) -> str:
        """Save the DOT source to file. Ensure the file ends with a newline.

        Args:
            filename: Filename for saving the source (defaults to ``name`` + ``'.gv'``)
            directory: (Sub)directory for source saving and rendering.
            skip_existing: Skip write if file exists (default: ``False``).

        Returns:
            The (possibly relative) path of the saved source file.
        """
        if filename is not None:
            self.filename = filename
        if directory is not None:
            self.directory = directory

        filepath = self.filepath
        if skip_existing and os.path.exists(filepath):
            return filepath

        self._mkdirs(filepath)

        log.debug('write lines to %r', filepath)
        with open(filepath, 'w', encoding=self.encoding) as fd:
            for uline in self:
                fd.write(uline)

        return filepath

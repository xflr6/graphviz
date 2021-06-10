# files.py - save, render, view

"""Save DOT code objects, render with Graphviz dot, and open in viewer."""

import codecs
import locale
import logging
import os

from . import backend
from . import tools

__all__ = ['File', 'Source']


log = logging.getLogger(__name__)


class Base(object):

    _engine = 'dot'

    _format = 'pdf'

    _encoding = backend.ENCODING

    @property
    def engine(self):
        """The layout commmand used for rendering (``'dot'``, ``'neato'``, ...)."""
        return self._engine

    @engine.setter
    def engine(self, engine):
        engine = engine.lower()
        if engine not in backend.ENGINES:
            raise ValueError(f'unknown engine: {engine!r}')
        self._engine = engine

    @property
    def format(self):
        """The output format used for rendering (``'pdf'``, ``'png'``, ...)."""
        return self._format

    @format.setter
    def format(self, format):
        format = format.lower()
        if format not in backend.FORMATS:
            raise ValueError(f'unknown format: {format!r}')
        self._format = format

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


class File(Base):

    directory = ''

    _default_extension = 'gv'

    def __init__(self, filename=None, directory=None,
                 format=None, engine=None, encoding=backend.ENCODING):
        if filename is None:
            name = getattr(self, 'name', None) or self.__class__.__name__
            filename = f'{name}.{self._default_extension}'
        self.filename = filename

        if directory is not None:
            self.directory = directory

        if format is not None:
            self.format = format

        if engine is not None:
            self.engine = engine

        self.encoding = encoding

    def _kwargs(self):
        result = super()._kwargs()
        result['filename'] = self.filename
        if 'directory' in self.__dict__:
            result['directory'] = self.directory
        return result

    def __str__(self):
        """The DOT source code as string."""
        return self.source

    def unflatten(self, stagger=None, fanout=False, chain=None):
        """Return a new :class:`.Source` instance with the source piped through the Graphviz *unflatten* preprocessor.

        Args:
            stagger (int): Stagger the minimum length of leaf edges between 1 and this small integer.
            fanout (bool): Fanout nodes with indegree = outdegree = 1 when staggering (requires ``stagger``).
            chain (int): Form disconnected nodes into chains of up to this many nodes.

        Returns:
            Source: Prepocessed DOT source code (improved layout aspect ratio).

        Raises:
            graphviz.RequiredArgumentError: If ``fanout`` is given but ``stagger`` is None.
            graphviz.ExecutableNotFound: If the Graphviz unflatten executable is not found.
            subprocess.CalledProcessError: If the exit status is non-zero.

        See also:
            https://www.graphviz.org/pdf/unflatten.1.pdf
        """
        out = backend.unflatten(self.source,
                                stagger=stagger, fanout=fanout, chain=chain,
                                encoding=self._encoding)
        return Source(out,
                      filename=self.filename, directory=self.directory,
                      format=self._format, engine=self._engine,
                      encoding=self._encoding)

    def _repr_svg_(self):
        return self.pipe(format='svg').decode(self._encoding)

    def pipe(self, format=None, renderer=None, formatter=None, quiet=False):
        """Return the source piped through the Graphviz layout command.

        Args:
            format: The output format used for rendering (``'pdf'``, ``'png'``, etc.).
            renderer: The output renderer used for rendering (``'cairo'``, ``'gd'``, ...).
            formatter: The output formatter used for rendering (``'cairo'``, ``'gd'``, ...).
            quiet (bool): Suppress ``stderr`` output from the layout subprocess.

        Returns:
            Binary (encoded) stdout of the layout command.

        Raises:
            ValueError: If ``format``, ``renderer``, or ``formatter`` are not known.
            graphviz.RequiredArgumentError: If ``formatter`` is given but ``renderer`` is None.
            graphviz.ExecutableNotFound: If the Graphviz executable is not found.
            subprocess.CalledProcessError: If the exit status is non-zero.
        """
        if format is None:
            format = self._format

        data = self.source.encode(self._encoding)

        out = backend.pipe(self._engine, format, data,
                           renderer=renderer, formatter=formatter,
                           quiet=quiet)

        return out

    @property
    def filepath(self):
        return os.path.join(self.directory, self.filename)

    def save(self, filename=None, directory=None):
        """Save the DOT source to file. Ensure the file ends with a newline.

        Args:
            filename: Filename for saving the source (defaults to ``name`` + ``'.gv'``)
            directory: (Sub)directory for source saving and rendering.

        Returns:
            The (possibly relative) path of the saved source file.
        """
        if filename is not None:
            self.filename = filename
        if directory is not None:
            self.directory = directory

        filepath = self.filepath
        tools.mkdirs(filepath)

        log.debug('write %d bytes to %r', len(self.source), filepath)
        with open(filepath, 'w', encoding=self.encoding) as fd:
            fd.write(self.source)
            if not self.source.endswith('\n'):
                fd.write('\n')

        return filepath

    def render(self, filename=None, directory=None, view=False, cleanup=False,
               format=None, renderer=None, formatter=None,
               quiet=False, quiet_view=False):
        """Save the source to file and render with the Graphviz engine.

        Args:
            filename: Filename for saving the source (defaults to ``name`` + ``'.gv'``)
            directory: (Sub)directory for source saving and rendering.
            view (bool): Open the rendered result with the default application.
            cleanup (bool): Delete the source file after rendering.
            format: The output format used for rendering (``'pdf'``, ``'png'``, etc.).
            renderer: The output renderer used for rendering (``'cairo'``, ``'gd'``, ...).
            formatter: The output formatter used for rendering (``'cairo'``, ``'gd'``, ...).
            quiet (bool): Suppress ``stderr`` output from the layout subprocess.
            quiet_view (bool): Suppress ``stderr`` output from the viewer process
                               (implies ``view=True``, ineffective on Windows).

        Returns:
            The (possibly relative) path of the rendered file.

        Raises:
            ValueError: If ``format``, ``renderer``, or ``formatter`` are not known.
            graphviz.RequiredArgumentError: If ``formatter`` is given but ``renderer`` is None.
            graphviz.ExecutableNotFound: If the Graphviz executable is not found.
            subprocess.CalledProcessError: If the exit status is non-zero.
            RuntimeError: If viewer opening is requested but not supported.

        The layout command is started from the directory of ``filepath``, so that
        references to external files (e.g. ``[image=...]``) can be given as paths
        relative to the DOT source file.
        """
        filepath = self.save(filename, directory)

        if format is None:
            format = self._format

        try:
            rendered = backend.render(self._engine, format, filepath,
                                    renderer=renderer, formatter=formatter,
                                    quiet=quiet)
        finally:
            if cleanup:
                log.debug('delete %r', filepath)
                os.remove(filepath)

        if quiet_view or view:
            self._view(rendered, self._format, quiet_view)

        return rendered

    def view(self, filename=None, directory=None, cleanup=False,
             quiet=False, quiet_view=False):
        """Save the source to file, open the rendered result in a viewer.

        Args:
            filename: Filename for saving the source (defaults to ``name`` + ``'.gv'``)
            directory: (Sub)directory for source saving and rendering.
            cleanup (bool): Delete the source file after rendering.
            quiet (bool): Suppress ``stderr`` output from the layout subprocess.
            quiet_view (bool): Suppress ``stderr`` output from the viewer process
                               (ineffective on Windows).

        Returns:
            The (possibly relative) path of the rendered file.

        Raises:
            graphviz.ExecutableNotFound: If the Graphviz executable is not found.
            subprocess.CalledProcessError: If the exit status is non-zero.
            RuntimeError: If opening the viewer is not supported.

        Short-cut method for calling :meth:`.render` with ``view=True``.

        Note:
            There is no option to wait for the application to close, and no way
            to retrieve the application's exit status.
        """
        return self.render(filename=filename, directory=directory,
                           view=True, cleanup=cleanup,
                           quiet=quiet, quiet_view=quiet_view)

    def _view(self, filepath, format, quiet):
        """Start the right viewer based on file format and platform."""
        methodnames = [
            f'_view_{format}_{backend.PLATFORM}',
            f'_view_{backend.PLATFORM}',
        ]
        for name in methodnames:
            view_method = getattr(self, name, None)
            if view_method is not None:
                break
        else:
            raise RuntimeError(f'{self.__class__!r} has no built-in viewer'
                               f' support for {format!r}'
                               f' on {backend.PLATFORM!r} platform')
        view_method(filepath, quiet=quiet)

    _view_darwin = staticmethod(backend.view.darwin)
    _view_freebsd = staticmethod(backend.view.freebsd)
    _view_linux = staticmethod(backend.view.linux)
    _view_windows = staticmethod(backend.view.windows)


class Source(File):
    """Verbatim DOT source code string to be rendered by Graphviz.

    Args:
        source: The verbatim DOT source code string.
        filename: Filename for saving the source (defaults to ``'Source.gv'``).
        directory: (Sub)directory for source saving and rendering.
        format: Rendering output format (``'pdf'``, ``'png'``, ...).
        engine: Layout command used (``'dot'``, ``'neato'``, ...).
        encoding: Encoding for saving the source.

    Note:
        All parameters except ``source`` are optional. All of them can be changed
        under their corresponding attribute name after instance creation.
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
        self.source = source  #: The verbatim DOT source code string.

    def _kwargs(self):
        result = super()._kwargs()
        result['source'] = self.source
        return result

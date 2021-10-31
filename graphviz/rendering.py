"""Save DOT code objects, render with Graphviz dot, and open in viewer."""

import codecs
import logging
import os
import typing

from . import backend
from . import base
from . import encoding
from . import files
from . import tools
from . import unflattening

__all__ = ['Render']


log = logging.getLogger(__name__)


class Pipe(base.Base, backend.Graphviz, encoding.Encoding):
    """Pipe source lines through the Graphviz layout command."""

# FIXME: pytype
##    @typing.overload
##    def pipe(self,
##             format: typing.Optional[str] = ...,
##             renderer: typing.Optional[str] = ...,
##             formatter: typing.Optional[str] = ...,
##             quiet: bool = ...,
##             *, encoding: _compat.Literal[None] = ...) -> bytes:
##        ...
##
##    @typing.overload
##    def pipe(self,
##             format: typing.Optional[str] = ...,
##             renderer: typing.Optional[str] = ...,
##             formatter: typing.Optional[str] = ...,
##             quiet: bool = ...,
##             *, encoding: str = ...) -> str:
##        ...
    def pipe(self,
             format: typing.Optional[str] = None,
             renderer: typing.Optional[str] = None,
             formatter: typing.Optional[str] = None,
             quiet: bool = False,
             *, encoding: typing.Optional[str] = None
             ) -> typing.Union[bytes, str]:
        """Return the source piped through the Graphviz layout command.

        Args:
            format: The output format used for rendering
                (``'pdf'``, ``'png'``, etc.).
            renderer: The output renderer used for rendering
                (``'cairo'``, ``'gd'``, ...).
            formatter: The output formatter used for rendering
                (``'cairo'``, ``'gd'``, ...).
            quiet (bool): Suppress ``stderr`` output
                from the layout subprocess.
            encoding: Encoding for decoding the stdout.

        Returns:
            Bytes or if encoding is given decoded string
                (stdout of the layout command).

        Raises:
            ValueError: If ``engine``, ``format``, ``renderer``, or ``formatter``
                are not known.
            graphviz.RequiredArgumentError: If ``formatter`` is given
                but ``renderer`` is None.
            graphviz.ExecutableNotFound: If the Graphviz 'dot' executable
                is not found.
            subprocess.CalledProcessError: If the returncode (exit status)
                of the rendering 'dot' subprocess is non-zero.

        Example:
            >>> import graphviz

            >>> source = 'graph { spam }'

            >>> graphviz.Source(source, format='svg').pipe()[:14]
            b'<?xml version='

            >>> graphviz.Source(source, format='svg').pipe(encoding='ascii')[:14]
            '<?xml version='

            >>> graphviz.Source(source, format='svg').pipe(encoding='utf-8')[:14]
            '<?xml version='
        """
        if format is None:
            format = self._format

        args = [self._engine, format, iter(self)]
        kwargs = {'renderer': renderer, 'formatter': formatter, 'quiet': quiet}

        if encoding is not None:
            if codecs.lookup(encoding) is codecs.lookup(self._encoding):
                # common case: both stdin and stdout need the same encoding
                return backend.pipe_lines_string(*args, encoding=encoding, **kwargs)
            raw = backend.pipe_lines(*args, input_encoding=self._encoding, **kwargs)
            return raw.decode(encoding)
        return backend.pipe_lines(*args, input_encoding=self._encoding, **kwargs)


class RenderFile(files.File, base.Base, backend.Graphviz, encoding.Encoding):
    """Write source lines to file and render with Graphviz."""

    def render(self, filename=None, directory=None, view=False, cleanup=False,
               format=None, renderer=None, formatter=None,
               quiet=False, quiet_view=False):
        """Save the source to file and render with the Graphviz engine.

        Args:
            filename: Filename for saving the source
                (defaults to ``name`` + ``'.gv'``).s
            directory: (Sub)directory for source saving and rendering.
            view (bool): Open the rendered result
                with the default application.
            cleanup (bool): Delete the source file
                after successful rendering.
            format: The output format used for rendering
                (``'pdf'``, ``'png'``, etc.).
            renderer: The output renderer used for rendering
                (``'cairo'``, ``'gd'``, ...).
            formatter: The output formatter used for rendering
                (``'cairo'``, ``'gd'``, ...).
            quiet (bool): Suppress ``stderr`` output
                from the layout subprocess.
            quiet_view (bool): Suppress ``stderr`` output
                from the viewer process
                (implies ``view=True``, ineffective on Windows).

        Returns:
            The (possibly relative) path of the rendered file.

        Raises:
            ValueError: If ``engine``, ``format``, ``renderer``, or ``formatter``
                are not known.
            graphviz.RequiredArgumentError: If ``formatter`` is given
                but ``renderer`` is None.
            graphviz.ExecutableNotFound: If the Graphviz 'dot' executable
                is not found.
            subprocess.CalledProcessError: If the returncode (exit status)
                of the rendering 'dot' subprocess is non-zero.
            RuntimeError: If viewer opening is requested but not supported.

        Note:
            The layout command is started from the directory of ``filepath``,
            so that references to external files
            (e.g. ``[image=images/camelot.png]``)
            can be given as paths relative to the DOT source file.
        """
        filepath = self.save(filename, directory, skip_existing=None)

        if format is None:
            format = self._format

        rendered = backend.render(self._engine, format, filepath,
                                  renderer=renderer, formatter=formatter,
                                  quiet=quiet)

        if cleanup:
            log.debug('delete %r', filepath)
            os.remove(filepath)

        if quiet_view or view:
            self._view(rendered, self._format, quiet_view)

        return rendered


class RenderFileView(RenderFile):
    """Convenience short-cut for running ``.render(view=True)``."""

    def view(self, filename=None, directory=None, cleanup=False,
             quiet=False, quiet_view=False):
        """Save the source to file, open the rendered result in a viewer.

        Args:
            filename: Filename for saving the source
                (defaults to ``name`` + ``'.gv'``).
            directory: (Sub)directory for source saving and rendering.
            cleanup (bool): Delete the source file after successful rendering.
            quiet (bool): Suppress ``stderr`` output from the layout subprocess.
            quiet_view (bool): Suppress ``stderr`` output
                from the viewer process (ineffective on Windows).

        Returns:
            The (possibly relative) path of the rendered file.

        Raises:
            graphviz.ExecutableNotFound: If the Graphviz executable
                is not found.
            subprocess.CalledProcessError: If the exit status is non-zero.
            RuntimeError: If opening the viewer is not supported.

        Short-cut method for calling :meth:`.render` with ``view=True``.

        Note:
            There is no option to wait for the application to close,
            and no way to retrieve the application's exit status.
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

    _view_darwin = staticmethod(backend.view_darwin)
    _view_freebsd = staticmethod(backend.view_unixoid)
    _view_linux = staticmethod(backend.view_unixoid)
    _view_windows = staticmethod(backend.view_windows)


@tools.setattr_add('render.pipe', Pipe.pipe)
@tools.setattr_add('render.file', RenderFile.render)
@tools.setattr_add('render.view', RenderFileView.view)
@tools.setattr_add('render.unflatten', unflattening.Unflatten.unflatten)
class Render(RenderFileView, RenderFile, Pipe, unflattening.Unflatten):
    """Render fules, pipe, unflatten."""

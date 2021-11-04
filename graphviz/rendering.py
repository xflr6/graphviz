"""Save DOT code objects, render with Graphviz dot, and open in viewer."""

import codecs
import logging
import os
import typing

from . import backend
from . import base
from . import encoding
from . import saving

__all__ = ['Pipe', 'Render']


log = logging.getLogger(__name__)


class Pipe(encoding.Encoding, base.Base, backend.Pipe):
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
        kwargs = self._get_pipe_kwargs(format=format,
                                       renderer=renderer,
                                       formatter=formatter,
                                       quiet=quiet)
        format = kwargs.pop('format')

        args = [self._engine, format, iter(self)]

        if encoding is not None:
            if codecs.lookup(encoding) is codecs.lookup(self._encoding):
                # common case: both stdin and stdout need the same encoding
                return self._pipe_lines_string(*args, encoding=encoding, **kwargs)
            raw = self._pipe_lines(*args, input_encoding=self._encoding, **kwargs)
            return raw.decode(encoding)
        return self._pipe_lines(*args, input_encoding=self._encoding, **kwargs)


class Render(saving.Save, backend.Render, backend.View):
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
        kwargs = self._get_render_kwargs(format=format,
                                         renderer=renderer,
                                         formatter=formatter,
                                         quiet=quiet)
        format = kwargs.pop('format')

        filepath = self.save(filename, directory, skip_existing=None)

        rendered = self._render(self._engine, format, filepath, **kwargs)

        if cleanup:
            log.debug('delete %r', filepath)
            os.remove(filepath)

        if quiet_view or view:
            self._view(rendered, self._format, quiet_view)

        return rendered

    def _view(self, filepath, format, quiet):
        """Start the right viewer based on file format and platform."""
        methodnames = [
            f'_view_{format}_{backend.viewing.PLATFORM}',
            f'_view_{backend.viewing.PLATFORM}',
        ]
        for name in methodnames:
            view_method = getattr(self, name, None)
            if view_method is not None:
                break
        else:
            raise RuntimeError(f'{self.__class__!r} has no built-in viewer'
                               f' support for {format!r}'
                               f' on {backend.viewing.PLATFORM!r} platform')
        view_method(filepath, quiet=quiet)

    def view(self, filename=None, directory=None, cleanup=False,
             quiet=False, quiet_view=False):
        """Save the source to file, open the rendered result in a viewer.

        Convenience short-cut for running ``.render(view=True)``.

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

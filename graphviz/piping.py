"""Pipe DOT code objects through Graphviz ``dot``."""

import codecs
import logging
from typing import overload

from . import _tools
from . import backend
from . import exceptions
from . import base
from . import encoding

__all__ = ['Pipe']


log = logging.getLogger(__name__)


class Pipe(encoding.Encoding, base.Base, backend.Pipe):
    """Pipe source lines through the Graphviz layout command."""

    @overload
    def pipe(self,
             format: str | None = ...,
             renderer: str | None = ...,
             formatter: str | None = ...,
             neato_no_op: bool | int | None = ...,
             quiet: bool = ..., *,
             y_invert: bool = ...,
             engine: str | None = ...,
             encoding: None = ...) -> bytes:
        """Return bytes with default ``encoding=None``."""

    @overload
    def pipe(self,
             format: str | None = ...,
             renderer: str | None = ...,
             formatter: str | None = ...,
             neato_no_op: bool | int | None = ...,
             quiet: bool = ..., *,
             y_invert: bool = ...,
             engine: str | None = ...,
             encoding: str) -> str:
        """Return string when given encoding."""

    @overload
    def pipe(self,
             format: str | None = ...,
             renderer: str | None = ...,
             formatter: str | None = ...,
             neato_no_op: bool | int | None = ...,
             quiet: bool = ..., *,
             y_invert: bool = ...,
             engine: str | None = ...,
             encoding: str | None) -> bytes | str:
        """Return bytes or string depending on encoding argument."""

    def pipe(self,
             format: str | None = None,
             renderer: str | None = None,
             formatter: str | None = None,
             neato_no_op: bool | int | None = None,
             quiet: bool = False, *,
             y_invert: bool = False,
             engine: str | None = None,
             encoding: str | None = None) -> bytes | str:
        """Return the source piped through the Graphviz layout command.

        Args:
            format: The output format used for rendering
                (``'pdf'``, ``'png'``, etc.).
            renderer: The output renderer used for rendering
                (``'cairo'``, ``'gd'``, ...).
            formatter: The output formatter used for rendering
                (``'cairo'``, ``'gd'``, ...).
            neato_no_op: Neato layout engine no-op flag.
            quiet (bool): Suppress ``stderr`` output
                from the layout subprocess.
            y_invert: Invert y coordinates in the rendered output.
            engine: Layout engine for rendering
                (``'dot'``, ``'neato'``, ...).
            encoding: Encoding for decoding the stdout.

        Returns:
            Bytes or if encoding is given decoded string
                (stdout of the layout command).

        Raises:
            ValueError: If ``engine``, ``format``, ``renderer``, or ``formatter``
                are unknown.
            graphviz.RequiredArgumentError: If ``formatter`` is given
                but ``renderer`` is None.
            graphviz.ExecutableNotFound: If the Graphviz ``dot`` executable
                is not found.
            graphviz.CalledProcessError: If the returncode (exit status)
                of the rendering ``dot`` subprocess is non-zero.

        Example:
            >>> doctest_mark_exe()
            >>> import graphviz
            >>> source = 'graph { spam }'
            >>> graphviz.Source(source, format='svg').pipe()[:14]
            b'<?xml version='
            >>> graphviz.Source(source, format='svg').pipe(encoding='ascii')[:14]
            '<?xml version='
            >>> graphviz.Source(source, format='svg').pipe(encoding='utf-8')[:14]
            '<?xml version='
        """
        return self._pipe_legacy(format,
                                 renderer=renderer,
                                 formatter=formatter,
                                 neato_no_op=neato_no_op,
                                 quiet=quiet,
                                 y_invert=y_invert,
                                 engine=engine,
                                 encoding=encoding)

    @_tools.deprecate_positional_args(supported_number=1, ignore_arg='self')
    def _pipe_legacy(self,
                     format: str | None = None,
                     renderer: str | None = None,
                     formatter: str | None = None,
                     neato_no_op: bool | int | None = None,
                     quiet: bool = False, *,
                     y_invert: bool = False,
                     engine: str | None = None,
                     encoding: str | None = None) -> bytes | str:
        return self._pipe_future(format,
                                 renderer=renderer,
                                 formatter=formatter,
                                 neato_no_op=neato_no_op,
                                 quiet=quiet,
                                 engine=engine,
                                 encoding=encoding)

    def _pipe_future(self, format: str | None = None, *,
                     renderer: str | None = None,
                     formatter: str | None = None,
                     neato_no_op: bool | int | None = None,
                     y_invert: bool = False,
                     quiet: bool = False,
                     engine: str | None = None,
                     encoding: str | None = None) -> bytes | str:
        (args, kwargs) = self._get_pipe_parameters(engine=engine,
                                                   format=format,
                                                   renderer=renderer,
                                                   formatter=formatter,
                                                   y_invert=y_invert,
                                                   neato_no_op=neato_no_op,
                                                   quiet=quiet,
                                                   verify=True)

        args.append(iter(self))

        if encoding is not None:
            if codecs.lookup(encoding) is codecs.lookup(self.encoding):
                # common case: both stdin and stdout need the same encoding
                return self._pipe_lines_string(*args, encoding=encoding, **kwargs)
            try:
                raw = self._pipe_lines(*args, input_encoding=self.encoding, **kwargs)
            except exceptions.CalledProcessError as e:
                if (output := e.output) is not None:
                    output = output.decode(self.encoding)
                if (stderr := e.stderr) is not None:
                    stderr = stderr.decode(self.encoding)
                raise e.__class__(e.returncode, e.cmd, output=output, stderr=stderr)
            else:
                return raw.decode(encoding)
        return self._pipe_lines(*args, input_encoding=self.encoding, **kwargs)

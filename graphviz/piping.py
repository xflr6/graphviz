"""Pipe DOT code objects through Graphviz dot."""

import codecs
import logging
import typing

from . import backend
from . import base
from . import encoding

__all__ = ['Pipe']


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
        args, kwargs = self._get_pipe_parameters(format=format,
                                                 renderer=renderer,
                                                 formatter=formatter,
                                                 quiet=quiet)

        args.append(iter(self))

        if encoding is not None:
            if codecs.lookup(encoding) is codecs.lookup(self._encoding):
                # common case: both stdin and stdout need the same encoding
                return self._pipe_lines_string(*args, encoding=encoding, **kwargs)
            raw = self._pipe_lines(*args, input_encoding=self._encoding, **kwargs)
            return raw.decode(encoding)
        return self._pipe_lines(*args, input_encoding=self._encoding, **kwargs)

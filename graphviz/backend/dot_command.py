"""Check and assemble commands for running Graphviz ``dot``."""

import os
import pathlib
import typing

from . import _common
from . import engines
from . import formats
from . import formatters
from . import renderers

__all__ = ['command']

#: :class:`pathlib.Path` of layout command (``Path('dot')``).
DOT_BINARY = pathlib.Path('dot')


def command(engine: str, format_: str, *,
            renderer: typing.Optional[str] = None,
            formatter: typing.Optional[str] = None
            ) -> typing.List[typing.Union[os.PathLike, str]]:
    """Return ``subprocess.Popen`` argument list for rendering."""
    if formatter is not None and renderer is None:
        raise _common.RequiredArgumentError('formatter given without renderer')

    if engine not in engines.ENGINES:
        raise ValueError(f'unknown engine: {engine!r}')

    if format_ not in formats.FORMATS:
        raise ValueError(f'unknown format: {format_!r}')

    if renderer is not None and renderer not in renderers.RENDERERS:
        raise ValueError(f'unknown renderer: {renderer!r}')

    if formatter is not None and formatter not in formatters.FORMATTERS:
        raise ValueError(f'unknown formatter: {formatter!r}')

    output_format = [f for f in (format_, renderer, formatter) if f is not None]
    output_format_flag = ':'.join(output_format)

    return [DOT_BINARY, f'-K{engine}', f'-T{output_format_flag}']

"""Check and assemble commands for running Graphviz ``dot``."""

import os
import pathlib
import typing

from .. import parameters

from . import _common

__all__ = ['DOT_BINARY', 'command']

DOT_BINARY = pathlib.Path('dot')


def command(engine: str, format_: str, *,
            renderer: typing.Optional[str] = None,
            formatter: typing.Optional[str] = None
            ) -> typing.List[typing.Union[os.PathLike, str]]:
    """Return ``subprocess.Popen`` argument list for rendering."""
    if formatter is not None and renderer is None:
        raise _common.RequiredArgumentError('formatter given without renderer')

    parameters.verify_engine(engine, required=True)
    parameters.verify_format(format_, required=True)
    parameters.verify_renderer(renderer, required=False)
    parameters.verify_formatter(formatter, required=False)

    output_format = [f for f in (format_, renderer, formatter) if f is not None]
    output_format_flag = ':'.join(output_format)

    return [DOT_BINARY, f'-K{engine}', f'-T{output_format_flag}']

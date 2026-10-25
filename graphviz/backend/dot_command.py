"""Check and assemble commands for running Graphviz ``dot``."""

from collections.abc import Mapping
import os
import pathlib
from typing import Final

from .. import exceptions
from .. import parameters

__all__ = ['DOT_BINARY', 'command']

DOT_BINARY: Final = pathlib.Path('dot')


def command(engine: str, format_: str, *,
            renderer: str | None = None,
            formatter: str | None = None,
            neato_no_op: bool | int | None = None,
            graph_attr: Mapping[str, str] | None = None) -> list[os.PathLike[str] | str]:
    """Return ``subprocess.Popen`` argument list for rendering.

    See also:
        Upstream documentation:
        - https://www.graphviz.org/doc/info/command.html#-K
        - https://www.graphviz.org/doc/info/command.html#-T
        - https://www.graphviz.org/doc/info/command.html#-n
        - https://www.graphviz.org/doc/info/command.html#-G
    """
    if formatter is not None and renderer is None:
        raise exceptions.RequiredArgumentError('formatter given without renderer')

    parameters.verify_engine(engine, required=True)
    parameters.verify_format(format_, required=True)
    parameters.verify_renderer(renderer, required=False)
    parameters.verify_formatter(formatter, required=False)

    output_format = [f for f in (format_, renderer, formatter) if f is not None]
    output_format_flag = ':'.join(output_format)

    cmd: list[os.PathLike[str] | str]
    cmd = [DOT_BINARY, f'-K{engine}', f'-T{output_format_flag}']

    if neato_no_op:
        cmd.append(f'-n{neato_no_op:d}')

    if graph_attr is not None:
        cmd.extend(f'-G{name}={value}' for name, value in graph_attr.items())

    return cmd

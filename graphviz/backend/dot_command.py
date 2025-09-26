"""Check and assemble commands for running Graphviz ``dot``."""

import os
import pathlib
from typing import Final, List, Optional, Union

from .. import exceptions
from .. import parameters

__all__ = ['DOT_BINARY', 'command']

DOT_BINARY: Final = pathlib.Path('dot')


def command(engine: str, format_: str, *,
            renderer: Optional[str] = None,
            formatter: Optional[str] = None,
            neato_no_op: Union[bool, int, None] = None
            ) -> List[Union[os.PathLike[str], str]]:
    """Return ``subprocess.Popen`` argument list for rendering.

    See also:
        Upstream documentation:
        - https://www.graphviz.org/doc/info/command.html#-K
        - https://www.graphviz.org/doc/info/command.html#-T
        - https://www.graphviz.org/doc/info/command.html#-n
    """
    if formatter is not None and renderer is None:
        raise exceptions.RequiredArgumentError('formatter given without renderer')

    parameters.verify_engine(engine, required=True)
    parameters.verify_format(format_, required=True)
    parameters.verify_renderer(renderer, required=False)
    parameters.verify_formatter(formatter, required=False)

    output_format = [f for f in (format_, renderer, formatter) if f is not None]
    output_format_flag = ':'.join(output_format)

    cmd: List[Union[os.PathLike[str], str]]
    cmd = [DOT_BINARY, f'-K{engine}', f'-T{output_format_flag}']

    if neato_no_op:
        cmd.append(f'-n{neato_no_op:d}')

    return cmd

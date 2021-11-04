import logging
import re
import subprocess
import typing

from . import running
from . import rendering


log = logging.getLogger(__name__)


def version() -> typing.Tuple[int, ...]:
    """Return the version number tuple
        from the ``stderr`` output of ``dot -V``.

    Returns:
        Two, three, or four ``int`` version ``tuple``.

    Raises:
        graphviz.ExecutableNotFound: If the Graphviz executable is not found.
        subprocess.CalledProcessError: If the exit status is non-zero.
        RuntimeError: If the output cannot be parsed into a version number.

    Example:
        >>> import graphviz
        >>> graphviz.version()  # doctest: +ELLIPSIS
        (...)

    Note:
        Ignores the ``~dev.<YYYYmmdd.HHMM>`` portion of development versions.

    See also:
        Graphviz Release version entry format:
        https://gitlab.com/graphviz/graphviz/-/blob/f94e91ba819cef51a4b9dcb2d76153684d06a913/gen_version.py#L17-20
    """
    cmd = [rendering.DOT_BINARY, '-V']
    log.debug('run %r', cmd)
    proc = running.run_check(cmd,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             encoding='ascii')

    ma = re.search(r'graphviz version'
                   r' '
                   r'(\d+)\.(\d+)'
                   r'(?:\.(\d+)'
                       r'(?:'  # noqa: E127
                           r'~dev\.\d{8}\.\d{4}'  # noqa: E127
                           r'|'
                           r'\.(\d+)'
                       r')?'
                   r')?'
                   r' ', proc.stdout)
    if ma is None:
        raise RuntimeError(f'cannot parse {cmd!r} output: {proc.stdout!r}')

    return tuple(int(d) for d in ma.groups() if d is not None)

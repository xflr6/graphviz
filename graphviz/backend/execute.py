"""Run subprocesses with ``subprocess.run()`` and ``subprocess.Popen()``."""

import errno
import logging
import os
import subprocess
import sys
import typing

from .. import _compat

__all__ = ['run_check', 'ExecutableNotFound']


log = logging.getLogger(__name__)


BytesOrStrIterator = typing.Union[typing.Iterator[bytes],
                                  typing.Iterator[str]]


@typing.overload
def run_check(cmd: typing.Sequence[typing.Union[os.PathLike, str]], *,
              input_lines: typing.Optional[typing.Iterator[bytes]] = ...,
              encoding: None = ...,
              capture_output: bool = ...,
              quiet: bool = ...,
              **kwargs) -> subprocess.CompletedProcess:
    """Accept bytes input_lines with default ``encoding=None```."""


@typing.overload
def run_check(cmd: typing.Sequence[typing.Union[os.PathLike, str]], *,
              input_lines: typing.Optional[typing.Iterator[str]] = ...,
              encoding: str,
              capture_output: bool = ...,
              quiet: bool = ...,
              **kwargs) -> subprocess.CompletedProcess:
    """Accept string input_lines when given ``encoding``."""


@typing.overload
def run_check(cmd: typing.Sequence[typing.Union[os.PathLike, str]], *,
              input_lines: typing.Optional[BytesOrStrIterator] = ...,
              encoding: typing.Optional[str] = ...,
              capture_output: bool = ...,
              quiet: bool = ...,
              **kwargs) -> subprocess.CompletedProcess:
    """Accept bytes or string input_lines depending on ``encoding``."""


def run_check(cmd: typing.Sequence[typing.Union[os.PathLike, str]], *,
              input_lines: typing.Optional[BytesOrStrIterator] = None,
              encoding: typing.Optional[str] = None,
              capture_output: bool = False,
              quiet: bool = False,
              **kwargs) -> subprocess.CompletedProcess:
    """Run the command described by ``cmd``
        with ``check=True`` and return its completed process.

    Raises:
        CalledProcessError: if the returncode of the subprocess is non-zero.
    """
    log.debug('run %r', cmd)

    if not kwargs.pop('check', True):  # pragma: no cover
        raise NotImplementedError('check must be True or omited')

    if capture_output:  # Python 3.6 compat
        kwargs['stdout'] = kwargs['stderr'] = subprocess.PIPE

    if encoding is not None:
        kwargs['encoding'] = encoding
    kwargs.setdefault('startupinfo', _compat.get_startupinfo())

    try:
        if input_lines is not None:
            assert kwargs.get('input') is None
            assert iter(input_lines) is input_lines
            popen = subprocess.Popen(cmd, stdin=subprocess.PIPE, **kwargs)
            stdin_write = popen.stdin.write
            for line in input_lines:
                stdin_write(line)
            stdout, stderr = popen.communicate()
            proc = subprocess.CompletedProcess(popen.args, popen.returncode,
                                               stdout=stdout, stderr=stderr)
        else:
            proc = subprocess.run(cmd, **kwargs)
    except OSError as e:
        if e.errno == errno.ENOENT:
            raise ExecutableNotFound(cmd) from e
        raise

    if not quiet and proc.stderr:
        stderr = proc.stderr
        if isinstance(stderr, bytes):
            stderr_encoding = (getattr(sys.stderr, 'encoding', None)
                               or sys.getdefaultencoding())
            stderr = stderr.decode(stderr_encoding)
        sys.stderr.write(stderr)
        sys.stderr.flush()

    try:
        proc.check_returncode()
    except subprocess.CalledProcessError as e:
        raise CalledProcessError(*e.args)

    return proc


class ExecutableNotFound(RuntimeError):
    """Exception raised if the Graphviz executable is not found."""

    _msg = ('failed to execute {!r}, '
            'make sure the Graphviz executables are on your systems\' PATH')

    def __init__(self, args) -> None:
        super().__init__(self._msg.format(*args))


class CalledProcessError(subprocess.CalledProcessError):
    """Exception raised if the returncode of the subprocess is non-zero."""

    def __str__(self) -> 'str':
        s = super().__str__()
        return f'{s} [stderr: {self.stderr!r}]'

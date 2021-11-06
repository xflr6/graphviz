"""Test helpers."""

import contextlib
import os
import pathlib
import platform
import subprocess

__all__ = ['EXPECTED_DOT_BINARY', 'EXPECTED_DEFAULT_ENCODING',
           'as_cwd',
           'check_startupinfo']

EXPECTED_DOT_BINARY = pathlib.Path('dot')

EXPECTED_DEFAULT_ENCODING = 'utf-8'


@contextlib.contextmanager
def as_cwd(path):
    """Return a context manager, which changes to the path's directory
        during the managed ``with`` context."""
    cwd = pathlib.Path().resolve()

    os.chdir(path)
    yield

    os.chdir(cwd)


def check_startupinfo(startupinfo):  # noqa: N803
    assert startupinfo is None


if platform.system().lower() == 'windows':
    def check_startupinfo(startupinfo):  # noqa: N803,F811
        assert isinstance(startupinfo, subprocess.STARTUPINFO)
        assert startupinfo.dwFlags & subprocess.STARTF_USESHOWWINDOW
        assert startupinfo.wShowWindow == subprocess.SW_HIDE

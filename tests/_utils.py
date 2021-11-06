"""Test helpers."""

import contextlib
import os
import pathlib
import platform
import subprocess

__all__ = ['as_cwd',
           'check_startupinfo']


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

"""Platform compatibility."""

import sys


def get_startupinfo() -> None:
    """Return None for startupinfo argument of ``subprocess.Popen``."""
    return None


assert get_startupinfo() is None, 'get_startupinfo() defaults to a no-op'  # type: ignore[func-returns-value]  # noqa: E501


# avoid platform.system() to work around https://github.com/python/mypy/issues/8166
if sys.platform == 'win32' or sys.platform == 'cygwin' or sys.platform == 'msys':  # pragma: no cover  # noqa: E501
    import subprocess

    def get_startupinfo() -> subprocess.STARTUPINFO:  # type: ignore[misc]  # noqa: E501
        """Return subprocess.STARTUPINFO instance hiding the console window."""
        startupinfo = subprocess.STARTUPINFO()  # pytype: disable=module-attr
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW  # pytype: disable=module-attr
        startupinfo.wShowWindow = subprocess.SW_HIDE  # pytype: disable=module-attr
        return startupinfo

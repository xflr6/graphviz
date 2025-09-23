"""Platform compatibility."""

import platform
import typing


def get_startupinfo() -> typing.Any:
    """Return None for startupinfo argument of ``subprocess.Popen``."""
    return None


assert get_startupinfo() is None, 'get_startupinfo() defaults to a no-op'


if platform.system() == 'Windows':  # pragma: no cover
    import subprocess

    def get_startupinfo() -> typing.Any:  # pytype: disable=module-attr
        """Return subprocess.STARTUPINFO instance hiding the console window."""
        startupinfo = subprocess.STARTUPINFO()  # pytype: disable=module-attr
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW  # pytype: disable=module-attr
        startupinfo.wShowWindow = subprocess.SW_HIDE  # pytype: disable=module-attr
        return startupinfo

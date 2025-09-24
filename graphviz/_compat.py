"""Platform compatibility."""

import platform


def get_startupinfo() -> None:
    """Return None for startupinfo argument of ``subprocess.Popen``."""
    return None


assert get_startupinfo() is None, 'get_startupinfo() defaults to a no-op'  # type: ignore[func-returns-value]  # noqa: E501


if platform.system() == 'Windows':  # pragma: no cover
    import subprocess

    def get_startupinfo() -> subprocess.STARTUPINFO:  # type: ignore[misc]  # noqa: E501
        """Return subprocess.STARTUPINFO instance hiding the console window."""
        startupinfo = subprocess.STARTUPINFO()  # pytype: disable=module-attr
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW  # pytype: disable=module-attr
        startupinfo.wShowWindow = subprocess.SW_HIDE  # pytype: disable=module-attr
        return startupinfo

"""Python 3.6 to 3.8 compatibility and platform compatibility."""

import platform
import sys
import typing

PY38 = (sys.version_info < (3, 9))


Literal: typing.Any


if PY38:
    import unittest.mock

    # pytype not supported
    Literal = unittest.mock.MagicMock(name='Literal')
else:
    from typing import Literal

    Literal = Literal


if platform.system() == 'Windows':  # pragma: no cover
    import subprocess

    def get_startupinfo():
        """Return subprocess.STARTUPINFO instance
            hiding the console window."""
        startupinfo = subprocess.STARTUPINFO()  # pytype: disable=module-attr
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW  # pytype: disable=module-attr
        startupinfo.wShowWindow = subprocess.SW_HIDE  # pytype: disable=module-attr
        return startupinfo
else:
    def get_startupinfo() -> None:
        """Return None for startupinfo argument of ``subprocess.Popen``."""
        return None

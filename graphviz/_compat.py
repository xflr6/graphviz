# _compat.py - Python 3.6 to 3.8 compatibility

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

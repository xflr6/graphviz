# _compat.py - Python 2/3 compatibility

import os
import sys

PY2 = sys.version_info[0] == 2


if PY2:  # pragma: no cover
    text_type = unicode

    def iteritems(d):
        return d.iteritems()

    def makedirs(name, mode=0o777, exist_ok=False):
        try:
            os.makedirs(name, mode)
        except OSError:
            if not exist_ok or not os.path.isdir(name):
                raise


else:  # pragma: no cover
    text_type = str

    def iteritems(d):
        return iter(d.items())

    makedirs = os.makedirs

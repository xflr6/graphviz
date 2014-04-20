# _compat.py - Python 2/3 compatibility

import sys

PY2 = sys.version_info[0] == 2


if PY2:
    text_type = unicode

    def iteritems(d):
        return d.iteritems()

else:
    text_type = str

    def iteritems(d):
        return iter(d.items())

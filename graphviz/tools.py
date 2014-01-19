# tools.py

import os
import errno

__all__ = ['mkdirs']


def mkdirs(filename, mode=0o777):
    """Recursively create directories up to the path of filename as needed."""
    path = os.path.dirname(filename)
    if not path:
        return

    try:
        os.makedirs(path, mode)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

# tools.py

import os
import errno

from ._compat import iteritems

__all__ = ['attach', 'mkdirs', 'mapping_items']


def attach(object, name):
    """Return a decorator doing setattr(object, name) with its argument."""
    def decorator(func):
        setattr(object, name, func)
        return func
    return decorator


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


def mapping_items(mapping):
    """Return an iterator over the mapping items, sort if it's a plain dict.

    >>> list(mapping_items({'spam': 0, 'ham': 1, 'eggs': 2}))
    [('eggs', 2), ('ham', 1), ('spam', 0)]

    >>> from collections import OrderedDict  # doctest: +SKIP
    >>> list(mapping_items(OrderedDict(enumerate(['spam', 'ham', 'eggs']))))  # doctest:+SKIP
    [(0, 'spam'), (1, 'ham'), (2, 'eggs')]
    """
    if type(mapping) is dict:
        return iter(sorted(iteritems(mapping)))
    return iteritems(mapping)

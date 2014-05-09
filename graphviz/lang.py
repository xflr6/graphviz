# lang.py - dot language creation helpers

"""Quote strings to be valid DOT identifiers, assemble attributes."""

import re

from .tools import mapping_items

__all__ = ['quote', 'attributes']

ID = re.compile(r'([a-zA-Z_][a-zA-Z0-9_]*|-?(\.\d+|\d+(\.\d*)?))$')
KEYWORD = re.compile(r'((node)|(edge)|(graph)|(digraph)|(subgraph)|(strict))$', re.IGNORECASE)

def quote(identifier, valid_id=ID.match, dot_keyword=KEYWORD.match):
    """Return DOT identifier from string, quote if needed.

    >>> quote('')
    '""'

    >>> quote('spam')
    'spam'

    >>> quote('Graph')
    '"Graph"'
    
    >>> quote('spam spam')
    '"spam spam"'

    >>> quote('-4.2')
    '-4.2'

    >>> quote('.42')
    '.42'
    """
    if not valid_id(identifier) or dot_keyword(identifier):
        return '"%s"' % identifier.replace('"', '\\"')
    return identifier


def attributes(label=None, kwargs=None, attributes=None, raw=None):
    """Return assembled DOT attributes string.

    Sorts kwargs and attributes if they are plain dicts (to avoid
    unpredictable order from hash randomization in Python 3.3+).

    >>> attributes()
    ''

    >>> attributes('spam spam', kwargs={'eggs':'eggs', 'ham': 'ham ham'})
    ' [label="spam spam" eggs=eggs ham="ham ham"]'

    >>> attributes(kwargs={'spam': None, 'eggs': ''})
    ' [eggs=""]'
    """
    if label is None:
        result = []
    else:
        result = ['label=%s' % quote(label)]

    if kwargs:
        items = ['%s=%s' % (quote(k), quote(v))
            for k, v in mapping_items(kwargs) if v is not None]
        result.extend(items)

    if attributes:
        if hasattr(attributes, 'items'):
            attributes = mapping_items(attributes)
        items = ['%s=%s' % (quote(k), quote(v))
            for k, v in attributes if v is not None]
        result.extend(items)

    if raw:
        result.append(raw)

    if not result:
        return ''
    return ' [%s]' % ' '.join(result)

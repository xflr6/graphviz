# lang.py - dot language creation helpers

import re

__all__ = ['quote', 'attributes']


ID = re.compile(r'([a-zA-Z_]\w*|-?(\.\d+|\d+(\.\d*)?))$')


def quote(identifier, valid_id=ID.match):
    """Return DOT identifier from string, quote if needed.

    >>> quote('')
    '""'

    >>> quote('spam')
    'spam'

    >>> quote('spam spam')
    '"spam spam"'

    >>> quote('"spam"') == '"' + chr(92) + '"' + 'spam' + chr(92) + '"' + '"'
    True

    >>> quote('-4.2')
    '-4.2'

    >>> quote('.42')
    '.42'
    """
    if not valid_id(identifier):
        return '"%s"' % identifier.replace('"', '\\"')
    return identifier


def attributes(label=None, kwargs=None, attributes=None, raw=None):
    """Return assembled DOT attributes string.

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
            for k, v in kwargs.iteritems() if v is not None]
        result.extend(items)

    if attributes:
        if hasattr(attributes, 'iteritems'):
            attributes = attributes.iteritems()
        items = ['%s=%s' % (quote(k), quote(v))
            for k, v in attributes if v is not None]
        result.extend(items)

    if raw:
        result.append(raw)

    if result:
        return ' [%s]' % ' '.join(result)
    return ''


def _test(verbose=False):
    import doctest
    doctest.testmod(verbose=verbose)

if __name__ == '__main__':
    _test()

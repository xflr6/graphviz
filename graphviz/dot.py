# dot.py - create dot code

"""Assemble DOT source code objects."""

import re
from itertools import imap

import files

__all__ = ['Digraph', 'Subgraph']


ID = re.compile(r'([a-zA-Z_]\w*|-?\d+)$')


def quote(key, valid_id=ID.match):
    """Return DOT identifier from key, quote if needed."""
    if not valid_id(key):
        return '"%s"' % key.replace('"', '\"')
    return key


def attributes(label=None, kwargs=None, attributes=None, raw=None):
    """Return assembled DOT attributes string."""
    if label is None:
        result = []
    else:
        result = ['label=%s' % quote(label)]
    if kwargs:
        result.extend(imap('%s=%s'.__mod__, kwargs.iteritems()))
    if attributes:
        if hasattr(attributes, 'iteritems'):
            attributes = attributes.iteritems()
        result.extend(imap('%s=%s'.__mod__, attributes))
    if raw:
        result.append(raw)
    return ' [%s]' % ' '.join(result) if result else ''


class Dot(files.File):
    """Assemble, save, and compile DOT source code, open result in viewer."""

    _comment = '// %r'
    _tail = '}'
    _filename = '%s.gv'

    quote = staticmethod(quote)
    attributes = staticmethod(attributes)

    def __init__(self, comment=None, key=None, filename=None, directory=None,
            graph_attr=None, node_attr=None, edge_attr=None, body=None):

        self.comment = comment
        self.key = key
        if filename is None:
            filename = self._filename % (key if key else 'Graph')
        self.filename =  filename
        self.directory = directory
        self._saved = False

        self.graph_attr = {} if graph_attr is None else dict(graph_attr)
        self.node_attr = {} if node_attr is None else dict(node_attr)
        self.edge_attr = {} if edge_attr is None else dict(edge_attr)

        self.body = [] if body is None else body

    def __iter__(self):
        yield self._comment % self.comment
        yield self._head % (self.quote(self.key) + ' ' if self.key else '')
        for kw in ('graph', 'node', 'edge'):
            attr = getattr(self, '%s_attr' % kw)
            if attr:
                yield '%s%s' % (kw, self.attributes(None, attr))
        for line in self.body:
            yield line
        yield self._tail

    def lines(self):
        return list(self)

    def __str__(self):
        return '\n'.join(self)

    source = property(__str__)

    def append(self, line):
        """Add line to the source."""
        self.body.append(line)

    def extend(self, lines):
        """Add lines to the source."""
        self.body.extend(lines)

    def node(self, key, label=None, _attributes=None, **kwargs):
        """Create a node."""
        key = self.quote(key)
        attributes = self.attributes(label, kwargs, _attributes)
        self.body.append('\t%s%s' % (key, attributes))

    def edge(self, parent_key, child_key, label=None, _attributes=None, **kwargs):
        """Create an edge."""
        parent_key = self.quote(parent_key)
        child_key = self.quote(child_key)
        attributes = self.attributes(label, kwargs, _attributes)
        self.body.append('\t\t%s -> %s%s' % (parent_key, child_key, attributes))

    def edges(self, parent_child):
        """Create a bunch of edges."""
        quote = self.quote
        self.body.extend('\t\t%s -> %s' % (quote(p), quote(c))
            for p, c in parent_child)


class Digraph(Dot):
    """Directed graph source code in the DOT language."""

    _head = 'digraph %s{'


class Subgraph(Dot):
    """Subgraph source code in the DOT language."""

    _head = 'subgraph %s{'

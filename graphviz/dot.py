# dot.py - create dot code

"""Assemble DOT source code objects.

>>> dot = Graph(comment=u'M\xf8nti Pyth\xf8n lk den H\xf8lie Grailen')

>>> dot.node(u'M\xf8\xf8se')
>>> dot.node('trained_by', u'trained by')
>>> dot.node('tutte', u'TUTTE HERMSGERVORDENBROTBORDA')

>>> dot.edge(u'M\xf8\xf8se', 'trained_by')
>>> dot.edge('trained_by', 'tutte')

>>> dot.node_attr['shape'] = 'rectangle'

>>> print(dot.source.replace(u'\xf8', '0'))  #doctest: +NORMALIZE_WHITESPACE
// M0nti Pyth0n lk den H0lie Grailen
graph {
    node [shape=rectangle]
        "M00se"
        trained_by [label="trained by"]
        tutte [label="TUTTE HERMSGERVORDENBROTBORDA"]
            "M00se" -- trained_by
            trained_by -- tutte
}

>>> dot.render('test-output/m00se.gv', view=True)
'test-output/m00se.gv.pdf'
"""

from . import lang, files

__all__ = ['Graph', 'Digraph', 'Subgraph']


class Dot(files.File):
    """Assemble, save, and render DOT source code, open result in viewer."""

    _comment = '// %s'
    _node = '\t%s%s'
    _tail = '}'

    quote = staticmethod(lang.quote)
    attributes = staticmethod(lang.attributes)

    def __init__(self, name=None, comment=None,
            filename=None, directory=None,
            format=None, engine=None, encoding=None,
            graph_attr=None, node_attr=None, edge_attr=None, body=None):

        self.name = name
        self.comment = comment

        super(Dot, self).__init__(filename, directory, format, engine, encoding)

        self.graph_attr = {} if graph_attr is None else dict(graph_attr)
        self.node_attr = {} if node_attr is None else dict(node_attr)
        self.edge_attr = {} if edge_attr is None else dict(edge_attr)

        self.body = [] if body is None else list(body)

    def __iter__(self):
        """Yield the DOT source code line by line."""
        yield self._comment % self.comment
        yield self._head % (self.quote(self.name) + ' ' if self.name else '')
        for kw in ('graph', 'node', 'edge'):
            attr = getattr(self, '%s_attr' % kw)
            if attr:
                yield '\t%s%s' % (kw, self.attributes(None, attr))
        if self.graph_attr or self.node_attr or self.edge_attr:
            for line in self.body:
                yield '\t' + line
        else:
            for line in self.body:
                yield line
        yield self._tail

    def __str__(self):
        return '\n'.join(self)

    source = property(__str__)

    def append(self, line):
        """Add line to the source."""
        self.body.append(line)

    def extend(self, lines):
        """Add lines to the source."""
        self.body.extend(lines)

    def node(self, name, label=None, _attributes=None, **kwargs):
        """Create a node."""
        name = self.quote(name)
        attributes = self.attributes(label, kwargs, _attributes)
        self.append(self._node % (name, attributes))

    def edge(self, tail_name, head_name, label=None, _attributes=None, **kwargs):
        """Create an edge."""
        tail_name = self.quote(tail_name)
        head_name = self.quote(head_name)
        attributes = self.attributes(label, kwargs, _attributes)
        edge = self._edge % (tail_name, head_name, attributes)
        self.append(edge)

    def edges(self, tail_head_iter):
        """Create a bunch of edges."""
        edge = self._edge_plain
        quote = self.quote
        self.extend(edge % (quote(t), quote(h))
            for t, h in tail_head_iter)


class Graph(Dot):
    """Graph source code in the DOT language."""

    _head = 'graph %s{'
    _edge = '\t\t%s -- %s%s'
    _edge_plain = '\t\t%s -- %s'


class Digraph(Dot):
    """Directed graph source code in the DOT language."""

    _head = 'digraph %s{'
    _edge = '\t\t%s -> %s%s'
    _edge_plain = '\t\t%s -> %s'


class Subgraph(Digraph):
    """Directed subgraph source code in the DOT language."""

    _head = 'subgraph %s{'

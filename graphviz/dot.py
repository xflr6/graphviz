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

__all__ = ['Graph', 'Digraph']


class Dot(files.File):
    """Assemble, save, and render DOT source code, open result in viewer."""

    _comment = '// %s'
    _subgraph = 'subgraph %s{'
    _node = '\t%s%s'
    _tail = '}'

    quote = staticmethod(lang.quote)
    quote_edge = staticmethod(lang.quote_edge)
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

    def __iter__(self, subgraph=False):
        """Yield the DOT source code line by line."""
        if self.comment:
            yield self._comment % self.comment

        head = self._subgraph if subgraph else self._head
        yield head % (self.quote(self.name) + ' ' if self.name else '')

        styled = False
        for kw in ('graph', 'node', 'edge'):
            attr = getattr(self, '%s_attr' % kw)
            if attr:
                styled = True
                yield '\t%s%s' % (kw, self.attributes(None, attr))

        indent = '\t' * styled
        for line in self.body:
            yield indent + line

        yield self._tail

    def __str__(self):
        return '\n'.join(self)

    source = property(__str__)

    def node(self, name, label=None, _attributes=None, **kwargs):
        """Create a node."""
        name = self.quote(name)
        attributes = self.attributes(label, kwargs, _attributes)
        self.body.append(self._node % (name, attributes))

    def edge(self, tail_name, head_name, label=None, _attributes=None, **kwargs):
        """Create an edge."""
        tail_name = self.quote_edge(tail_name)
        head_name = self.quote_edge(head_name)
        attributes = self.attributes(label, kwargs, _attributes)
        edge = self._edge % (tail_name, head_name, attributes)
        self.body.append(edge)

    def edges(self, tail_head_iter):
        """Create a bunch of edges."""
        edge = self._edge_plain
        quote = self.quote_edge
        self.body.extend(edge % (quote(t), quote(h))
            for t, h in tail_head_iter)

    def attr(self, kw, _attributes=None, **kwargs):
        """Add a graph/node/edge attribute statement."""
        if kw.lower() not in {'graph', 'node', 'edge'}:
            raise ValueError('attr statement must target graph, node, or edge: '
                '%r' % kw)
        if _attributes or kwargs:
            line = '\t%s%s' % (kw, self.attributes(None, kwargs, _attributes))
            self.body.append(line)

    def subgraph(self, graph):
        """Add the current content of a graph as subgraph."""
        if not isinstance(graph, self.__class__):
            raise ValueError('%r cannot add subgraphs of different kind: %r '
                % (self, graph))
        lines = ['\t' + line for line in graph.__iter__(subgraph=True)]
        self.body.extend(lines)


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

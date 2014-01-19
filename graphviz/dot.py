# dot.py - create dot code

"""Assemble DOT source code objects."""

import lang
import files

__all__ = ['Digraph', 'Subgraph']


class Dot(files.File):
    """Assemble, save, and compile DOT source code, open result in viewer."""

    _comment = '// %s'
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
        yield self._comment % self.comment
        yield self._head % (self.quote(self.name) + ' ' if self.name else '')
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

    def node(self, name, label=None, _attributes=None, **kwargs):
        """Create a node."""
        name = self.quote(name)
        attributes = self.attributes(label, kwargs, _attributes)
        self.body.append('\t%s%s' % (name, attributes))

    def edge(self, tail_name, head_name, label=None, _attributes=None, **kwargs):
        """Create an edge."""
        tail_name = self.quote(tail_name)
        head_name = self.quote(head_name)
        attributes = self.attributes(label, kwargs, _attributes)
        self.body.append('\t\t%s -> %s%s' % (tail_name, head_name, attributes))

    def edges(self, tail_head_iter):
        """Create a bunch of edges."""
        quote = self.quote
        self.body.extend('\t\t%s -> %s' % (quote(t), quote(h))
            for t, h in tail_head_iter)


class Digraph(Dot):
    """Directed graph source code in the DOT language."""

    _head = 'digraph %s{'


class Subgraph(Dot):
    """Subgraph source code in the DOT language."""

    _head = 'subgraph %s{'

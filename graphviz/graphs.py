r"""Assemble DOT source code objects.

>>> import graphviz
>>> dot = graphviz.Graph(comment='M\xf8nti Pyth\xf8n ik den H\xf8lie Grailen')

>>> dot.node('M\xf8\xf8se')
>>> dot.node('trained_by', 'trained by')
>>> dot.node('tutte', 'TUTTE HERMSGERVORDENBROTBORDA')

>>> dot.edge('M\xf8\xf8se', 'trained_by')
>>> dot.edge('trained_by', 'tutte')

>>> dot.node_attr['shape'] = 'rectangle'

>>> print(dot.source.replace('\xf8', '0'))  #doctest: +NORMALIZE_WHITESPACE
// M0nti Pyth0n ik den H0lie Grailen
graph {
    node [shape=rectangle]
    "M00se"
    trained_by [label="trained by"]
    tutte [label="TUTTE HERMSGERVORDENBROTBORDA"]
    "M00se" -- trained_by
    trained_by -- tutte
}

>>> dot.view('test-output/m00se.gv')  # doctest: +SKIP
'test-output/m00se.gv.pdf'
"""

import typing

from .encoding import DEFAULT_ENCODING
from . import dot
from . import jupyter_integration
from . import piping
from . import rendering
from . import unflattening

__all__ = ['Graph', 'Digraph']


class BaseGraph(dot.Dot,
                rendering.Render,
                jupyter_integration.JupyterSvgIntegration, piping.Pipe,
                unflattening.Unflatten):
    """Dot language creation and source code rendering."""

    def __init__(self, name: typing.Optional[str] = None,
                 comment: typing.Optional[str] = None,
                 filename=None, directory=None,
                 format: typing.Optional[str] = None,
                 engine: typing.Optional[str] = None,
                 encoding: typing.Optional[str] = DEFAULT_ENCODING,
                 graph_attr=None, node_attr=None, edge_attr=None,
                 body=None,
                 strict: bool = False, *,
                 renderer: typing.Optional[str] = None,
                 formatter: typing.Optional[str] = None) -> None:
        super().__init__(name=name, comment=comment,
                         graph_attr=graph_attr,
                         node_attr=node_attr, edge_attr=edge_attr,
                         body=body, strict=strict,
                         filename=filename, directory=directory,
                         encoding=encoding,
                         format=format, engine=engine,
                         renderer=renderer, formatter=formatter)

    @property
    def source(self) -> str:
        """The generated DOT source code as string."""
        return ''.join(self)


def graph_head(name: str) -> str:
    return f'graph {name}{{\n'


def digraph_head(name: str) -> str:
    return f'digraph {name}{{\n'


def graph_edge(*, tail: str, head: str, attr: str) -> str:
    return f'\t{tail} -- {head}{attr}\n'


def digraph_edge(*, tail: str, head: str, attr: str) -> str:
    return f'\t{tail} -> {head}{attr}\n'


class Graph(BaseGraph):
    """Graph source code in the DOT language.

    Args:
        name: Graph name used in the source code.
        comment: Comment added to the first line of the source.
        filename: Filename for saving the source
            (defaults to ``name`` + ``'.gv'``).
        directory: (Sub)directory for source saving and rendering.
        format: Rendering output format (``'pdf'``, ``'png'``, ...).
        engine: Layout command used (``'dot'``, ``'neato'``, ...).
        renderer: Output renderer used (``'cairo'``, ``'gd'``, ...).
        formatter: Output formatter used (``'cairo'``, ``'gd'``, ...).
        encoding: Encoding for saving the source.
        graph_attr: Mapping of ``(attribute, value)`` pairs for the graph.
        node_attr: Mapping of ``(attribute, value)`` pairs set for all nodes.
        edge_attr: Mapping of ``(attribute, value)`` pairs set for all edges.
        body: Iterable of verbatim lines to add to the graph ``body``.
        strict (bool): Rendering should merge multi-edges.

    Note:
        All parameters are `optional` and can be changed under their
        corresponding attribute name after instance creation.
    """

    _head = staticmethod(graph_head)

    _edge = staticmethod(graph_edge)

    @property
    def directed(self) -> bool:
        """``False``"""
        return False


class Digraph(BaseGraph):
    """Directed graph source code in the DOT language."""

    if Graph.__doc__ is not None:
        __doc__ += Graph.__doc__.partition('.')[2]

    _head = staticmethod(digraph_head)

    _edge = staticmethod(digraph_edge)

    @property
    def directed(self) -> bool:
        """``True``"""
        return True

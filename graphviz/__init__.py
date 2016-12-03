# graphviz - create dot, save, render, view

"""Assemble DOT source code and render it with Graphviz.

>>> dot = Digraph(comment='The Round Table')

>>> dot.node('A', 'King Arthur')
>>> dot.node('B', 'Sir Bedevere the Wise')
>>> dot.node('L', 'Sir Lancelot the Brave')

>>> dot.edges(['AB', 'AL'])

>>> dot.edge('B', 'L', constraint='false')

>>> print(dot)  #doctest: +NORMALIZE_WHITESPACE
// The Round Table
digraph {
    A [label="King Arthur"]
    B [label="Sir Bedevere the Wise"]
    L [label="Sir Lancelot the Brave"]
        A -> B
        A -> L
        B -> L [constraint=false]
}
"""

from .dot import Graph, Digraph
from .files import Source
from .backend import render, pipe, view, ENGINES, FORMATS

__all__ = [
    'Graph', 'Digraph',
    'Source',
    'render', 'pipe', 'view',
    'ENGINES', 'FORMATS',
]

__title__ = 'graphviz'
__version__ = '0.5.2'
__author__ = 'Sebastian Bank <sebastian.bank@uni-leipzig.de>'
__license__ = 'MIT, see LICENSE'
__copyright__ = 'Copyright (c) 2013-2016 Sebastian Bank'

#: Set of the supported layout commands used for rendering ('dot', 'neato', ...)
ENGINES = ENGINES

#: Set of the supported output formats for rendering ('pdf', 'png', ...)
FORMATS = FORMATS

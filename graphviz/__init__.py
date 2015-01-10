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

__title__ = 'graphviz'
__version__ = '0.4.3.dev0'
__author__ = 'Sebastian Bank <sebastian.bank@uni-leipzig.de>'
__license__ = 'MIT, see LICENSE'
__copyright__ = 'Copyright (c) 2013-2015 Sebastian Bank'

from .dot import Graph, Digraph

__all__ = ['Graph', 'Digraph']

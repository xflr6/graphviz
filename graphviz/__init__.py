# graphviz - create dot, save, compile, view

"""Assemble DOT source code and compile it with Graphviz.

>>> dot = Digraph(comment='The Round Table')

>>> dot.node('A', 'King Arthur')
>>> dot.node('B', 'Sir Bedevere the Wise')
>>> dot.node('L', 'Sir Lancelot the Brave')

>>> dot.edges(['AB', 'AL'])

>>> dot.edge('B', 'L', constraint='false')

>>> print dot  #doctest: +NORMALIZE_WHITESPACE
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
__version__ = '0.2.1'
__author__ = 'Sebastian Bank <sebastian.bank@uni-leipzig.de>'
__license__ = 'MIT, see LICENSE'
__copyright__ = 'Copyright (c) 2014 Sebastian Bank'

from dot import Graph, Digraph, Subgraph

__all__ = ['Graph', 'Digraph', 'Subgraph']

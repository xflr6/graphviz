#!/usr/bin/env python3

"""https://stackoverflow.com/questions/25734244/how-do-i-place-nodes-on-the-same-level-in-dot"""

import graphviz

d = graphviz.Digraph(filename='rank_same.gv')

with d.subgraph() as s:
    s.attr(rank='same')
    s.node('A')
    s.node('X')

d.node('C')

with d.subgraph() as s:
    s.attr(rank='same')
    s.node('B')
    s.node('D')
    s.node('Y')

d.edges(['AB', 'AC', 'CD', 'XY'])

d.view()

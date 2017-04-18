#!/usr/bin/env python
# cluster.py - http://www.graphviz.org/content/cluster

from graphviz import Digraph

g = Digraph('G', filename='cluster.gv')

c0 = Digraph('cluster_0')
c0.attr(style='filled')
c0.attr(color='lightgrey')
c0.node_attr.update(style='filled', color='white')
c0.edges([('a0', 'a1'), ('a1', 'a2'), ('a2', 'a3')])
c0.attr(label='process #1')

c1 = Digraph('cluster_1')
c1.node_attr.update(style='filled')
c1.edges([('b0', 'b1'), ('b1', 'b2'), ('b2', 'b3')])
c1.attr(label='process #2')
c1.attr(color='blue')

g.subgraph(c0)
g.subgraph(c1)

g.edge('start', 'a0')
g.edge('start', 'b0')
g.edge('a1', 'b3')
g.edge('b2', 'a3')
g.edge('a3', 'a0')
g.edge('a3', 'end')
g.edge('b3', 'end')

g.node('start', shape='Mdiamond')
g.node('end', shape='Msquare')

g.view()

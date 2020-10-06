#!/usr/bin/env python
# https://stackoverflow.com/questions/25734244/how-do-i-place-nodes-on-the-same-level-in-dot

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

# you can define the graph first and add the rank info afterwards like this.
# format is (id, display text)
d.node("1", "hello")
d.node("2", "world")
d.node("3", "there")
d.edges(["13", "32"])

with d.subgraph() as s:
    s.attr(rank='same')
    s.node("1")  # refer to the id
    s.node("3")

d.view()

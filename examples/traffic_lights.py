#!/usr/bin/env python
# traffic_lights.py - http://www.graphviz.org/content/traffic_lights

from graphviz import Digraph

t = Digraph('TrafficLights', filename='traffic_lights.gv', engine='neato')

t.attr('node', shape='box')
for i in (2, 1):
    t.node('gy%d' % i)
    t.node('yr%d' % i)
    t.node('rg%d' % i)

t.attr('node', shape='circle', fixedsize='true', width='0.9')
for i in (2, 1):
    t.node('green%d' % i)
    t.node('yellow%d' % i)
    t.node('red%d' % i)
    t.node('safe%d' % i)

for i, j in [(2, 1), (1, 2)]:
    t.edge('gy%d' % i, 'yellow%d' % i)
    t.edge('rg%d' % i, 'green%d' % i)
    t.edge('yr%d' % i, 'safe%d' % j)
    t.edge('yr%d' % i, 'red%d' % i)
    t.edge('safe%d' % i, 'rg%d' % i)
    t.edge('green%d' % i, 'gy%d' % i)
    t.edge('yellow%d' % i, 'yr%d' % i)
    t.edge('red%d' % i, 'rg%d' % i)

t.attr(overlap='false')
t.attr(label=r'PetriNet Model TrafficLights\n'
             r'Extracted from ConceptBase and layed out by Graphviz')
t.attr(fontsize='12')

t.view()

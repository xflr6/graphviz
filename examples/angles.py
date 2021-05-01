#!/usr/bin/env python3

"""http://www.graphviz.org/Gallery/gradient/angles.html"""

import graphviz

g = graphviz.Digraph('G', filename='angles.gv')
g.attr(bgcolor='blue')

with g.subgraph(name='cluster_1') as c:
    c.attr(fontcolor='white')
    c.attr('node', shape='circle', style='filled', fillcolor='white:black',
           gradientangle='360', label='n9:360', fontcolor='black')
    c.node('n9')
    for i, a in zip(range(8, 0, -1), range(360 - 45, -1, -45)):
        c.attr('node', gradientangle=f'{a:d}', label=f'n{i:d}:{a:d}')
        c.node(f'n{i:d}')
    c.attr(label='Linear Angle Variations (white to black gradient)')

with g.subgraph(name='cluster_2') as c:
    c.attr(fontcolor='white')
    c.attr('node', shape='circle', style='radial', fillcolor='white:black',
           gradientangle='360', label='n18:360', fontcolor='black')
    c.node('n18')
    for i, a in zip(range(17, 9, -1), range(360 - 45, -1, -45)):
        c.attr('node', gradientangle=f'{a:d}', label=f'n{i:d}:{a:d}')
        c.node(f'n{i:d}')
    c.attr(label='Radial Angle Variations (white to black gradient)')

g.edge('n5', 'n14')

g.view()

#!/usr/bin/env python3

"""http://www.graphviz.org/Gallery/gradient/g_c_n.html"""

import graphviz

g = graphviz.Graph('G', filename='g_c_n.gv')
g.attr(bgcolor='purple:pink', label='agraph', fontcolor='white')

with g.subgraph(name='cluster1') as c:
    c.attr(fillcolor='blue:cyan', label='acluster', fontcolor='white',
           style='filled', gradientangle='270')
    c.attr('node', shape='box', fillcolor='red:yellow',
           style='filled', gradientangle='90')
    c.node('anode')

g.view()

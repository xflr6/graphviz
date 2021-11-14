#!/usr/bin/env python3

"""https://graphviz.org/docs/attr-types/color"""

import graphviz

g = graphviz.Graph(filename='colors.gv')

red, green, blue = 64, 224, 208
assert f'#{red:x}{green:x}{blue:x}' == '#40e0d0'

g.node('RGB: #40e0d0', style='filled', fillcolor='#40e0d0')

g.node('RGBA: #ff000042', style='filled', fillcolor='#ff000042')

g.node('HSV: 0.051 0.718 0.627', style='filled', fillcolor='0.051 0.718 0.627')

g.node('name: deeppink', style='filled', fillcolor='deeppink')

g.view()

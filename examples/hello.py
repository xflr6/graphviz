#!/usr/bin/env python3

"""https://graphviz.org/Gallery/directed/hello.html"""

import graphviz

g = graphviz.Digraph('G', filename='hello.gv')

g.edge('Hello', 'World')

g.view()

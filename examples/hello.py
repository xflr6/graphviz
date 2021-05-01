#!/usr/bin/env python3

"""http://www.graphviz.org/content/hello"""

import graphviz

g = graphviz.Digraph('G', filename='hello.gv')

g.edge('Hello', 'World')

g.view()

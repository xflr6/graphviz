#!/usr/bin/env python
# hello.py - http://www.graphviz.org/content/hello

from graphviz import Digraph

g = Digraph('G', filename='hello.gv')

g.edge('Hello', 'World')

g.view()

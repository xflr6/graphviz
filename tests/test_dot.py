# test_dot.py

import unittest

from graphviz.dot import Graph, Digraph


class TestDot(unittest.TestCase):

    def test_attr(self):
        with self.assertRaises(ValueError):
            Graph().attr('spam')

    def test_subgraph_invalid(self):
        with self.assertRaises(ValueError):
            Graph().subgraph(Digraph())

        with self.assertRaises(ValueError):
            Digraph().subgraph(Graph())

    def test_subgraph_recursive(self):  # guard against potential infinite loop
        dot = Graph()
        dot.subgraph(dot)
        self.assertEqual(dot.source, 'graph {\n\tsubgraph {\n\t}\n}')

    def test_subgraph(self):
        s1 = Graph()
        s1.node('A')
        s1.node('B')
        s1.node('C')
        s1.edge('A', 'B', constraint='false')
        s1.edges(['AC', 'BC'])

        s2 = Graph()
        s2.node('D')
        s2.node('E')
        s2.node('F')
        s2.edge('D', 'E', constraint='false')
        s2.edges(['DF', 'EF'])

        dot = Graph()
        dot.subgraph(s1)
        dot.subgraph(s2)
        dot.attr('edge', style='dashed')
        dot.edges(['AD', 'BE', 'CF'])

        self.assertEqual(dot.source, '''graph {
	subgraph {
		A
		B
		C
			A -- B [constraint=false]
			A -- C
			B -- C
	}
	subgraph {
		D
		E
		F
			D -- E [constraint=false]
			D -- F
			E -- F
	}
	edge [style=dashed]
		A -- D
		B -- E
		C -- F
}''')

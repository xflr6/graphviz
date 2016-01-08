# test_dot.py

import unittest2 as unittest

from graphviz.dot import Graph, Digraph


class TestDot(unittest.TestCase):

    def test_repr_svg(self):
        self.assertRegexpMatches(Graph('spam')._repr_svg_(),
            r'(?s)^<\?xml .+</svg>\s*$')

    def test_attr(self):
        with self.assertRaises(ValueError):
            Graph().attr('spam')

    def test_strict(self):
        self.assertEqual(Graph(strict=True).source, 'strict graph {\n}')
        self.assertEqual(Digraph(strict=True).source, 'strict digraph {\n}')

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


class TestHTML(unittest.TestCase):
    """http://www.graphviz.org/doc/info/shapes.html#html"""

    def test_label_html(self):
        dot = Digraph('structs', node_attr={'shape': 'plaintext'})
        dot.node('struct1', '''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
  <TR>
    <TD>left</TD>
    <TD PORT="f1">middle</TD>
    <TD PORT="f2">right</TD>
  </TR>
</TABLE>>''')
        dot.node('struct2', '''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
  <TR>
    <TD PORT="f0">one</TD>
    <TD>two</TD>
  </TR>
</TABLE>>''')
        dot.node('struct3', '''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
  <TR>
    <TD ROWSPAN="3">hello<BR/>world</TD>
    <TD COLSPAN="3">b</TD>
    <TD ROWSPAN="3">g</TD>
    <TD ROWSPAN="3">h</TD>
  </TR>
  <TR>
    <TD>c</TD>
    <TD PORT="here">d</TD>
    <TD>e</TD>
  </TR>
  <TR>
    <TD COLSPAN="3">f</TD>
  </TR>
</TABLE>>''')
        dot.edge('struct1:f1', 'struct2:f0')
        dot.edge('struct1:f2', 'struct3:here')
        self.assertEqual(dot.source, '''digraph structs {
	node [shape=plaintext]
		struct1 [label=<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
  <TR>
    <TD>left</TD>
    <TD PORT="f1">middle</TD>
    <TD PORT="f2">right</TD>
  </TR>
</TABLE>>]
		struct2 [label=<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
  <TR>
    <TD PORT="f0">one</TD>
    <TD>two</TD>
  </TR>
</TABLE>>]
		struct3 [label=<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
  <TR>
    <TD ROWSPAN="3">hello<BR/>world</TD>
    <TD COLSPAN="3">b</TD>
    <TD ROWSPAN="3">g</TD>
    <TD ROWSPAN="3">h</TD>
  </TR>
  <TR>
    <TD>c</TD>
    <TD PORT="here">d</TD>
    <TD>e</TD>
  </TR>
  <TR>
    <TD COLSPAN="3">f</TD>
  </TR>
</TABLE>>]
			struct1:f1 -> struct2:f0
			struct1:f2 -> struct3:here
}''')
        dot.render('test-output/html.gv')

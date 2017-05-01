# test_dot.py
# flake8: noqa

import re
import itertools

import pytest

from graphviz.dot import Graph, Digraph


def test_repr_svg(pattern=r'(?s)^<\?xml .+</svg>\s*$'):
    assert re.match(pattern, Graph('spam')._repr_svg_())


def test_iter_subgraph_strict():
    with pytest.raises(ValueError) as e:
        Graph().subgraph(Graph(strict=True))
    e.match(r'strict')


def test_iter_strict():
    assert Graph(strict=True).source == 'strict graph {\n}'
    assert Digraph(strict=True).source == 'strict digraph {\n}'


def test_attr_invalid_kw():
    with pytest.raises(ValueError) as e:
        Graph().attr('spam')
    e.match(r'attr')


def test_attr_kw_none():
    dot = Graph()
    dot.attr(spam='eggs')
    assert dot.source == 'graph {\n\tspam=eggs\n}'


def test_subgraph_graph_none():
    dot = Graph()
    with dot.subgraph(name='name', comment='comment'):
        pass
    assert dot.source == 'graph {\n\t// comment\n\tsubgraph name {\n\t}\n}'


def test_subgraph_graph_notsole():
    with pytest.raises(ValueError) as e:
        Graph().subgraph(Graph(), name='spam')
    e.match(r'sole')


def test_subgraph_mixed():
    for cls1, cls2 in itertools.permutations([Graph, Digraph], 2):
        with pytest.raises(ValueError) as e:
            cls1().subgraph(cls2())
        e.match(r'kind')


def test_subgraph_reflexive():  # guard against potential infinite loop
    dot = Graph()
    dot.subgraph(dot)
    assert dot.source == 'graph {\n\t{\n\t}\n}'


def test_subgraph():
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

    assert dot.source == '''graph {
	{
		A
		B
		C
			A -- B [constraint=false]
			A -- C
			B -- C
	}
	{
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
}'''


def test_label_html():
    """http://www.graphviz.org/doc/info/shapes.html#html"""
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
    assert dot.source == '''digraph structs {
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
}'''
    dot.render('test-output/html.gv')

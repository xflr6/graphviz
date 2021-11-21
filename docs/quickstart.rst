Basic usage
-----------

The :doc:`graphviz <api>` module provides two classes: :class:`.Graph` and
:class:`.Digraph`. They create graph descriptions in the DOT_ language for
undirected and directed graphs respectively.
They have the same :doc:`API <api>`.

Create a graph by instantiating a new :class:`.Graph` or
:class:`.Digraph` object:

.. doctest::

    >>> import graphviz

    >>> dot = graphviz.Digraph('round-table', comment='The Round Table', directory='doctest-output')  # doctest: +NO_EXE

    >>> dot  # doctest: +ELLIPSIS
    <graphviz.graphs.Digraph object at 0x...>

Their constructors allow to set the graph's :attr:`~.Graph.name`, the
:attr:`~.Graph.filename` for the DOT source and the rendered graph, a
:attr:`~.Graph.comment` for the first source code line, etc.

Add nodes and edges to the graph object using its :meth:`~.Graph.node` and
:meth:`~.Graph.edge`- or :meth:`~.Graph.edges`-methods:

.. doctest::

    >>> dot.node('A', 'King Arthur')  # doctest: +NO_EXE
    >>> dot.node('B', 'Sir Bedevere the Wise')
    >>> dot.node('L', 'Sir Lancelot the Brave')

    >>> dot.edges(['AB', 'AL'])
    >>> dot.edge('B', 'L', constraint='false')

The :meth:`~.Graph.node`-method takes a ``name`` identifier as first argument
and an optional ``label``. The :meth:`~.Graph.edge`-method takes the names of
start node and end node, while :meth:`~.Graph.edges` takes an iterable of
name pairs. Keyword arguments are turned into (node and edge) attributes (see
`Graphviz docs <DOT attrs_>`_ on available attributes).

Check the generated source code:

.. doctest::

    >>> print(dot.source)  # doctest: +NORMALIZE_WHITESPACE  +NO_EXE
    // The Round Table
    digraph "round-table" {
        A [label="King Arthur"]
        B [label="Sir Bedevere the Wise"]
        L [label="Sir Lancelot the Brave"]
        A -> B
        A -> L
        B -> L [constraint=false]
    }

Use the :meth:`~.Graph.render`-method to save the source code and render it with the
default layout program
(``dot``, see below for using `other layout commands <engines>`_). 

.. doctest::

    >>> doctest_mark_exe()

    >>> dot.render().replace('\\', '/')
    'doctest-output/round-table.gv.pdf'

Passing ``view=True`` will automatically open the resulting (PDF, PNG, SVG,
etc.) file with your system's default viewer application for the file type.

.. doctest::

    >>> doctest_mark_exe()

    >>> dot.render(view=True)  # doctest: +SKIP
    'doctest-output/round-table.gv.pdf'

.. image:: _static/round-table.svg
    :align: center


.. include:: _links.rst

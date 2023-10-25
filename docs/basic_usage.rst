Basic usage
-----------

The :doc:`graphviz <api>` package provides two main classes: :class:`graphviz.Graph`
and :class:`graphviz.Digraph`. They create graph descriptions in the DOT_ language for
undirected and directed graphs respectively.
They have the same :doc:`API <api>`.

.. hint::

    :class:`.Graph` and :class:`.Digraph` produce different DOT syntax
    and have different values for :attr:`~.Graph.directed`.

Create a graph by instantiating a new :class:`.Graph` or
:class:`.Digraph` object:

.. doctest::

    >>> import graphviz

    >>> dot = graphviz.Digraph('round-table', comment='The Round Table')  # doctest: +NO_EXE

    >>> dot  # doctest: +ELLIPSIS
    <graphviz.graphs.Digraph object at 0x...>

Their constructors allow to set the graph's :attr:`~.Graph.name` identifier,
the :attr:`~.Graph.filename` for the DOT source and the rendered graph,
an optional :attr:`~.Graph.comment` for the first source code line, etc.

Add nodes and edges to the graph object using its :meth:`~.Graph.node`
and :meth:`~.Graph.edge` or :meth:`~.Graph.edges` methods:

.. doctest::

    >>> dot.node('A', 'King Arthur')  # doctest: +NO_EXE
    >>> dot.node('B', 'Sir Bedevere the Wise')
    >>> dot.node('L', 'Sir Lancelot the Brave')

    >>> dot.edges(['AB', 'AL'])
    >>> dot.edge('B', 'L', constraint='false')

The :meth:`~.Graph.node` method takes a ``name`` identifier as first argument
and an optional ``label``.
The :meth:`~.Graph.edge` method takes the names of start node and end node,
while :meth:`~.Graph.edges` takes an iterable of name pairs.
Keyword arguments are turned into (node and edge) attributes
(see extensive `Graphviz docs on available attributes <DOT attrs_>`_).

Check the generated DOT source code:

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

Use the :meth:`~.Graph.render` method to save the DOT source code
and render it with the default ``dot`` `layout engine <DOT layouts_>`_
(see :ref:`below <engines>` for using other layout engines).

.. attention::
    Skip/ignore any ``doctest_mark_exe()`` lines in documentation code examples.

.. doctest::

    >>> doctest_mark_exe()  # skip this line

    >>> dot.render(directory='doctest-output').replace('\\', '/')
    'doctest-output/round-table.gv.pdf'

Passing ``view=True`` will automatically open the resulting (PDF, SVG, PNG,
etc.) file with your system's default viewer application
for the rendered file type.

.. doctest::

    >>> doctest_mark_exe()  # skip this line

    >>> dot.render(directory='doctest-output', view=True)  # doctest: +SKIP
    'doctest-output/round-table.gv.pdf'

.. image:: _static/round-table.svg
    :align: center


.. include:: _links.rst

.. attention::

    Backslash-escapes and strings of the form ``<...>``
    have a special meaning in the DOT_ language
    and are currently passed on as is by this library.
    If you need to render arbitrary strings literally (e.g. from user input),
    consider wrapping them with the :func:`graphviz.escape` function first.
    See the sections on :ref:`backslash-escapes`
    and :ref:`quoting-and-html-like-labels` below for details.

Quoting and HTML-like labels
----------------------------

The graph-building methods of :class:`.Graph` and :class:`.Digraph` objects
automatically take care of quoting (and escaping quotes)
`where needed <DOT_>`_ (whitespace, keywords, double quotes, etc.):

.. doctest::

    >>> import graphviz

    >>> q = graphviz.Digraph()  # doctest: +NO_EXE

    >>> q.edge('spam', 'eggs eggs')
    >>> q.edge('node', '"here\'s a quote"')

    >>> print(q.source)  # doctest: +NORMALIZE_WHITESPACE
    digraph {
        spam -> "eggs eggs"
        "node" -> "\"here's a quote\""
    }

If a string starts with ``'<'`` and ends with ``'>'``, it is passed on as is,
without quoting/escaping: The content between the angle brackets is treated by
the engine as special **HTML string** that can be used for
`HTML-like labels <DOT shapes_>`_:

.. doctest::

    >>> h = graphviz.Graph('html_table')  # doctest: +NO_EXE

    >>> h.node('tab', label='''<<TABLE>
    ...  <TR>
    ...    <TD>left</TD>
    ...    <TD>right</TD>
    ...  </TR>
    ... </TABLE>>''')

.. image:: _static/html_table.svg
    :align: center

For strings that should literally begin with ``'<'`` and end with ``'>'``, use
the :func:`.nohtml` function to disable the special meaning of angled
parenthesis and apply normal quoting/escaping (before ``0.8.2``, the only
workaround was to add leading or trailing space, e.g. ``label=' <>'``):

.. doctest::

    >>> d = graphviz.Digraph('diamond', format='svg')  # doctest: +NO_EXE

    >>> d.node('diamond', label=graphviz.nohtml('<>'))

    >>> print(d.source)  # doctest: +NORMALIZE_WHITESPACE
    digraph diamond {
        diamond [label="<>"]
    }

.. image:: _static/diamond.svg
    :align: center


.. include:: _links.rst

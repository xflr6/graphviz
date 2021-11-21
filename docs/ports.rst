Node ports & compass
--------------------

The :meth:`~.Graph.edge`- and :meth:`~.Graph.edges`-methods use the
colon-separated format ``node[:port[:compass]]`` for ``tail`` and ``head``
nodes. This allows to specify an optional node ``port`` plus an optional
``compass`` point the edge should aim at for the given tail or head node
(:ref:`example <btree.py>`).

As colons are used to indicate ``port`` and ``compass``, node names with
literal colon(s) (``:``) are not supported. Note that there is no such
restriction for the ``label`` argument, so you can work around by choosing a
colon-free ``name`` together with the wanted ``label``:

.. doctest::

    >>> import graphviz

    >>> cpp = graphviz.Digraph('C++')  # doctest: +NO_EXE

    >>> cpp.node('A', 'std::string')
    >>> cpp.node('B', '"spam"')

    >>> cpp.edge('A', 'B')

    >>> print(cpp.source)  # doctest: +NORMALIZE_WHITESPACE
    digraph "C++" {
        A [label="std::string"]
        B [label="\"spam\""]
        A -> B
    }

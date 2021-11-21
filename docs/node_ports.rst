Node ports & compass
--------------------

The :meth:`~.Graph.edge` and :meth:`~.Graph.edges` methods use the
colon-separated ``node[:port[:compass]]`` format
for ``tail`` and ``head`` nodes.
This allows to specify an optional node ``port``
plus an optional ``compass`` point the edge should aim at
for the given tail or head node (:ref:`example <btree.py>`).

.. caution::

    As colons are used to indicate ``port`` and ``compass`` for edges,
    node names containing one or more literal colons ``:``
    are currently not supported.
    `GH #54 <https://github.com/xflr6/graphviz/issues/53>`_

.. tip::

    There is no such restriction for the ``label`` argument,
    so you can work around by choosing a colon-free ``name``
    together with the wanted ``label`` as demonstrated below

.. doctest::

    >>> import graphviz  # doctest: +NO_EXE

    >>> cpp = graphviz.Digraph('C++')

    >>> cpp.node('A', 'std::string')
    >>> cpp.node('B', '"spam"')

    >>> cpp.edge('A', 'B')

    >>> print(cpp.source)  # doctest: +NORMALIZE_WHITESPACE
    digraph "C++" {
        A [label="std::string"]
        B [label="\"spam\""]
        A -> B
    }

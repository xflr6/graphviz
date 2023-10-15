Styling
-------

Use the ``graph_attr``, ``node_attr``, and ``edge_attr`` arguments
of the :class:`.Graph` and :class:`.Digraph` constructors to change
the default `attributes <DOT attrs_>`_ for your graph, nodes, and edges.

.. doctest::

    >>> import graphviz  # doctest: +NO_EXE

    >>> ps = graphviz.Digraph('pet-shop', node_attr={'shape': 'plaintext'})

    >>> ps.node('parrot')
    >>> ps.node('dead')
    >>> ps.edge('parrot', 'dead')

After creation, the :attr:`~.Graph.graph_attr`, :attr:`~.Graph.node_attr`, and
:attr:`~.Graph.edge_attr` attributes be edited on instances:

.. doctest::

    >>> ps.graph_attr['rankdir'] = 'LR'  # doctest: +NO_EXE
    >>> ps.edge_attr.update(arrowhead='vee', arrowsize='2')

    >>> print(ps.source)  # doctest: +NORMALIZE_WHITESPACE
    digraph "pet-shop" {
        graph [rankdir=LR]
        node [shape=plaintext]
        edge [arrowhead=vee arrowsize=2]
        parrot
        dead
        parrot -> dead
    }

.. image:: _static/pet-shop.svg
    :align: center


.. include:: _links.rst

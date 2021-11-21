Styling
-------

Use the :attr:`~.Graph.graph_attr`, :attr:`~.Graph.node_attr`, and
:attr:`~.Graph.edge_attr` arguments to change the default `appearance <DOT attrs_>`_
of your graph, nodes, and edges.

.. doctest::

    >>> import graphviz

    >>> ps = graphviz.Digraph('pet-shop', node_attr={'shape': 'plaintext'})  # doctest: +NO_EXE

    >>> ps.node('parrot')
    >>> ps.node('dead')
    >>> ps.edge('parrot', 'dead')

After creation, they can be edited on the graph object:

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

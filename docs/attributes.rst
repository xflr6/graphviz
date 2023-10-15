Attributes
----------

To directly add DOT_ ``att_stmt`` attribute statements,
call the :meth:`~.Graph.attr` method
of the :class:`.Graph` or :class:`.Digraph` instance
with the wanted target as first argument and the attributes as keyword args.

.. hint::

    Attribute statements affect all **later** graphs, nodes, or edges
    within the same (sub-)graph.

.. doctest::

    >>> import graphviz

    >>> ni = graphviz.Graph('ni')  # doctest: +NO_EXE

    >>> ni.attr('node', shape='rarrow')
    >>> ni.node('1', 'Ni!')
    >>> ni.node('2', 'Ni!')

    >>> ni.node('3', 'Ni!', shape='egg')

    >>> ni.attr('node', shape='star')
    >>> ni.node('4', 'Ni!')
    >>> ni.node('5', 'Ni!')

If you omit the first :meth:`~.Graph.attr` argument, the method can be used
to set arbitrary attributes as key-value pairs targeting
the current (sub-)graph
(e.g. for ``rankdir``, ``label``,
or setting ``rank='same'`` within a subgraph context,
:ref:`example <rank_same.py>`):

.. doctest::

    >>> ni.attr(rankdir='LR')  # doctest: +NO_EXE

    >>> ni.edges(['12', '23', '34', '45'])

    >>> print(ni.source)  # doctest: +NORMALIZE_WHITESPACE
    graph ni {
        node [shape=rarrow]
        1 [label="Ni!"]
        2 [label="Ni!"]
        3 [label="Ni!" shape=egg]
        node [shape=star]
        4 [label="Ni!"]
        5 [label="Ni!"]
        rankdir=LR
        1 -- 2
        2 -- 3
        3 -- 4
        4 -- 5
    }

.. image:: _static/ni.svg
    :align: center


.. include:: _links.rst

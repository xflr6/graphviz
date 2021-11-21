Attributes
----------

To directly add attritbute statements (affecting all following graph, node, or
edge items within the same (sub-)graph), use the :meth:`~.Graph.attr`-method
with the target as first argument:

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

By omitting its first argument, you can use it to set arbitrary attributes as
key-value pairs targeting the current (sub-)graph (e.g. for ``rankdir``,
``label``, or setting ``rank='same'`` within a subgraph context,
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

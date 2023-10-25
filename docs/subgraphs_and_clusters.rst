Subgraphs & clusters
--------------------

:class:`.Graph` and :class:`.Digraph` objects have a
:meth:`~.Graph.subgraph` method for adding a subgraph to the instance.

There are two ways to use it: Either with a ready-made instance
of the same kind as the only argument (whose content is added as a subgraph)
or omitting the ``graph`` argument
(returning a context manager for defining the subgraph content more elegantly
within a ``with``-block).

First option, with ``graph`` as the only argument:

.. doctest::

    >>> import graphviz  # doctest: +NO_EXE

    >>> p = graphviz.Graph(name='parent')
    >>> p.edge('spam', 'eggs')

    >>> c = graphviz.Graph(name='child', node_attr={'shape': 'box'})
    >>> c.edge('foo', 'bar')

    >>> p.subgraph(c)

Second usage, with a ``with``-block (omitting the ``graph`` argument):

.. doctest::

    >>> p = graphviz.Graph('parent')  # doctest: +NO_EXE
    >>> p.edge('spam', 'eggs')

    >>> with p.subgraph(name='child', node_attr={'shape': 'box'}) as c:
    ...    c.edge('foo', 'bar')

Both produce the same result:

.. doctest::

    >>> print(p.source)  # doctest: +NORMALIZE_WHITESPACE +NO_EXE
    graph parent {
        spam -- eggs
        subgraph child {
            node [shape=box]
            foo -- bar
        }
    }

.. tip::

    If the ``name`` of a subgraph begins with ``'cluster'`` (all lowercase),
    the layout engine treats it as a special **cluster** subgraph
    (:ref:`example <cluster.py>` ).
    See the `Subgraphs and Clusters` section in `DOT language <DOT_>`_.

When :meth:`~.Graph.subgraph` is used as a context manager,
the new graph instance  is created with ``strict=None``
copying the **parent graph values** for ``directory``,
``engine``, ``format``, ``renderer``, ``formatter``,
and ``encoding``:

.. doctest::

    >>> doctest_mark_exe()  # skip this line

    >>> p = graphviz.Graph('parent', directory='doctest-output')

    >>> with p.subgraph(name='child') as c:
    ...    c.edge('bacon', 'eggs')
    ...    c.render().replace('\\', '/')
    'doctest-output/child.gv.pdf'

.. note::

    These copied attributes are only relevant for rendering the subgraph
    **independently** (i.e. as a stand-alone graph) from within the ``with``-block.


.. include:: _links.rst

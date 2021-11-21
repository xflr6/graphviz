Subgraphs & clusters
--------------------

:class:`.Graph` and :class:`.Digraph` objects have a
:meth:`~.Graph.subgraph`-method for adding a subgraph to an instance.

There are two ways to use it: Either with a ready-made graph object of the same
kind as the only argument (whose content is added as a subgraph) or omitting
the ``graph`` argument (returning a context manager for defining the subgraph
content more elegantly within a ``with``-block).

First usage option, with ``graph`` as the only argument:

.. doctest::

    >>> import graphviz

    >>> p = graphviz.Graph(name='parent')  # doctest: +NO_EXE
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

.. important::

    If the ``name`` of a subgraph begins with ``'cluster'`` (all lowercase) the
    layout engine will treat it as a special cluster subgraph
    (:ref:`example <cluster.py>` ). Also see the `Subgraphs and Clusters`
    section of `the DOT language documentation <DOT_>`_.

When :meth:`~.Graph.subgraph` is used as a context manager, the new graph
instance  is created with ``strict=None`` and the parent graph's values for
``directory``, ``engine``, ``format``,``renderer``, ``formatter``, and ``encoding``.
Note that these attributes are only relevant when rendering the subgraph independently
(i.e. as a stand-alone graph) from within the ``with``-block:

.. doctest::

    >>> doctest_mark_exe()

    >>> p = graphviz.Graph('parent', directory='doctest-output')

    >>> with p.subgraph(name='child') as c:
    ...    c.edge('bacon', 'eggs')
    ...    c.render().replace('\\', '/')
    'doctest-output/child.gv.pdf'


.. include:: _links.rst

.. _api:

API Reference
=============

.. note::
    The two main classes ``Graph`` and ``Digraph`` (for creating `undirected`
    vs. `directed` graphs) have exactly the same API.
    Their division reflects the fact that both graph types cannot be mixed.


Graph
-----

.. autoclass:: graphviz.Graph
    :members:
        source,
        node, edge, edges, attr, subgraph,
        format, engine, encoding,
        pipe, save, render, view


Digraph
-------

.. autoclass:: graphviz.Digraph
    :members:
        source,
        node, edge, edges, attr, subgraph,
        format, engine, encoding,
        pipe, save, render, view


Source
------

.. autoclass:: graphviz.Source
    :members:
        format, engine, encoding,
        pipe, save, render, view

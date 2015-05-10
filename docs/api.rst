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
    :members: node, edge, edges, attr, subgraph, source,
        format, engine,
        pipe, save, render, view
    :undoc-members:


Digraph
-------

.. autoclass:: graphviz.Digraph
    :members: node, edge, edges, attr, subgraph, source,
        format, engine,
        pipe, save, render, view
    :undoc-members:

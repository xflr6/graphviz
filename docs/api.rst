.. _api:

API Reference
=============

.. note::

    The two main classes :class:`.Graph` and :class:`.Digraph` (for creating
    `undirected` vs. `directed` graphs) have exactly the same API.
    Their division reflects the fact that both graph types cannot be mixed.


Graph
-----

.. autoclass:: graphviz.Graph
    :members:
        source,
        node, edge, edges, attr, subgraph,
        format, engine, encoding,
        copy, pipe, save, render, view


Digraph
-------

.. autoclass:: graphviz.Digraph
    :members:
        source,
        node, edge, edges, attr, subgraph,
        format, engine, encoding,
        copy, pipe, save, render, view


Source
------

.. autoclass:: graphviz.Source
    :members:
        format, engine, encoding,
        copy, pipe, save, render, view


Low-level functions
-------------------

The functions in this section are provided to work directly with existing
files and strings instead of using the object-oriented DOT creation methods
documented above.

.. autofunction:: graphviz.render
.. autofunction:: graphviz.pipe
.. autofunction:: graphviz.view


Other
-----

.. autodata:: graphviz.ENGINES
   :annotation:

.. autodata:: graphviz.FORMATS
   :annotation:

.. autodata:: graphviz.ExecutableNotFound
   :annotation:

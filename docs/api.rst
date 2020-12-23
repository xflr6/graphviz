.. _api:

API Reference
=============

.. autosummary::
    :nosignatures:

    ~graphviz.Graph
    ~graphviz.Digraph
    ~graphviz.Source
    graphviz.render
    graphviz.pipe
    graphviz.unflatten
    graphviz.view

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
        clear, copy, unflatten, pipe, save, render, view,
        directed


Digraph
-------

.. autoclass:: graphviz.Digraph
    :members:
        source,
        node, edge, edges, attr, subgraph,
        format, engine, encoding,
        clear, copy, unflatten, pipe, save, render, view,
        directed


Source
------

.. autoclass:: graphviz.Source
    :members:
        source,
        format, engine, encoding,
        copy, unflatten, pipe, save, render, view,
        from_file


Low-level functions
-------------------

The functions in this section are provided to work directly with existing
files and strings instead of using the object-oriented DOT creation methods
documented above.

.. autofunction:: graphviz.render
.. autofunction:: graphviz.pipe
.. autofunction:: graphviz.unflatten
.. autofunction:: graphviz.view


Other
-----

.. autodata:: graphviz.ExecutableNotFound
   :annotation:

.. autodata:: graphviz.RequiredArgumentError
   :annotation:

.. autofunction:: graphviz.version

.. autofunction:: graphviz.escape

.. autofunction:: graphviz.nohtml

Manually maintained whitelists (see https://graphviz.gitlab.io/_pages/pdf/dot.1.pdf,
http://www.graphviz.org/doc/info/output.html, and ``dot -T:`` output):

.. autodata:: graphviz.ENGINES
   :annotation:

.. autodata:: graphviz.FORMATS
   :annotation:

.. autodata:: graphviz.RENDERERS
   :annotation:

.. autodata:: graphviz.FORMATTERS
   :annotation:

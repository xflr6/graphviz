.. _manual:

User Guide
==========


Installation
------------

:mod:`graphviz` provides a simple pure-Python interface for the Graphviz_
graph-drawing software. It runs under Python 2.6, 2.7 and 3.3+. To install it
with pip_ run the following:

.. code:: bash

    $ pip install graphviz

For a system-wide install, this typically requires administrator access. For an
isolated install, you can run the same inside a virtualenv_ or a
:mod:`py3:venv` (Python 3.3+ only).

The only dependency is a working installation of Graphviz (`download page`_).

After installing Graphviz, make sure that its ``bin/`` subdirectory containing
the layout commands for rendering graph descriptions (``dot``, ``circo``,
``neato``, etc.) is on your systems' path: On the command-line, ``dot -V``
should print the version of your Graphiz installation.


Basic usage
-----------

The :mod:`graphviz` module provides two classes: :class:`.Graph` and
:class:`.Digraph`. They create graph descriptions in the DOT_ language for
undirected and directed graphs respectively. They have the same
:ref:`API <api>`.

Create a graph by instantiating a new :class:`.Graph` or
:class:`.Digraph` object:

.. code:: python

    >>> from graphviz import Digraph

    >>> dot = Digraph(comment='The Round Table')

    >>> dot  #doctest: +ELLIPSIS
    <graphviz.dot.Digraph object at 0x...>

Their constructors allow to set the graph's :attr:`~.Graph.name`, the
:attr:`~.Graph.filename` for the DOT source and the rendered graph, a
:attr:`~.Graph.comment` for the first source code line, etc.

Add nodes and edges to the graph object using its :meth:`~.Graph.node` and
:meth:`~.Graph.edge` or :meth:`~.Graph.edges` methods:

.. code:: python

    >>> dot.node('A', 'King Arthur')
    >>> dot.node('B', 'Sir Bedevere the Wise')
    >>> dot.node('L', 'Sir Lancelot the Brave')

    >>> dot.edges(['AB', 'AL'])
    >>> dot.edge('B', 'L', constraint='false')

The :meth:`~.Graph.node`-method takes a ``name`` identifier as first argument
and an optional ``label``. The :meth:`~.Graph.edge`-method takes the names of
start- and end-node, while :meth:`~.Graph.edges` takes iterable of name-pairs.
Keyword arguments are turned into (node and edge) attributes (see `Graphviz
docs <appearance_>`_).

Check the generated source code:

.. code:: python

    >>> print(dot.source)  # doctest: +NORMALIZE_WHITESPACE
    // The Round Table
    digraph {
        A [label="King Arthur"]
        B [label="Sir Bedevere the Wise"]
        L [label="Sir Lancelot the Brave"]
            A -> B
            A -> L
            B -> L [constraint=false]
    }

Use the :meth:`~.Graph.render`-method to save the source code and render it with the
default layout program (``dot``, see below for using `other layout commands
<Engines_>`_). 

.. code:: python

    >>> dot.render('test-output/round-table.gv', view=True)
    'test-output/round-table.gv.pdf'

.. image:: _static/round-table.svg
    :align: center

Passing ``view=True`` will automatically open the resulting (PDF, PNG, SVG,
etc.) file with your system's default viewer application for the file type.


Formats
-------

To use a different `output file format`_ than the default PDF, use the
:attr:`~.Graph.format` argument when creating your :class:`.Graph` or
:class:`.Digraph` object:

.. code:: python

    >>> from graphviz import Graph

    >>> g = Graph(format='png')

You can also change the :attr:`~.Graph.format` attribute on an existing graph
object:

.. code:: python

    >>> dot.format = 'svg'

    >>> dot.render()
    'test-output/round-table.gv.svg'


Piped output
------------

To directly access the results from the Graphviz rendering command (e.g.
``dot``) as binary data string from within Python instead of writing to a file,
use the :meth:`~.Graph.pipe`-method of your :class:`.Graph` or
:class:`.Digraph` object:

.. code:: python

    >>> h = Graph('hello', format='svg')

    >>> h.edge('Hello', 'World')

    >>> print(h.pipe().decode('utf-8'))  # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
    <?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <!DOCTYPE svg
    ...
    </svg>

Note that :meth:`~.Graph.pipe` returns the raw ``stdout`` from the rendering
command (``str`` on Python 2, ``bytes`` on Python 3): When piping into
plain-text formats like ``svg`` or ``plain``, you usually want to decode the
return value as shown above.

.. note::

    The output for :meth:`~.Graph.pipe` is buffered in memory, so do not use
    this method if the data size is large.


Jupyter notebooks
-----------------

:class:`.Graph` and :class:`.Digraph` objects have a
:meth:`~.Graph._repr_svg_`-method so they can be rendered and displayed
directly inside a `Jupyter notebook`_. For an example, check the
``examples/notebook.ipynb`` file in the
`source repository/distribution <notebook_>`_ (nbviewer_).


Styling
-------

Use the :attr:`~.Graph.graph_attr`, :attr:`~.Graph.node_attr`, and
:attr:`~.Graph.edge_attr` arguments to change the default appearance_ of your
graph, nodes, and edges.

.. code:: python

    >>> dot = Digraph(name='pet-shop', node_attr={'shape': 'plaintext'})

    >>> dot.node('parrot')
    >>> dot.node('dead')
    >>> dot.edge('parrot', 'dead')

After creation, they can be edited on the graph object:

.. code:: python

    >>> dot.graph_attr['rankdir'] = 'LR'
    >>> dot.edge_attr.update(arrowhead='vee', arrowsize='2')

    >>> print(dot.source)  # doctest: +NORMALIZE_WHITESPACE
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


Engines
-------

To use a different layout command than the default ``dot`` when rendering your
graph, use the :attr:`~.Graph.engine` argument when creating your graph. 

.. code:: python

    >>> g = Graph(engine='neato')

You can also change the :attr:`~.Graph.engine` attribute of an existing
instance:

.. code:: python

    >>> dot.engine = 'circo'


Using raw DOT
-------------

To render a ready-made DOT source code string (instead of assembling one with
the higher-level interface of :class:`.Graph` or :class:`.Digraph`), create a
:class:`.Source` object holding your DOT string:

.. code:: python

    >>> from graphviz import Source

    >>> src = Source('digraph "the holy hand grenade" { rankdir=LR; 1 -> 2 -> 3 -> lob }')

    >>> src  #doctest: +ELLIPSIS
    <graphviz.files.Source object at 0x...>

Use the :meth:`~.Source.render`-method to save and render it:

.. code:: python

    >>> src.render('test-output/holy-grenade.gv', view=True)
    'test-output/holy-grenade.gv.pdf'

.. image:: _static/holy-grenade.svg
    :align: center

Apart from the missing editing methods, :class:`.Source` objects are the same
as the higher-level graph objects (:meth:`~.Source.pipe`-method,
:attr:`~.Source.format`, :attr:`~.Source.engine`, Jupyter notebook repr, etc.),
see above.


.. _pip: http://pip.readthedocs.org
.. _virtualenv: http://virtualenv.pypa.io

.. _Graphviz: http://www.graphviz.org
.. _download page: http://www.graphviz.org/Download.php
.. _DOT: http://www.graphviz.org/doc/info/lang.html
.. _output file format: http://www.graphviz.org/doc/info/output.html
.. _appearance: http://www.graphviz.org/doc/info/attrs.html

.. _Jupyter notebook: http://jupyter.org
.. _notebook: http://github.com/xflr6/graphviz/blob/master/examples/notebook.ipynb
.. _nbviewer: http://nbviewer.jupyter.org/github/xflr6/graphviz/blob/master/examples/notebook.ipynb

Graphviz
========

|PyPI version| |License| |Supported Python| |Format| |Downloads|

This package facilitates the creation of graph descriptions in the DOT_ language
of the Graphviz_ graph drawing software from Python.

Create a graph object, assemble the graph by adding nodes and edges, and
retrieve its DOT source code string. Save the source code to a file and render
it with the Graphviz installation of your system. Use the ``view``
option/method to directly inspect the resulting (PDF, PNG, SVG, etc.) file with
its default application.


Installation
------------

This package runs under Python 2.7 and 3.3+, use pip_ to install:

.. code:: bash

    $ pip install graphviz

To render the generated DOT source code, you also need to install Graphviz
(`download page`_).

Make sure that the ``dot`` executable is on your systems' path.


Usage
-----

Create a graph object:

.. code:: python

    >>> from graphviz import Digraph

    >>> dot = Digraph(comment='The Round Table')

    >>> dot  #doctest: +ELLIPSIS
    <graphviz.dot.Digraph object at 0x...>

Add nodes and edges:

.. code:: python

    >>> dot.node('A', 'King Arthur')
    >>> dot.node('B', 'Sir Bedevere the Wise')
    >>> dot.node('L', 'Sir Lancelot the Brave')

    >>> dot.edges(['AB', 'AL'])
    >>> dot.edge('B', 'L', constraint='false')

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

Save and render the source code, optionally view the result:

.. code:: python

    >>> dot.render('test-output/round-table.gv', view=True)
    'test-output/round-table.gv.pdf'

.. image:: https://raw.github.com/xflr6/graphviz/master/docs/round-table.png
    :align: center


Formats
-------

To use a different `output file format`_ than the default PDF, set the
``format`` argument when creating your ``Graph`` or ``Digraph`` object:

.. code:: python

    >>> from graphviz import Graph

    >>> g = Graph(format='png')

You can also change the ``format`` attribute on an existing graph object:

.. code:: python

    >>> dot.format = 'svg'

    >>> dot.render()
    'test-output/round-table.gv.svg'


Styling
-------

Use the ``graph_attr``, ``node_attr``, and ``edge_attr`` arguments to change
the default `appearance`_ of your graph, nodes, and edges.

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

.. image:: https://raw.github.com/xflr6/graphviz/master/docs/pet-shop.png
    :align: center


Engines
-------

To use a different layout command than the default ``dot`` when rendering your
graph, set the ``engine`` argument on graph creation. 

.. code:: python

    >>> g = Graph(engine='neato')

You can also change the ``engine`` attribute of an existing instance:

.. code:: python

    >>> dot.engine = 'circo'


See also
--------

- pygraphviz_ |--| full-blown interface wrapping the Graphviz C library with SWIG
- graphviz-python_ |--| official Python bindings (documentation_)
- pydot_ |--| stable pure-Python approach, requires pyparsing


License
-------

This package is distributed under the `MIT license`_.

.. _pip: http://pip.readthedocs.org
.. _Graphviz:  http://www.graphviz.org
.. _download page: http://www.graphviz.org/Download.php
.. _DOT: http://www.graphviz.org/doc/info/lang.html
.. _output file format: http://www.graphviz.org/doc/info/output.html
.. _appearance: http://www.graphviz.org/doc/info/attrs.html

.. _pygraphviz: http://pypi.python.org/pypi/pygraphviz
.. _graphviz-python: https://pypi.python.org/pypi/graphviz-python
.. _documentation: http://www.graphviz.org/pdf/gv.3python.pdf
.. _pydot: http://pypi.python.org/pypi/pydot

.. _MIT license: http://opensource.org/licenses/MIT


.. |--| unicode:: U+2013


.. |PyPI version| image:: https://pypip.in/v/graphviz/badge.svg
    :target: https://pypi.python.org/pypi/graphviz
    :alt: Latest PyPI Version
.. |License| image:: https://pypip.in/license/graphviz/badge.svg
    :target: https://pypi.python.org/pypi/graphviz
    :alt: License
.. |Supported Python| image:: https://pypip.in/py_versions/graphviz/badge.svg
    :target: https://pypi.python.org/pypi/graphviz
    :alt: Supported Python Versions
.. |Format| image:: https://pypip.in/format/graphviz/badge.svg
    :target: https://pypi.python.org/pypi/graphviz
    :alt: Format
.. |Downloads| image:: https://pypip.in/d/graphviz/badge.svg
    :target: https://pypi.python.org/pypi/graphviz
    :alt: Downloads

Graphviz
========

|PyPI version| |License| |Downloads|

This package facilitates the creation of graph descriptions in
the `DOT <http://www.graphviz.org/doc/info/lang.html>`_ language
of the `Graphviz <http://www.graphviz.org>`_ graph drawing software
from Python. Create a graph object, assemble the graph by adding
nodes and edges, and retrieve its DOT source code string. Save the
source code to a file and compile it with the Graphviz installation
of your system.


Installation
------------

.. code:: bash

    $ pip install graphviz

To compile the generated DOT source code, you also need to install
Graphviz (`download page <http://www.graphviz.org/Download.php>`_).
Make sure that the ``dot`` executable is on your systems' path.


Usage
-----

Create a graph object:

.. code:: python

    >>> from graphviz import Digraph
	
    >>> dot = Digraph('The Round Table')

    >>> dot  #doctest: +ELLIPSIS
    <graphviz.dot.Digraph object at 0x...>

Add nodes and edges:

.. code:: python
	
    >>> dot.node('A', 'Kind Arthur')
    >>> dot.node('B', 'Sir Bedevere the Wise')
    >>> dot.node('L', 'Sir Lancelot the Brave')

    >>> dot.edges(['AB', 'AL'])
    >>> dot.edge('B', 'L', constraint='false')

Check results:

.. code:: python

    >>> print dot.source  # doctest: +NORMALIZE_WHITESPACE
    // 'The Round Table'
    digraph {
        A [label="Kind Arthur"]
        B [label="Sir Bedevere the Wise"]
        L [label="Sir Lancelot the Brave"]
                A -> B
                A -> L
                B -> L [constraint=false]
    }

Save the source code, optionally compile and view result:

.. code:: python

    >>> dot.save('round-table.gv', compile=True, view=True)

.. image:: https://raw.github.com/xflr6/graphviz/master/docs/round-table.gv.png


License
-------

This package is distributed under the `MIT license
<http://opensource.org/licenses/MIT>`_.

.. |PyPI version| image:: https://pypip.in/v/graphviz/badge.png
    :target: https://pypi.python.org/pypi/graphviz
    :alt: Latest PyPI Version
.. |License| image:: https://pypip.in/license/graphviz/badge.png
    :target: https://pypi.python.org/pypi/graphviz
    :alt: License
.. |Downloads| image:: https://pypip.in/d/graphviz/badge.png
    :target: https://pypi.python.org/pypi/graphviz
    :alt: Downloads

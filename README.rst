Graphviz
========

|PyPI version| |License| |Supported Python| |Format| |Docs|

This package facilitates the creation and rendering of graph descriptions in
the DOT_ language of the Graphviz_ graph drawing software (repo_) from Python.

Create a graph object, assemble the graph by adding nodes and edges, and
retrieve its DOT source code string. Save the source code to a file and render
it with the Graphviz installation of your system.

Use the ``view`` option/method to directly inspect the resulting (PDF, PNG,
SVG, etc.) file with its default application. Graphs can also be rendered
and displayed within `Jupyter notebooks`_ (a.k.a. `IPython notebooks`_,
example_).


Links
-----

- GitHub: http://github.com/xflr6/graphviz
- PyPI: http://pypi.python.org/pypi/graphviz
- Documentation: http://graphviz.readthedocs.io
- Changelog: http://graphviz.readthedocs.io/en/latest/changelog.html
- Issue Tracker: http://github.com/xflr6/graphviz/issues
- Download: http://pypi.python.org/pypi/graphviz#downloads


Installation
------------

This package runs under Python 2.7, and 3.3+, use pip_ to install:

.. code:: bash

    $ pip install graphviz

To render the generated DOT source code, you also need to install Graphviz
(`download page`_).

Make sure that the directory containing the ``dot`` executable is on your
systems' path.


Quickstart
----------

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


See also
--------

- pygraphviz_ |--| full-blown interface wrapping the Graphviz C library with SWIG
- graphviz-python_ |--| official Python bindings (documentation_)
- pydot_ |--| stable pure-Python approach, requires pyparsing


License
-------

This package is distributed under the `MIT license`_.


.. _pip: http://pip.readthedocs.io
.. _Graphviz:  http://www.graphviz.org
.. _repo: http://github.com/ellson/graphviz/
.. _download page: http://www.graphviz.org/Download.php
.. _DOT: http://www.graphviz.org/doc/info/lang.html
.. _Jupyter notebooks: http://jupyter.org
.. _IPython notebooks: http://ipython.org/notebook.html
.. _example: http://nbviewer.jupyter.org/github/xflr6/graphviz/blob/master/examples/notebook.ipynb

.. _pygraphviz: http://pypi.python.org/pypi/pygraphviz
.. _graphviz-python: http://pypi.python.org/pypi/graphviz-python
.. _documentation: http://www.graphviz.org/pdf/gv.3python.pdf
.. _pydot: http://pypi.python.org/pypi/pydot

.. _MIT license: http://opensource.org/licenses/MIT


.. |--| unicode:: U+2013


.. |PyPI version| image:: https://img.shields.io/pypi/v/graphviz.svg
    :target: https://pypi.python.org/pypi/graphviz
    :alt: Latest PyPI Version
.. |License| image:: https://img.shields.io/pypi/l/graphviz.svg
    :target: https://pypi.python.org/pypi/graphviz
    :alt: License
.. |Supported Python| image:: https://img.shields.io/pypi/pyversions/graphviz.svg
    :target: https://pypi.python.org/pypi/graphviz
    :alt: Supported Python Versions
.. |Format| image:: https://img.shields.io/pypi/format/graphviz.svg
    :target: https://pypi.python.org/pypi/graphviz
    :alt: Format
.. |Downloads| image:: https://img.shields.io/pypi/dm/graphviz.svg
    :target: https://pypi.python.org/pypi/graphviz
    :alt: Downloads
.. |Docs| image:: https://readthedocs.org/projects/graphviz/badge/?version=latest
    :target: https://graphviz.readthedocs.io/en/latest/
    :alt: Readthedocs
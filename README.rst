Graphviz
========

|PyPI version| |License| |Supported Python| |Format|

|Build| |Codecov| |Readthedocs-stable| |Readthedocs-latest|

This package facilitates the creation and rendering of graph descriptions in
the DOT_ language of the Graphviz_ graph drawing software (`upstream repo`_)
from Python.

Create a graph object, assemble the graph by adding nodes and edges, and
retrieve its DOT source code string. Save the source code to a file and render
it with the Graphviz installation of your system.

Use the ``view`` option/method to directly inspect the resulting (PDF, PNG,
SVG, etc.) file with its default application. Graphs can also be rendered
and displayed within `Jupyter notebooks`_ (formerly known as
`IPython notebooks`_,
`example <notebook_>`_, `nbviewer <notebook-nbviewer_>`_)
as well as the `Jupyter QtConsole`_.


Links
-----

- GitHub: https://github.com/xflr6/graphviz
- PyPI: https://pypi.org/project/graphviz/
- Documentation: https://graphviz.readthedocs.io
- Changelog: https://graphviz.readthedocs.io/en/latest/changelog.html
- Issue Tracker: https://github.com/xflr6/graphviz/issues
- Download: https://pypi.org/project/graphviz/#files


Installation
------------

This package runs under Python 3.6+, use pip_ to install:

.. code:: bash

    $ pip install graphviz

To render the generated DOT source code, you also need to install Graphviz_
(`download page <upstream-download_>`_,
`archived versions <upstream-archived_>`_,
`installation procedure for Windows <upstream-windows_>`_).

Make sure that the directory containing the ``dot`` executable is on your
systems' path.

Anaconda_: see the conda-forge_ package
`conda-forge/python-graphviz <conda-forge-python-graphviz_>`_
(`feedstock <conda-forge-python-graphviz-feedstock_>`_),
which should automatically ``conda install``
`conda-forge/graphviz <conda-forge-graphviz_>`_
(`feedstock <conda-forge-graphviz-feedstock_>`_) as dependency.


Quickstart
----------

Create a graph object:

.. code:: python

    >>> import graphviz
    >>> dot = graphviz.Digraph(comment='The Round Table')
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

    >>> dot.render('test-output/round-table.gv', view=True)  # doctest: +SKIP
    'test-output/round-table.gv.pdf'

.. image:: https://raw.github.com/xflr6/graphviz/master/docs/round-table.png
    :align: center

See also
--------

- pygraphviz_ |--| full-blown interface wrapping the Graphviz C library with SWIG
- graphviz-python_ |--| official Python bindings
  (`documentation <graphviz-python-docs_>`_)
- pydot_ |--| stable pure-Python approach, requires pyparsing


License
-------

This package is distributed under the `MIT license`_.


.. raw:: html

   <hr>


Development
-----------

Install in a venv_ in development mode (``pip install -e .[dev,test,docs]``):

.. code:: bash

    $ python -m venv .venv
    $ source .venv/bin/activate  # Windows: .venv\Script\activate.bat
    $ python -m pip install -r requirements.txt

**Tests**

- `Build workflow <https://github.com/xflr6/graphviz/actions/workflows/build.yaml>`_

**Run the tests** (in the current environment):

.. code:: bash

    $ run-tests.py

**Run the tests** with tox_ (in a virtualenv_):

.. code:: bash

    $ python -m tox

**Documentation**

- Read the Docs Project Home: https://readthedocs.org/projects/graphviz/
- stable: https://graphviz.readthedocs.io
- latest: https://graphviz.readthedocs.io/en/latest/

**Build the documentation** with sphinx_ and sphinx-rtd-theme_ (in the current environment):

.. code:: bash

    $ cd docs
    $ python -m sphinx . _build


.. raw:: html

   <hr>


Release process
^^^^^^^^^^^^^^^

Create ``release`` branch from main:

.. code:: bash

    $ git checkout -b release

Set release version (remove ``.dev0`` from ``$MAJOR.$MINOR[.$BUGFIX]``):

- ``docs/conf.py``
- ``graphviz/__init__.py``
- ``setup.py``

Document release:

- remove ``in development`` from ``CHANGES.txt``

Run the tests:

.. code:: bash

    $ python -m tox -r  # a.k.a --recreate

Commit to ``release`` branch and push to ``origin``:

.. code:: bash

    $ git commit -m "release $MAJOR.$MINOR[.$BUGFIX]"
    $ git push

- Check ``release`` `build workflow <https://github.com/xflr6/graphviz/actions?query=branch%3Arelease>`_

Build the release:

.. code:: bash

    $ python setup.py sdist bdist_wheel

Check the release:

- ``dist/graphviz-$MAJOR.$MINOR[.$BUGFIX].zip``
- ``dist/graphviz-$MAJOR.$MINOR[.$BUGFIX]-py3-none-any.whl``

If changes are needed (and go back to set version):

.. code:: bash

    $ git commit --ammend -m "$MESSAGE"

Publish the release with twine_:

.. code:: bash

    $ python -m twine upload dist/*

Switch to main branch and merge ``release``:

.. code:: bash

    $ git switch master
    $ git merge release

Create annotated release tag:

.. code:: bash

    $ git tag -a -m "$MAJOR.$MINOR[.$BUGFIX] release"

Bump version to ``$MAJOR.$MINOR.[.$BUGFIX].dev0``:

- ``docs/conf.py``
- ``graphviz/__init__.py``
- ``setup.py``

Document release:

- edit ``CHANGES.txt`` (add ``Version $MAJOR.$MINOR[.$BUGFIX] (in development)``)

Commit to main branch and push:

.. code:: bash

    $ git commit -m "bump version for development"
    $ git push --tags  # push all tags

- Check main branch `build workflow <https://github.com/xflr6/graphviz/actions?query=branch%3Amaster>`_
- Check `GitHub page <https://github.com/xflr6/graphviz>`_

Verify publication (install in default environment):

- Check `PyPI files <https://pypi.org/project/graphviz/#files>`_
- Check Read the Docs `builds <https://readthedocs.org/projects/graphviz/builds/>`_

.. code:: bash

    $ pip install -U graphviz


.. _Graphviz:  https://www.graphviz.org
.. _DOT: https://www.graphviz.org/doc/info/lang.html
.. _upstream repo: https://gitlab.com/graphviz/graphviz/
.. _upstream-download: https://www.graphviz.org/download/
.. _upstream-archived: https://www2.graphviz.org/Archive/stable/
.. _upstream-windows: https://forum.graphviz.org/t/new-simplified-installation-procedure-on-windows/224

.. _pip: https://pip.readthedocs.io

.. _Jupyter notebooks: https://jupyter.org
.. _IPython notebooks: https://ipython.org/notebook.html
.. _Jupyter QtConsole: https://qtconsole.readthedocs.io

.. _notebook: https://github.com/xflr6/graphviz/blob/master/examples/graphviz-notebook.ipynb
.. _notebook-nbviewer: https://nbviewer.jupyter.org/github/xflr6/graphviz/blob/master/examples/graphviz-notebook.ipynb

.. _Anaconda: https://docs.anaconda.com/anaconda/install/
.. _conda-forge: https://conda-forge.org
.. _conda-forge-python-graphviz: https://anaconda.org/conda-forge/python-graphviz
.. _conda-forge-python-graphviz-feedstock: https://github.com/conda-forge/python-graphviz-feedstock
.. _conda-forge-graphviz: https://anaconda.org/conda-forge/graphviz
.. _conda-forge-graphviz-feedstock: https://github.com/conda-forge/graphviz-feedstock
.. _pygraphviz: https://pypi.org/project/pygraphviz/
.. _graphviz-python: https://pypi.org/project/graphviz-python/
.. _graphviz-python-docs: https://www.graphviz.org/pdf/gv.3python.pdf
.. _pydot: https://pypi.org/project/pydot/

.. _MIT license: https://opensource.org/licenses/MIT

.. _venv: https://docs.python.org/3/library/venv.html#creating-virtual-environments
.. _tox: https://tox.wiki/en/latest/
.. _virtualenv: https://virtualenv.pypa.io
.. _sphinx: https://www.sphinx-doc.org
.. _sphinx-rtd-theme: https://sphinx-rtd-theme.readthedocs.io
.. _twine: https://twine.readthedocs.io/en/latest/


.. |--| unicode:: U+2013


.. |PyPI version| image:: https://img.shields.io/pypi/v/graphviz.svg
    :target: https://pypi.org/project/graphviz/
    :alt: Latest PyPI Version
.. |License| image:: https://img.shields.io/pypi/l/graphviz.svg
    :target: https://pypi.org/project/graphviz/
    :alt: License
.. |Supported Python| image:: https://img.shields.io/pypi/pyversions/graphviz.svg
    :target: https://pypi.org/project/graphviz/
    :alt: Supported Python Versions
.. |Format| image:: https://img.shields.io/pypi/format/graphviz.svg
    :target: https://pypi.org/project/graphviz/
    :alt: Format

.. |Build| image:: https://github.com/xflr6/graphviz/actions/workflows/build.yaml/badge.svg?branch=master
    :target: https://github.com/xflr6/graphviz/actions/workflows/build.yaml?query=branch%3Amaster
    :alt: Build
.. |Codecov| image:: https://codecov.io/gh/xflr6/graphviz/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/xflr6/graphviz
    :alt: Codecov
.. |Readthedocs-stable| image:: https://readthedocs.org/projects/graphviz/badge/?version=stable
    :target: https://graphviz.readthedocs.io/en/stable/?badge=stable
    :alt: Readthedocs stable
.. |Readthedocs-latest| image:: https://readthedocs.org/projects/graphviz/badge/?version=latest
    :target: https://graphviz.readthedocs.io/en/latest/?badge=latest
    :alt: Readthedocs latest
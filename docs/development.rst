.. _development:

Development
===========

|PyPI version| |License| |Supported Python| |Format|

- Changelog: https://graphviz.readthedocs.io/en/latest/changelog.html
- Issue Tracker: https://github.com/xflr6/graphviz/issues

Installation
------------

Install in a venv_ in development mode (includes all ``extras_require``):

.. code:: bash

    $ python -m venv .venv
    $ source .venv/bin/activate
    $ python -m pip install -r requirements.txt

.. admonition:: Platform: Windows

    ``C:\>.venv\Script\activate.bat``
    to replace ``source .venv/bin/activate``

.. hint::

    alteratively: ``pip install -e .[dev,test,docs]``
    (same as ``pip install -r requirements.txt``)

Tests
-----

|Build| |Codecov|

- GitHub Actions
  `Build workflow <https://github.com/xflr6/graphviz/actions/workflows/build.yaml>`_
  (Python 3.6 to 3.10, experimental: PyPy 3.8 to 3.8)
- Codecov
  `test coverage <https://app.codecov.io/gh/xflr6/graphviz>`_
  (`main branch <https://app.codecov.io/gh/xflr6/graphviz/branch/master>`_)

**Run the tests** (in the current environment):

.. code:: bash

    $ ./run-tests.py

Run **only tests** that are expected to work **without Graphviz** executables:

.. code:: bash

    $ ./run-tests.py --skip-exe

**Run the tests** with tox_ (**installing** into a virtualenv_ or many of them):

.. code:: bash

    $ python -m tox

Documentation
-------------

|Readthedocs-stable| |Readthedocs-latest|

- Read the Docs Project Home: https://readthedocs.org/projects/graphviz/
- stable: https://graphviz.readthedocs.io
- latest: https://graphviz.readthedocs.io/en/latest/

**Build the documentation** with sphinx_ and sphinx-rtd-theme_ (in the current environment):

.. code:: bash

    $ cd docs
    $ python -m sphinx . _build

Overview
--------

Use ``help()`` in the REPL to shows/structure methods and attributes in dependency order:

- Introduction: https://graphviz.readthedocs.io/en/latest/api.html#online-help-internal
- ``Graph``: https://github.com/xflr6/graphviz/blob/master/docs/api.rst#graph-1
- ``Digraph``: https://github.com/xflr6/graphviz/blob/master/docs/api.rst#digraph-1
- ``Source``: https://github.com/xflr6/graphviz/blob/master/docs/api.rst#source-1

.. tip::

    In the above, cooperative multiple inheritance classes reveal their
    (diamond) MRO structure and methods are shown in **method resolution order** (MRO),
    which should be an extension of their dependency relation...
    
    TLDR; you might find this presentation helps to follow the implementation.


.. _venv: https://docs.python.org/3/library/venv.html#creating-virtual-environments
.. _tox: https://tox.wiki/en/latest/
.. _virtualenv: https://virtualenv.pypa.io
.. _sphinx: https://www.sphinx-doc.org
.. _sphinx-rtd-theme: https://sphinx-rtd-theme.readthedocs.io


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

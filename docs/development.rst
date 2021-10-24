.. _development:

Development
===========

Installation
------------

Install in a venv_ in development mode:

.. code:: bash

    $ python -m venv .venv
    $ source .venv/bin/activate  # Windows: .venv\Script\activate.bat
    $ python -m pip install -r requirements.txt  # pip install -e .[dev,test,docs]

Tests
-----

- GitHub Actions **`Build workflow <https://github.com/xflr6/graphviz/actions/workflows/build.yaml>`_**
  (Python 3.6 to 3.10, experimental: PyPy 3.8 to 3.8)

**Run the tests** (in the current environment):

.. code:: bash

    $ ./run-tests.py

**Run the tests** with tox_ (in a virtualenv_):

.. code:: bash

    $ python -m tox

Documentation
-------------

- Read the Docs Project Home: https://readthedocs.org/projects/graphviz/
- stable: https://graphviz.readthedocs.io
- latest: https://graphviz.readthedocs.io/en/latest/

**Build the documentation** with sphinx_ and sphinx-rtd-theme_ (in the current environment):

.. code:: bash

    $ cd docs
    $ python -m sphinx . _build


.. _venv: https://docs.python.org/3/library/venv.html#creating-virtual-environments
.. _tox: https://tox.wiki/en/latest/
.. _virtualenv: https://virtualenv.pypa.io
.. _sphinx: https://www.sphinx-doc.org
.. _sphinx-rtd-theme: https://sphinx-rtd-theme.readthedocs.io

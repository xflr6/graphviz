.. _development:

Development
===========

|PyPI version| |License| |Supported Python| |Wheel| |Downloads|

- GitHub: https://github.com/xflr6/graphviz
- Changelog: https://graphviz.readthedocs.io/en/latest/changelog.html
- Issue Tracker: https://github.com/xflr6/graphviz/issues


Installation
------------

|Binder-HEAD|

Development environment **binder** : https://mybinder.org/v2/gh/xflr6/graphviz/HEAD

Local installation
^^^^^^^^^^^^^^^^^^

Install in a venv_ in development mode (includes all ``extras_require``):

.. code:: bash

    $ git clone https://github.com/xflr6/graphviz.git
    $ cd graphviz
    $ python -m venv .venv
    $ source .venv/bin/activate
    $ python -m pip install -r requirements.txt

.. admonition:: Platform: Windows

    ``.venv\Script\activate.bat``
    to replace ``source .venv/bin/activate``

.. hint::

    alternatively: ``pip install -e .[dev,test,docs]``
    (same as ``pip install -r requirements.txt``)


Tests
-----

|Build| |Codecov|

- GitHub Actions
  `Build workflow <https://github.com/xflr6/graphviz/actions/workflows/build.yaml>`_
  (Python 3.8 to 3.11, experimental: PyPy 3.8 to 3.9)
- Codecov
  `test coverage <https://app.codecov.io/gh/xflr6/graphviz>`_
  (`main branch <https://app.codecov.io/gh/xflr6/graphviz/branch/master>`_)

**Run the tests** (in the current environment):

.. code:: bash

    $ python run-tests.py

Run **only tests** that are expected to ``PASS`` or ``XFAIL``
**without Graphviz** executables:

.. code:: bash

    $ python run-tests.py --skip-exe

**Run the tests** with tox_ (**installing** into a virtualenv_ or many of them):

.. code:: bash

    $ python -m tox

**Run the static type checker**
(pytype_,
supported `platforms <pytpe_platforms_>`_
and `Python versions <pytype_python_versions_>`_):

.. code:: bash

    $ pip install pytype
    $ pytype

**Run the code linter** (flake8_):

.. code:: bash

    $ python lint-code.py


Documentation
-------------

|Readthedocs-stable| |Readthedocs-latest|

- Read the Docs Project Home: https://readthedocs.org/projects/graphviz/
- stable: https://graphviz.readthedocs.io
- latest: https://graphviz.readthedocs.io/en/latest/

**Build the documentation** with sphinx_ and sphinx-rtd-theme_ (in the current environment):

.. code:: bash

    $ python build-docs.py


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


.. include:: _links.rst


.. |PyPI version| image:: https://img.shields.io/pypi/v/graphviz.svg
    :target: https://pypi.org/project/graphviz/
    :alt: Latest PyPI Version
.. |License| image:: https://img.shields.io/pypi/l/graphviz.svg
    :target: https://github.com/xflr6/graphviz/blob/master/LICENSE.txt
    :alt: License
.. |Supported Python| image:: https://img.shields.io/pypi/pyversions/graphviz.svg
    :target: https://pypi.org/project/graphviz/
    :alt: Supported Python Versions
.. |Wheel| image:: https://img.shields.io/pypi/wheel/graphviz.svg
    :target: https://pypi.org/project/graphviz/
    :alt: Wheel format
.. |Downloads| image::  https://img.shields.io/pypi/dm/graphviz.svg
    :target: https://pypi.org/project/graphviz/#files
    :alt: Monthly downloads

.. |Build| image:: https://github.com/xflr6/graphviz/actions/workflows/build.yaml/badge.svg?branch=master
    :target: https://github.com/xflr6/graphviz/actions/workflows/build.yaml?query=branch%3Amaster
    :alt: Build
.. |Codecov| image:: https://codecov.io/gh/xflr6/graphviz/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/xflr6/graphviz
    :alt: Codecov
.. |Readthedocs-stable| image:: https://readthedocs.org/projects/graphviz/badge/?version=stable
    :target: https://graphviz.readthedocs.io/en/stable/
    :alt: Readthedocs (stable)
.. |Readthedocs-latest| image:: https://readthedocs.org/projects/graphviz/badge/?version=latest
    :target: https://graphviz.readthedocs.io/en/latest/
    :alt: Readthedocs (latest)

.. |Binder-HEAD| image:: https://img.shields.io/badge/launch-binder%20(HEAD)-E66581.svg?logo=data:image/png;base64,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
    :target: https://mybinder.org/v2/gh/xflr6/graphviz/HEAD
    :alt: Binder (HEAD)

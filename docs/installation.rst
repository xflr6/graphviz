Installation
------------

:doc:`graphviz <api>` provides a simple pure-Python interface for the Graphviz_
graph-drawing software. It runs under Python 3.8+. To install it with pip_, run
the following:

.. code:: bash

    $ pip install graphviz

For a system-wide install, this typically requires administrator access. For an
isolated install, you can run the same inside a :mod:`venv` or a virtualenv_.

The only dependency is a working installation of Graphviz_
(`download page <upstream-download_>`_,
`archived versions <upstream-archived_>`_,
`installation procedure for Windows <upstream-windows_>`_).

After installing Graphviz, make sure that its ``bin/`` subdirectory containing
the ``dot`` `layout command <DOT command_>`_ for rendering graph descriptions
is on your systems' ``PATH``
(sometimes done by the installer;
setting ``PATH``
on `Linux <set-path-linux_>`_,
`Mac <set-path-darwin_>`_,
and `Windows <set-path-windows_>`_):
On the command-line, ``dot -V`` should print the version of your Graphiz installation.

.. admonition:: Platform: Windows

    Windows users might want to check the status of known issues
    (gvedit.exe__, sfdp__, commands__) and consider trying an older archived
    version as a workaround (e.g. graphviz-2.38.msi__).

__ https://gitlab.com/graphviz/graphviz/-/issues/1816
__ https://gitlab.com/graphviz/graphviz/-/issues/1269
__ https://gitlab.com/graphviz/graphviz/-/issues/1753
__ https://www2.graphviz.org/Archive/stable/windows/graphviz-2.38.msi

.. admonition:: Platform: Anaconda

    See the downstream conda-forge_ distribution
    `conda-forge/python-graphviz <conda-forge-python-graphviz_>`_
    (`feedstock <conda-forge-python-graphviz-feedstock_>`_),
    which should automatically ``conda install``
    `conda-forge/graphviz <conda-forge-graphviz_>`_
    (`feedstock <conda-forge-graphviz-feedstock_>`_) as dependency.


.. include:: _links.rst

Release process
===============


Build
-----

Create ``release`` branch from main:

.. code:: bash

    $ git checkout -b release

Cleanup:

.. code:: bash

    $ git clean -f -d -x  # remove all untracked files and directories

Set release version (remove ``.dev0`` from ``$MAJOR.$MINOR[.$BUGFIX]``):

- ``docs/conf.py``
- ``graphviz/__init__.py``
- ``setup.py``

Update `help output <online-help-internal>`_ if needed.

Document release:

- remove ``in development`` from ``CHANGES.rst``
- bump stable ``$MAJOR.$MINOR[.$BUGFIX]`` tag of binder badge in ``README.rst``

Run the tests, run the linter, and build the docs:

.. code:: bash

    $ python -m tox -r -- -W error  # --recreate, raise error on warning
    $ python -m flake8 --disable-noqa
    $ cd docs
    $ python -m sphinx . _build
    $ cd ..
    $ git clean -f -d -x  # remove all untracked files and directories

Commit to ``release`` branch and push to ``origin``:

.. code:: bash

    $ git add *
    $ git commit -m "release $MAJOR.$MINOR[.$BUGFIX]"
    $ git push --set-upstream origin release

- Check GitHub Actions ``relase`` `Build workflow
  <https://github.com/xflr6/graphviz/actions?query=branch%3Arelease>`_
- Check Codecov ``release`` build `test coverage
  <https://app.codecov.io/gh/xflr6/graphviz/branch/release>`_

Build the release:

.. code:: bash

    $ python setup.py sdist bdist_wheel

Check the release:

- ``dist/graphviz-$MAJOR.$MINOR[.$BUGFIX].zip``
- ``dist/graphviz-$MAJOR.$MINOR[.$BUGFIX]-py3-none-any.whl``

If changes are needed (and go back to: **Cleanup**):

.. code:: bash

    $ git commit --amend --date=now


Publish
-------

Publish the release with twine_:

.. code:: bash

    $ python -m twine upload dist/*

Switch to main branch and merge ``release``:

.. code:: bash

    $ git switch master
    $ git merge --ff-only release

Create annotated release tag:

.. code:: bash

    $ git tag -a -m "$MAJOR.$MINOR[.$BUGFIX] release"

Bump version to ``$MAJOR.$MINOR.[.$BUGFIX].dev0``:

- ``docs/conf.py``
- ``graphviz/__init__.py``
- ``setup.py``

Document release:

- edit ``CHANGES.rst`` (add ``Version $MAJOR.$MINOR[.$BUGFIX] (in development)``)

Commit to main branch and push:

.. code:: bash

    $ git commit -m "bump version for development"
    $ git push --tags  # pushes all tags

- Check GitHub Actions `main branch Build workflow
  <https://github.com/xflr6/graphviz/actions?query=branch%3Amaster>`_
- Check GitHub `Main page <https://github.com/xflr6/graphviz>`_


Verify
------

Verify publication (install in default environment):

- Check `PyPI files <https://pypi.org/project/graphviz/#files>`_
- Check Read the Docs `builds <https://readthedocs.org/projects/graphviz/builds/>`_
- Check `stable release notes <https://graphviz.readthedocs.io/en/stable/changelog.html>`_
- Check `latest release notes <https://graphviz.readthedocs.io/en/latest/changelog.html>`_

.. code:: bash

    $ pip install -U graphviz
    $ python -c "import graphviz; print((graphviz.__version__, graphviz.version()))"

- Check downstream `conda-forge release <https://github.com/conda-forge/python-graphviz-feedstock>`_


.. flake8: https://flake8.pycqa.org/en/latest/
.. _twine: https://twine.readthedocs.io/en/latest/

Release process
===============


Build
-----

Update build dependencies:

.. code:: bash

    $ pip install -U setuptools wheel twine

Create ``release`` branch from main:

.. code:: bash

    $ git checkout -b release

**Cleanup** (remove all untracked files and directories):

.. code:: bash

    $ git clean -f -d -x

Update ``help()`` output:

.. code:: bash

    $ python update-help.py

Set **release version** (remove ``.dev0`` from ``$MAJOR.$MINOR[.$BUGFIX]`` version):

- ``docs/conf.py``
- ``graphviz/__init__.py``
- ``setup.py``

Document release:

- remove ``(in development)`` from ``CHANGES.rst`` header

Run the tests, lint the code, and build the documentation:

.. code:: bash

    $ python -m tox -r -- -W error  # --recreate, raise error on warning
    $ python lint-code.py --disable-noqa
    $ python build-docs.py -b doctest
    $ python build-docs.py
    $ git clean -f -d -x

Commit to ``release`` branch and push to ``origin``:

.. code:: bash

    $ git add *
    $ git commit -m "release $MAJOR.$MINOR[.$BUGFIX]"
    $ git push --set-upstream origin release

- Check GitHub Actions ``relase`` `Build workflow
  <https://github.com/xflr6/graphviz/actions?query=branch%3Arelease>`_
- Check Codecov ``release`` build `test coverage
  <https://app.codecov.io/gh/xflr6/graphviz/branch/release>`_

**Build** and check the release files:

.. code:: bash

    $ python setup.py sdist bdist_wheel
    $ python -m twine check --strict dist/*

- ``dist/graphviz-$MAJOR.$MINOR[.$BUGFIX].zip``
- ``dist/graphviz-$MAJOR.$MINOR[.$BUGFIX]-py3-none-any.whl``

If changes are needed (and go back to: **Cleanup** step):

.. code:: bash

    $ git commit --amend --date=now

Switch to main branch and merge ``release``:

.. code:: bash

    $ git switch master
    $ git merge --ff-only release

**Tag** with annotated release version tag:

.. code:: bash

    $ git tag -a -m "$MAJOR.$MINOR[.$BUGFIX] release"

Bump **post-release version** to ``$MAJOR.$MINOR.[.$BUGFIX].dev0``:

- ``docs/conf.py``
- ``graphviz/__init__.py``
- ``setup.py``

Document post-release:

- add new ``Version $MAJOR.$MINOR[.$BUGFIX] (in development)`` heading to ``CHANGES.rst``

Commit version bump to main branch:

.. code:: bash

    $ git commit -m "bump version for development"


Publish
-------

Publish the release with twine_:

.. code:: bash

    $ python -m twine upload dist/*

Push main branch and push all new tags:

.. code:: bash

    $ git push --tags

Update `stable <https://github.com/xflr6/graphviz/tree/stable>`_ branch to the latest release:

.. code:: bash

    $ git switch stable
    $ git merge --ff-only $MAJOR.$MINOR[.$BUGFIX]
    $ git push


Verify
------

Verify publication:

- Check `PyPI files <https://pypi.org/project/graphviz/#files>`_
- Check GitHub `Main page <https://github.com/xflr6/graphviz>`_
- Check GitHub Actions `main branch Build workflow
  <https://github.com/xflr6/graphviz/actions?query=branch%3Amaster>`_
- Check Read the Docs `builds <https://readthedocs.org/projects/graphviz/builds/>`_
- Check `latest release notes <https://graphviz.readthedocs.io/en/latest/changelog.html>`_
- Check `stable release notes <https://graphviz.readthedocs.io/en/stable/changelog.html>`_
- Check ``stable`` binder: https://mybinder.org/v2/gh/xflr6/graphviz/stable

Install in default environment:

.. code:: bash

    $ pip install -U graphviz
    $ python -c "import graphviz; print((graphviz.__version__, graphviz.version()))"

Downstream
----------

- Check downstream `conda-forge release <https://github.com/conda-forge/python-graphviz-feedstock>`_


.. include:: _links.rst

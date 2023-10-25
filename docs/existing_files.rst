Existing files
--------------

To directly render an existing DOT_ source file (e.g. created with other tools),
you can use the :func:`graphviz.render` function.

.. doctest::

    >>> doctest_mark_exe()  # skip this line

    >>> import pathlib
    >>> import graphviz

    >>> src = 'digraph "the holy hand grenade" { rankdir=LR; 1 -> 2 -> 3 -> lob }'
    >>> filepath = pathlib.Path('doctest-output/the-holy-hand-grenade.gv')
    >>> filepath.write_text(src, encoding='ascii')
    66

    >>> graphviz.render('dot', 'png', filepath).replace('\\', '/')
    'doctest-output/the-holy-hand-grenade.gv.png'

To directly display the rendered visualization of an existing DOT_ source file
inside a  Jupyter `notebook <Jupyter notebook_>`_
or `Qt Console <Jupyter Qt Console_>`_,
you can use :meth:`graphviz.Source.from_file` (alternative constructor):

.. image:: _static/qtconsole-source.png
    :align: center

Note that :meth:`~.Source.render` and :meth:`~.Source.view`
on :class:`.Source` instances returned by :meth:`graphviz.Source.from_file`
skip writing the loaded file back.
The same holds for :meth:`~.Source.save`.
The instances resolve default ``.save(skip_existing=None)``
to ``.save(skip_existing_run=True)``
to skip writing the read :attr:`~.Source.source` back into the same file
(specifically the same path that it was loaded from).
Call ``.save(skip_existing=False)`` if you want to re-write the loaded source.

.. admonition:: Historical note

    Before version ``0.18`` of this library,
    :meth:`.Source.save`, :meth:`.Source.render`, and :meth:`.Source.view`,
    wrote the content read into source back into the file.
    It was advised to use :func:`graphviz.render` and :func:`graphviz.view`
    to directly work on files if the superfluous saving needed to be avoided.


.. include:: _links.rst

Existing files
--------------

To directly render an existing DOT source file (e.g. created with other tools),
you can use the :func:`graphviz.render` function. 

.. doctest::

    >>> doctest_mark_exe()

    >>> import pathlib
    >>> import graphviz

    >>> src = 'digraph "the holy hand grenade" { rankdir=LR; 1 -> 2 -> 3 -> lob }'
    >>> filepath = pathlib.Path('doctest-output/the-holy-hand-grenade.gv')
    >>> filepath.write_text(src, encoding='ascii')
    66

    >>> graphviz.render('dot', 'png', str(filepath)).replace('\\', '/')
    'doctest-output/the-holy-hand-grenade.gv.png'

To directly display the graph of an existing DOT source file inside a 
Jupyter `notebook <Jupyter notebook_>`_ or `Qt Console <Jupyter Qt Console_>`_,
you can use the :meth:`.Source.from_file`-classmethod (alternate constructor):

.. image:: _static/qtconsole-source.png
    :align: center

Note that :meth:`~.Source.render` and :meth:`~.Source.view` on the :class:`.Source`
returned by ``.Source.from_file`` skip writing the loaded file back. The same
holds for :meth:`~.Source.save` (resolve default ``.save(skip_existing=None)`` to
``skip_existing_run=True`` to skip writing the read :attr:`~.Source.source`
back into the same file (specifically to the same path that it was loaded from).
Call ``.save(skip_existing=False)`` if you want to re-write the loaded source.

.. admonition:: Historical note

    Before version ``0.18``, ``.render()``, ``.view()``, and ``.save()``
    wrote the content read into source back into the file.
    It was advised to use ``graphviz.render()`` and ``graphiz.view()``
    to directly work on files in case this was needed to avoid.


.. include:: _links.rst

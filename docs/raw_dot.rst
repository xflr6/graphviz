Using raw DOT
-------------

To render a ready-made DOT_ source code string
(instead of assembling one with the higher-level interface
of :class:`.Graph` or :class:`.Digraph`),
create a :class:`graphviz.Source` object holding your DOT string:

.. doctest::

    >>> import graphviz  # doctest: +NO_EXE

    >>> src = graphviz.Source('digraph "the holy hand grenade" { rankdir=LR; 1 -> 2 -> 3 -> lob }')

    >>> src  #doctest: +ELLIPSIS
    <graphviz.sources.Source object at 0x...>

Use the :meth:`~.Source.render` method to save and render it:

.. doctest::

    >>> doctest_mark_exe()  # skip this line

    >>> src.render('doctest-output/holy-grenade.gv').replace('\\', '/')
    'doctest-output/holy-grenade.gv.pdf'

.. doctest::

    >>> doctest_mark_exe()  # skip this line

    >>> src.render('doctest-output/holy-grenade.gv', view=True).replace('\\', '/')  # doctest: +SKIP
    'doctest-output/holy-grenade.gv.pdf'

.. image:: _static/holy-grenade.svg
    :align: center

.. hint::

    Apart from lacking editing methods, :class:`.Source` objects have the same basic API
    as the higher-level :class:`.Graph` and :class:`.Digraph` objects
    (e.g. :meth:`~.Source.save`, :meth:`~.Source.render`, :meth:`~.Source.view`,
    :meth:`~.Source.pipe` methods,
    :attr:`~.Source.engine` and :attr:`~.Source.format` attributes,
    Jupyter notebook :meth:`~.Source._repr_mimebundle_`, etc.
    See :class:`API docs <.Source>`).


.. include:: _links.rst

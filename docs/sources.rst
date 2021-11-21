Using raw DOT
-------------

To render a ready-made DOT source code string (instead of assembling one with
the higher-level interface of :class:`.Graph` or :class:`.Digraph`), create a
:class:`.Source` object holding your DOT string:

.. doctest::

    >>> import graphviz

    >>> src = graphviz.Source('digraph "the holy hand grenade" { rankdir=LR; 1 -> 2 -> 3 -> lob }')  # doctest: +NO_EXE

    >>> src  #doctest: +ELLIPSIS
    <graphviz.sources.Source object at 0x...>

Use the :meth:`~.Source.render`-method to save and render it:

.. doctest::

    >>> doctest_mark_exe()

    >>> src.render('doctest-output/holy-grenade.gv').replace('\\', '/')
    'doctest-output/holy-grenade.gv.pdf'

.. doctest::

    >>> doctest_mark_exe()

    >>> src.render('doctest-output/holy-grenade.gv', view=True).replace('\\', '/')  # doctest: +SKIP
    'doctest-output/holy-grenade.gv.pdf'

.. image:: _static/holy-grenade.svg
    :align: center

Apart from the missing editing methods, :class:`.Source` objects are the same
as the higher-level graph objects (:meth:`~.Source.pipe`-method,
:attr:`~.Source.format`, :attr:`~.Source.engine`, Jupyter notebook repr, etc.),
see above.

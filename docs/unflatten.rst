Unflatten
---------

To prepocess the DOT_ source of a :class:`.Graph` or :class:`.Digraph` with
the `unflatten <DOT unflatten>`_ preprocessor (`PDF <DOT unflatten_pdf_>`_),
use the :meth:`~.Graph.unflatten`-method.

.. doctest::

    >>> import graphviz

    >>> w = graphviz.Digraph('wide')  # doctest: +NO_EXE

    >>> w.edges(('0', str(i)) for i in range(1, 10))

.. doctest::

    >>> doctest_mark_exe()

    >>> w.view()  # doctest: +SKIP

.. image:: _static/wide.svg
    :align: center

unflatten_ is used to improve the aspect ratio of graphs having many leaves or
disconnected nodes.

.. doctest::

    >>> u = w.unflatten(stagger=3)  # doctest: +NO_EXE

.. doctest::

    >>> doctest_mark_exe()

    >>> u.view()  # doctest: +SKIP

.. image:: _static/wide-unflatten-stagger-3.svg
    :align: center

The method returns a :class:`.Source` object that you can
:meth:`~.Source.render`, :meth:`~.Source.view`, etc. with the same API
(minus modification, see details `below <sources>`_).

.. doctest::

    >>> u = w.unflatten(stagger=2)  # doctest: +NO_EXE
    >>> u  # doctest: +ELLIPSIS
    <graphviz.sources.Source object at 0x...>

.. doctest::

    >>> doctest_mark_exe()

    >>> u.view()  # doctest: +SKIP

.. image:: _static/wide-unflatten-stagger-2.svg
    :align: center


.. include:: _links.rst

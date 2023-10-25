Unflatten
---------

To preprocess the DOT_ source of a :class:`.Graph` or :class:`.Digraph` with
the `unflatten <DOT unflatten>`_ preprocessor
(`manpage <DOT unflatten_>`_, `PDF <DOT unflatten_pdf_>`_),
use the :meth:`~.Graph.unflatten` method.

.. doctest::

    >>> import graphviz  # doctest: +NO_EXE

    >>> w = graphviz.Digraph('wide')

    >>> w.edges(('0', str(i)) for i in range(1, 10))

.. doctest::

    >>> doctest_mark_exe()  # skip this line

    >>> w.view()  # doctest: +SKIP

.. image:: _static/wide.svg
    :align: center

.. hint::

    :meth:`~.Graph.unflatten` improves the aspect ratio of graphs
    with many leaves or disconnected nodes.

.. doctest::

    >>> u = w.unflatten(stagger=3)  # doctest: +NO_EXE

.. doctest::

    >>> doctest_mark_exe()  # skip this line

    >>> u.view()  # doctest: +SKIP

.. image:: _static/wide-unflatten-stagger-3.svg
    :align: center

The method returns a :class:`.Source` object
that you can :meth:`~.Source.render`, :meth:`~.Source.view`, etc.
with the same basic API as :class:`.Graph` or :class:`.Digraph` objects
(minus modification, see details :ref:`below <using-raw-dot>`).

.. doctest::

    >>> u = w.unflatten(stagger=2)  # doctest: +NO_EXE
    >>> u  # doctest: +ELLIPSIS
    <graphviz.sources.Source object at 0x...>

.. doctest::

    >>> doctest_mark_exe()  # skip this line

    >>> u.view()  # doctest: +SKIP

.. image:: _static/wide-unflatten-stagger-2.svg
    :align: center


.. include:: _links.rst

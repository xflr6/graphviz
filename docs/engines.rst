Engines
-------

To use a different `layout engine <DOT layouts_>`_ than the default ``dot``
when rendering your graph, you can use the ``engine`` argument
on the constructor of :class:`.Graph` or :class:`.Digraph`.

.. doctest::

    >>> import graphviz  # doctest: +NO_EXE

    >>> g = graphviz.Graph(engine='neato')

You can also change the :attr:`~.Graph.engine` attribute
on an existing instance:

.. doctest::

    >>> g.engine = 'circo'  # doctest: +NO_EXE


.. include:: _links.rst

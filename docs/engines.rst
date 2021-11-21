Engines
-------

To use a different layout command than the default ``dot`` when rendering your
graph, use the :attr:`~.Graph.engine` argument when creating your graph. 

.. doctest::

    >>> import graphviz

    >>> g = graphviz.Graph(engine='neato')  # doctest: +NO_EXE

You can also change the :attr:`~.Graph.engine` attribute of an existing
instance:

.. doctest::

    >>> g.engine = 'circo'  # doctest: +NO_EXE

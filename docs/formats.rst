Formats
-------

To use a different `output file format <DOT outputs_>`_ than the default PDF,
you can use the ``format`` argument when creating your :class:`.Graph`
or :class:`.Digraph` object:

.. doctest::

    >>> import graphviz

    >>> g = graphviz.Graph(format='png')  # doctest: +NO_EXE

You can also change the :attr:`~.Graph.format` attribute on an existing graph
object:


.. doctest::

    >>> doctest_mark_exe()  # skip this line

    >>> dot = graphviz.Digraph('hello')
    >>> dot.edge('hello', 'world')
    >>> dot.format = 'svg'

    >>> dot.render(directory='doctest-output').replace('\\', '/')
    'doctest-output/hello.gv.svg'


.. include:: _links.rst

Piped output
------------

To directly access the raw results from the Graphviz_ ``dot``
`layout command <DOT command_>`_ as binary :class:`bytes`
or as decoded :class:`str` (for plain-text formats like SVG)
instead of writing to a file, use the :meth:`~.Graph.pipe` method
of your :class:`.Graph` or :class:`.Digraph` object:

.. doctest::

    >>> import graphviz

    >>> h = graphviz.Graph('hello', format='svg')  # doctest: +NO_EXE

    >>> h.edge('Hello', 'World')

.. doctest::

    >>> doctest_mark_exe()  # skip this line

    >>> h.pipe(format='pdf')[:4]
    b'%PDF'

    >>> print(h.pipe(encoding='utf-8'))  # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
    <?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <!DOCTYPE svg
    ...
    </svg>

.. tip::

    Because :meth:`~.Graph.pipe` returns the raw ``stdout``
    from the layout subprocess by default (:class:`bytes`),
    you usually want to decode the return value
    when piping into formats like ``'svg'`` or ``'plain'``,

.. caution::

    The output for :meth:`~.Graph.pipe` is buffered in memory,
    so avoid this method if the data size is large.


.. include:: _links.rst

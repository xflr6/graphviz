Piped output
------------

To directly access the results from the Graphviz rendering command (e.g.
``dot``) as binary data string from within Python instead of writing to a file,
use the :meth:`~.Graph.pipe`-method of your :class:`.Graph` or
:class:`.Digraph` object:

.. doctest::

    >>> import graphviz

    >>> h = graphviz.Graph('hello', format='svg')  # doctest: +NO_EXE

    >>> h.edge('Hello', 'World')

.. doctest::

    >>> doctest_mark_exe()

    >>> print(h.pipe().decode('utf-8'))  # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
    <?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <!DOCTYPE svg
    ...
    </svg>

Note that :meth:`~.Graph.pipe` returns the raw ``stdout`` from the rendering
command (:class:`bytes`): When piping into plain-text formats like ``'svg'`` or
``'plain'``, you usually want to decode the return value as shown above.

.. warning::

    The output for :meth:`~.Graph.pipe` is buffered in memory, so do not use
    this method if the data size is large.

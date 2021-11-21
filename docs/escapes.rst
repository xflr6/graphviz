Backslash escapes
-----------------

The Graphviz layout engine supports a number of
`escape sequences <DOT escString_>`_ such as ``\n``, ``\l``, ``\r``
(for multi-line labels: centered, left-justified, right-justified)
and ``\N``, ``\G``, ``\L``
(expanded to the current node name, graph name, object label).
To be able to use them from this library (e.g. for labels),
strings with backslashes are passed on as is.
This means that literal backslashes need to be escaped (doubled) by the user.
As the backslash is also special in Python string literals,
a second level of doubling is needed (e.g. ``label='\\\\'``).
This kind of doubling can be avoided by using `raw string literals`_ (``r'...'``)
instead (same solution as proposed for the stdlib :mod:`re` module):

.. doctest::

    >>> import graphviz

    >>> e = graphviz.Digraph('escapes')  # doctest: +NO_EXE

    >>> e.node('backslash', label=r'\\')
    >>> e.node('multi_line', label=r'centered\nleft\lright\r')

    >>> print(e.source)  # doctest: +NORMALIZE_WHITESPACE
    digraph escapes {
        backslash [label="\\"]
        multi_line [label="centered\nleft\lright\r"]
    }

.. image:: _static/escapes.svg
    :align: center

To disable any special character meaning in a string (e.g. from user input to
be rendered literally), use the :func:`.escape` function (cf. the
:func:`re.escape` function):

.. doctest::

    >>> bs = graphviz.Digraph()  # doctest: +NO_EXE

    >>> bs.node(graphviz.escape('\\'))

    >>> print(bs.source)  # doctest: +NORMALIZE_WHITESPACE
    digraph {
        "\\"
    }

.. admonition:: Historical note

    To prevent breaking the internal quoting mechanism, the special meaning of
    ``\"`` as a backslash-escaped quote has been disabled since version
    ``0.14``. E.g. both ``label='"'`` and ``label='\\"'`` now produce the same
    DOT source ``[label="\""]`` (a label that renders as a literal quote).


.. include:: _links.rst

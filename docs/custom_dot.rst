Custom DOT statements
---------------------

To add arbitrary statements to the created DOT_ source, you can use the
:attr:`~.Graph.body` attribute of :class:`.Graph` and :class:`.Digraph` objects.
It holds the verbatim :class:`list` of (:class:`str`) lines to be written to the source file
(including their final newline).
Use its ``append()`` or ``extend()`` method:

.. doctest::

    >>> import graphviz

    >>> rt = graphviz.Digraph(comment='The Round Table')  # doctest: +NO_EXE

    >>> rt.body.append('\t"King Arthur" -> {\n\t\t"Sir Bedevere", "Sir Lancelot"\n\t}\n')
    >>> rt.edge('Sir Bedevere', 'Sir Lancelot', constraint='false')

    >>> print(rt.source)  # doctest: +NORMALIZE_WHITESPACE
    // The Round Table
    digraph {
        "King Arthur" -> {
            "Sir Bedevere", "Sir Lancelot"
        }
        "Sir Bedevere" -> "Sir Lancelot" [constraint=false]
    }

.. attention::

    Note that you might need to correctly quote/escape identifiers
    and strings containing whitespace or other special characters
    when using this method.


.. include:: _links.rst

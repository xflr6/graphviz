Custom DOT statements
---------------------

To add arbitrary statements to the created DOT_ source, use the
:attr:`~.Graph.body` attribute of the :class:`.Graph` or :class:`.Digraph`
object. It holds the verbatim :class:`list` of lines to be written to the source file
(including their newline). Use its ``append()``- or ``extend()``-method:

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

Note that you might need to correctly quote/escape identifiers and strings
containing whitespace or other special characters when using this method.


.. include:: _links.rst

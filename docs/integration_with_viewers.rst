Integration with viewers
------------------------

On platforms such as Windows, viewer programs opened by :meth:`~.Graph.render`
with ``view=True`` (or equivalently with the :meth:`~.Graph.view` shortcut-method)
might **lock** the (PDF, PNG, etc.) file for as long as the viewer is open
(blocking re-rendering it with a ``Permission denied`` error).

.. tip::

    You can use the :func:`tempfile.mktemp` function
    from the stdlib :mod:`tempfile` module to render to a different file
    for each invocation. This avoids needing to close the viewer window
    each time within such an incremental workflow
    (and also serves to preserves the intermediate steps).

.. doctest::

    >>> import tempfile  # doctest: +NO_EXE
    >>> import graphviz

    >>> g = graphviz.Graph()

    >>> g.node('spam')

.. doctest::

    >>> doctest_mark_exe()  # skip this line

    >>> g.view(tempfile.mktemp('.gv'))  # doctest: +SKIP
    'C:\\Users\\User\\AppData\\Local\\Temp\\tmp3aoie8d0.gv.pdf'

    >>> g.view(tempfile.mktemp('.gv'))  # doctest: +SKIP
    'C:\\Users\\User\\AppData\\Local\\Temp\\tmphh4ig7a_.gv.pdf'

Other options:

- use a viewer that `support live updates <live viewer updates_>`_

- use the `Jupyter notebook`_ or `Qt Console <Jupyter Qt Console_>`_
  (display the current version of the rendered graph
  in repeated add/render/view cycles)


.. include:: _links.rst

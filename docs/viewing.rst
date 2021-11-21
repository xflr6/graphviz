Integration with viewers
------------------------

On platforms such as Windows, viewer programs opened by rendering with
``view=True`` or the :meth:`~.Graph.view`-method might lock the (PDF, PNG,
etc.) file for as long as the viewer is open (blocking re-rendering it with a
``Permission denied`` error). You can use the :func:`~tempfile.mktemp` function
from the stdlib :mod:`tempfile` module to render to a different file for each
invocation to avoid needing to close the viewer window each time within such an
incremental workflow (and also preserve its intermediate steps):

.. doctest::

    >>> import graphviz  # doctest: +NO_EXE
    >>> import tempfile

    >>> g = graphviz.Graph()

    >>> g.node('spam')

.. doctest::

    >>> doctest_mark_exe()

    >>> g.view(tempfile.mktemp('.gv'))  # doctest: +SKIP
    'C:\\Users\\User\\AppData\\Local\\Temp\\tmp3aoie8d0.gv.pdf'

    >>> g.view(tempfile.mktemp('.gv'))  # doctest: +SKIP
    'C:\\Users\\User\\AppData\\Local\\Temp\\tmphh4ig7a_.gv.pdf'

Other options are viewers that `support live updates <live viewer updates_>`_
or using the `Jupyter notebook`_ or `Qt Console <Jupyter Qt Console_>`_ to
display the current version of the rendered graph in repeated add/render/view
cycles.


.. include:: _links.rst
Jupyter notebooks
-----------------

:class:`.Graph` and :class:`.Digraph` objects have a
:meth:`~.Graph._repr_mimebundle_` method so they can be rendered and displayed
directly inside a `Jupyter notebook`_.
For an example, check the ``examples/graphviz-notebook.ipynb`` file
in the `source repository/distribution <GitHub graphviz-notebook.ipynb_>`_
(or the same notebook in `nbviewer <nbviewer graphviz-notebook.ipynb_>`_).

This also allows direct displaying within the `Jupyter Qt Console`_
(also `the one <Spyder ipythonconsole_>`_ inside `Spyder IDE`_):

.. image:: _static/qtconsole.png
    :align: center

By default :meth:`~.Graph._repr_mimebundle_` uses ``'svg'`` format.
You can use the :func:`graphviz.set_jupyter_format` to override the default format
that is used for displaying in IPython/Jupyter.
(`example <GitHub graphviz-jupyter-format.ipynb_>`_,
`nbviewer <nbviewer graphviz-jupyter-format.ipynb_>`_).

.. hint::

    You can also use ``display_svg()``, ``display_png()``, or ``.display_jpeg()``
    from `IPython.display`_ to display the rendered
    :class:`.Graph` or :class:`.Digraph` as SVG, PNG or JPEG
    in IPython/Jupyter.


.. include:: _links.rst

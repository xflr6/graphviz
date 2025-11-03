API Reference
=============

.. autosummary::
    :nosignatures:

    graphviz.Graph
    graphviz.Digraph
    graphviz.Source
    graphviz.escape
    graphviz.nohtml
    graphviz.ExecutableNotFound
    graphviz.CalledProcessError
    graphviz.RequiredArgumentError
    graphviz.render
    graphviz.pipe
    graphviz.pipe_string
    graphviz.unflatten
    graphviz.view
    graphviz.version

.. hint::

    The two main classes :class:`.Graph` and :class:`.Digraph`
    (creating **undirected** vs. **directed** graphs) have exactly the same API.
    Their division reflects the fact that both graph syntaxes cannot be mixed.


Graph
-----

.. autoclass:: graphviz.Graph
    :members:
        directed,
        name, comment,
        filename, directory,
        format, engine, encoding, renderer, formatter,
        graph_attr, node_attr, edge_attr,
        body,
        strict,
        __iter__,
        source,
        node, edge, edges, attr, subgraph,
        filepath, save, render, view, pipe, unflatten,
        _repr_mimebundle_,
        clear, copy


Digraph
-------

.. autoclass:: graphviz.Digraph
    :members:
        directed,
        name, comment,
        filename, directory,
        format, engine, encoding, renderer, formatter,
        graph_attr, node_attr, edge_attr,
        body,
        strict,
        __iter__,
        source,
        node, edge, edges, attr, subgraph,
        filepath, save, render, view, pipe, unflatten,
        _repr_mimebundle_,
        clear, copy


Source
------

.. autoclass:: graphviz.Source
    :members:
        from_file,
        filename, directory,
        format, engine, encoding, renderer, formatter,
        __iter__,
        source,
        filepath, save, render, view, pipe, unflatten,
        _repr_mimebundle_,
        copy


Quoting/escaping
----------------

.. autofunction:: graphviz.escape

.. autofunction:: graphviz.nohtml


Exceptions
----------

.. autoexception:: graphviz.ExecutableNotFound

.. autoexception:: graphviz.CalledProcessError

.. autoexception:: graphviz.RequiredArgumentError

.. autoexception:: graphviz.FileExistsError


Warnings
--------

.. autoexception:: graphviz.UnknownSuffixWarning

.. autoexception:: graphviz.FormatSuffixMismatchWarning

.. autoexception:: graphviz.DotSyntaxWarning


Low-level functions
-------------------

The functions in this section are provided to work directly
with existing files and strings instead of using the object-oriented
DOT_ creation methods documented above.

.. autofunction:: graphviz.render
.. autofunction:: graphviz.pipe
.. autofunction:: graphviz.pipe_string
.. autofunction:: graphviz.pipe_lines
.. autofunction:: graphviz.pipe_lines_string
.. autofunction:: graphviz.unflatten
.. autofunction:: graphviz.view


Constants
---------

Manually maintained allowlists for Graphviz_ **parameters**
(cf. `man dot <DOT manpage_pdf_>`_, `outputs <DOT outputs_>`_, and ``dot -T:`` output):

.. autodata:: graphviz.ENGINES
   :annotation:

.. autodata:: graphviz.FORMATS
   :annotation:

.. autodata:: graphviz.RENDERERS
   :annotation:

.. autodata:: graphviz.FORMATTERS
   :annotation:

Supported **IPython/Jupyter display formats**:

.. autodata:: graphviz.SUPPORTED_JUPYTER_FORMATS
   :annotation:

Names of **upstream binaries**:

.. autodata:: graphviz.DOT_BINARY
   :annotation:

.. autodata:: graphviz.UNFLATTEN_BINARY
   :annotation:


Defaults
--------

Functions for setting **package-wide defaults** for ``engine`` and ``format``:

.. attention::

    These functions are provided mainly to simplify testing
    but may also be used by end-users for convenience in scripts.
    They **should be avoided in library code**.
    Prefer passing or setting ``engine`` and ``format`` explicitly
    if you create a library that depends on this package.

.. autofunction:: graphviz.set_default_engine

.. autofunction:: graphviz.set_default_format


Function for setting the **package-wide default for IPython/Jupyter display format**:

.. attention::

    This function is provided for end-users.
    Prefer `IPython.display`_ functions in library code.

.. autofunction:: graphviz.set_jupyter_format


Other
-----

.. autofunction:: graphviz.version


.. include:: _links.rst


Online ``help()`` (internal)
----------------------------

Results of :func:`help` for :class:`graphviz.Graph`, :class:`graphviz.Digraph`,
and :class:`graphviz.Source` for reference.

.. attention::

    The outputs in this section may contain (some) **internals** (implementation details).
    They serve to record some current implementation details and their changes.
    They mainly serve the development process (e.g. checking the MRO).
    They might be outdated.
    They **may change at any point** in time.
    See above for the full (public) API.
    First shalt thou take out the Holy Pin.
    Then shalt thou count to three, no more, no less.

To **update** :func:`help` outputs below:

.. code:: bash

    $ ./update-help.py

To **debug**: remove ``+SKIP`` flags below and check output(s):

.. code:: bash

    $ ./run-tests.py docs --doctest-report none


Graph
"""""

Partially syntax-highlighted:
https://github.com/xflr6/graphviz/blob/master/docs/api.rst#graph-1

.. doctest::

    >>> import graphviz
    >>> help(graphviz.Graph)  # doctest: +NORMALIZE_WHITESPACE +SKIP
    Help on class Graph in module graphviz.graphs:
    <BLANKLINE>
    class Graph(graphviz.dot.GraphSyntax, BaseGraph)
     |  Graph(
     |      name: str | None = None,
     |      comment: str | None = None,
     |      filename=None,
     |      directory=None,
     |      format: str | None = None,
     |      engine: str | None = None,
     |      encoding: str | None = 'utf-8',
     |      graph_attr: Mapping[str, str] | None = None,
     |      node_attr: Mapping[str, str] | None = None,
     |      edge_attr: Mapping[str, str] | None = None,
     |      body: Iterable[str] | None = None,
     |      strict: bool = False,
     |      *,
     |      renderer: str | None = None,
     |      formatter: str | None = None
     |  ) -> None
     |
     |  Graph source code in the DOT language.
     |
     |  Args:
     |      name: Graph name used in the source code.
     |      comment: Comment added to the first line of the source.
     |      filename: Filename for saving the source
     |          (defaults to ``name`` + ``'.gv'``).
     |      directory: (Sub)directory for source saving and rendering.
     |      format: Rendering output format (``'pdf'``, ``'png'``, ...).
     |      engine: Layout command used (``'dot'``, ``'neato'``, ...).
     |      renderer: Output renderer used (``'cairo'``, ``'gd'``, ...).
     |      formatter: Output formatter used (``'cairo'``, ``'gd'``, ...).
     |      encoding: Encoding for saving the source.
     |      graph_attr: Mapping of ``(attribute, value)`` pairs for the graph.
     |      node_attr: Mapping of ``(attribute, value)`` pairs set for all nodes.
     |      edge_attr: Mapping of ``(attribute, value)`` pairs set for all edges.
     |      body: Iterable of verbatim lines (including their final newline)
     |          to add to the graph ``body``.
     |      strict (bool): Rendering should merge multi-edges.
     |
     |  Note:
     |      All parameters are `optional` and can be changed under their
     |      corresponding attribute name after instance creation.
     |
     |  Method resolution order:
     |      Graph
     |      graphviz.dot.GraphSyntax
     |      BaseGraph
     |      graphviz.dot.Dot
     |      graphviz.quoting.Quote
     |      graphviz.rendering.Render
     |      graphviz.saving.Save
     |      graphviz.jupyter_integration.JupyterIntegration
     |      graphviz.piping.Pipe
     |      graphviz.unflattening.Unflatten
     |      graphviz.encoding.Encoding
     |      graphviz.base.Base
     |      graphviz.base.LineIterable
     |      graphviz.backend.mixins.Render
     |      graphviz.backend.mixins.Pipe
     |      graphviz.parameters.mixins.Parameters
     |      graphviz.parameters.engines.Engine
     |      graphviz.parameters.formats.Format
     |      graphviz.parameters.renderers.Renderer
     |      graphviz.parameters.formatters.Formatter
     |      graphviz.parameters.base.ParameterBase
     |      graphviz.copying.CopyBase
     |      graphviz.backend.mixins.View
     |      graphviz.backend.mixins.Unflatten
     |      builtins.object
     |
     |  Readonly properties defined here:
     |
     |  directed
     |      ``False``
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from graphviz.dot.GraphSyntax:
     |
     |  __dict__
     |      dictionary for instance variables
     |
     |  __weakref__
     |      list of weak references to the object
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from BaseGraph:
     |
     |  __init__(
     |      self,
     |      name: str | None = None,
     |      comment: str | None = None,
     |      filename=None,
     |      directory=None,
     |      format: str | None = None,
     |      engine: str | None = None,
     |      encoding: str | None = 'utf-8',
     |      graph_attr: Mapping[str, str] | None = None,
     |      node_attr: Mapping[str, str] | None = None,
     |      edge_attr: Mapping[str, str] | None = None,
     |      body: Iterable[str] | None = None,
     |      strict: bool = False,
     |      *,
     |      renderer: str | None = None,
     |      formatter: str | None = None
     |  ) -> None
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  ----------------------------------------------------------------------
     |  Readonly properties inherited from BaseGraph:
     |
     |  source
     |      The generated DOT source code as string.
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.dot.Dot:
     |
     |  __iter__(self, subgraph: bool = False) -> Iterator[str]
     |      Yield the DOT source code line by line (as graph or subgraph).
     |
     |      Yields: Line ending with a newline (``'\n'``).
     |
     |  attr(self, kw: str | None = None, _attributes=None, **attrs: str) -> None
     |      Add a general or graph/node/edge attribute statement.
     |
     |      Args:
     |          kw: Attributes target
     |              (``None`` or ``'graph'``, ``'node'``, ``'edge'``).
     |          attrs: Attributes to be set (must be strings, may be empty).
     |
     |      See the :ref:`usage examples in the User Guide <attributes>`.
     |
     |  clear(self, keep_attrs: bool = False) -> None
     |      Reset content to an empty body, clear graph/node/egde_attr mappings.
     |
     |      Args:
     |          keep_attrs (bool): preserve graph/node/egde_attr mappings
     |
     |  edge(
     |      self,
     |      tail_name: str,
     |      head_name: str,
     |      label: str | None = None,
     |      _attributes=None,
     |      **attrs: str
     |  ) -> None
     |      Create an edge between two nodes.
     |
     |      Args:
     |          tail_name: Start node identifier
     |              (format: ``node[:port[:compass]]``).
     |          head_name: End node identifier
     |              (format: ``node[:port[:compass]]``).
     |          label: Caption to be displayed near the edge.
     |          attrs: Any additional edge attributes (must be strings).
     |
     |      Note:
     |          The ``tail_name`` and ``head_name`` strings are separated
     |          by (optional) colon(s) into ``node`` name, ``port`` name,
     |          and ``compass`` (e.g. ``sw``).
     |          See :ref:`details in the User Guide <node-ports-compass>`.
     |
     |      Attention:
     |          When rendering ``label``, backslash-escapes
     |          and strings of the form ``<...>`` have a special meaning.
     |          See the sections :ref:`backslash-escapes` and
     |          :ref:`quoting-and-html-like-labels` in the user guide for details.
     |
     |  edges(self, tail_head_iter: Iterable[tuple[str, str]]) -> None
     |      Create a bunch of edges.
     |
     |      Args:
     |          tail_head_iter: Iterable of ``(tail_name, head_name)`` pairs
     |              (format:``node[:port[:compass]]``).
     |
     |
     |      Note:
     |          The ``tail_name`` and ``head_name`` strings are separated
     |          by (optional) colon(s) into ``node`` name, ``port`` name,
     |          and ``compass`` (e.g. ``sw``).
     |          See :ref:`details in the User Guide <node-ports-compass>`.
     |
     |  node(self,
             name: str,
             label: str | None = None,
             _attributes=None, **attrs: str) -> None
     |      Create a node.
     |
     |      Args:
     |          name: Unique identifier for the node inside the source.
     |          label: Caption to be displayed (defaults to the node ``name``).
     |          attrs: Any additional node attributes (must be strings).
     |
     |      Attention:
     |          When rendering ``label``, backslash-escapes
     |          and strings of the form ``<...>`` have a special meaning.
     |          See the sections :ref:`backslash-escapes` and
     |          :ref:`quoting-and-html-like-labels` in the user guide for details.
     |
     |  subgraph(
     |      self,
     |      graph=None,
     |      name: str | None = None,
     |      comment: str | None = None,
     |      graph_attr: Mapping[str, str] | None = None,
     |      node_attr: Mapping[str, str] | None = None,
     |      edge_attr: Mapping[str, str] | None = None,
     |      body=None
     |  )
     |      Add the current content of the given sole ``graph`` argument
     |          as subgraph or return a context manager
     |          returning a new graph instance
     |          created with the given (``name``, ``comment``, etc.) arguments
     |          whose content is added as subgraph
     |          when leaving the context manager's ``with``-block.
     |
     |      Args:
     |          graph: An instance of the same kind
     |              (:class:`.Graph`, :class:`.Digraph`) as the current graph
     |              (sole argument in non-with-block use).
     |          name: Subgraph name (``with``-block use).
     |          comment: Subgraph comment (``with``-block use).
     |          graph_attr: Subgraph-level attribute-value mapping
     |              (``with``-block use).
     |          node_attr: Node-level attribute-value mapping
     |              (``with``-block use).
     |          edge_attr: Edge-level attribute-value mapping
     |              (``with``-block use).
     |          body: Verbatim lines to add to the subgraph ``body``
     |              (``with``-block use).
     |
     |      See the :ref:`usage examples in the User Guide <subgraphs-clusters>`.
     |
     |      When used as a context manager, the returned new graph instance
     |      uses ``strict=None`` and the parent graph's values
     |      for ``directory``, ``format``, ``engine``, and ``encoding`` by default.
     |
     |      Note:
     |          If the ``name`` of the subgraph begins with
     |          ``'cluster'`` (all lowercase)
     |          the layout engine will treat it as a special cluster subgraph.
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.rendering.Render:
     |
     |  render(
     |      self,
     |      filename: os.PathLike[str] | str | None = None,
     |      directory: os.PathLike[str] | str | None = None,
     |      view: bool = False,
     |      cleanup: bool = False,
     |      format: str | None = None,
     |      renderer: str | None = None,
     |      formatter: str | None = None,
     |      neato_no_op: bool | int | None = None,
     |      quiet: bool = False,
     |      quiet_view: bool = False,
     |      *,
     |      y_invert: bool = False,
     |      outfile: os.PathLike[str] | str | None = None,
     |      engine: str | None = None,
     |      raise_if_result_exists: bool = False,
     |      overwrite_source: bool = False
     |  ) -> str
     |      Save the source to file and render with the Graphviz engine.
     |
     |      Args:
     |          filename: Filename for saving the source
     |              (defaults to ``name`` + ``'.gv'``).s
     |          directory: (Sub)directory for source saving and rendering.
     |          view (bool): Open the rendered result
     |              with the default application.
     |          cleanup (bool): Delete the source file
     |              after successful rendering.
     |          format: The output format used for rendering
     |              (``'pdf'``, ``'png'``, etc.).
     |          renderer: The output renderer used for rendering
     |              (``'cairo'``, ``'gd'``, ...).
     |          formatter: The output formatter used for rendering
     |              (``'cairo'``, ``'gd'``, ...).
     |          neato_no_op: Neato layout engine no-op flag.
     |          quiet (bool): Suppress ``stderr`` output
     |              from the layout subprocess.
     |          quiet_view (bool): Suppress ``stderr`` output
     |              from the viewer process
     |              (implies ``view=True``, ineffective on Windows platform).
     |          y_invert: Invert y coordinates in the rendered output.
     |          outfile: Path for the rendered output file.
     |          engine: Layout engine for rendering
     |              (``'dot'``, ``'neato'``, ...).
     |          raise_if_result_exists: Raise :exc:`graphviz.FileExistsError`
     |              if the result file exists.
     |          overwrite_source: Allow ``dot`` to write to the file it reads from.
     |              Incompatible with ``raise_if_result_exists``.
     |
     |      Returns:
     |          The (possibly relative) path of the rendered file.
     |
     |      Raises:
     |          ValueError: If ``engine``, ``format``, ``renderer``, or ``formatter``
     |              are unknown.
     |          graphviz.RequiredArgumentError: If ``formatter`` is given
     |              but ``renderer`` is None.
     |          ValueError: If ``outfile`` is the same file as the source file
     |              unless ``overwite_source=True``.
     |          graphviz.ExecutableNotFound: If the Graphviz ``dot`` executable
     |              is not found.
     |          graphviz.CalledProcessError: If the returncode (exit status)
     |              of the rendering ``dot`` subprocess is non-zero.
     |          RuntimeError: If viewer opening is requested but not supported.
     |
     |      Example:
     |          >>> doctest_mark_exe()
     |          >>> import graphviz
     |          >>> dot = graphviz.Graph(name='spam', directory='doctest-output')
     |          >>> dot.render(format='png').replace('\', '/')
     |          'doctest-output/spam.gv.png'
     |          >>> dot.render(outfile='spam.svg').replace('\', '/')
     |          'doctest-output/spam.svg'
     |
     |      Note:
     |          The layout command is started from the directory of ``filepath``,
     |          so that references to external files
     |          (e.g. ``[image=images/camelot.png]``)
     |          can be given as paths relative to the DOT source file.
     |
     |  view(
     |      self,
     |      filename: os.PathLike[str] | str | None = None,
     |      directory: os.PathLike[str] | str | None = None,
     |      cleanup: bool = False,
     |      quiet: bool = False,
     |      quiet_view: bool = False
     |  ) -> str
     |      Save the source to file, open the rendered result in a viewer.
     |
     |      Convenience short-cut for running ``.render(view=True)``.
     |
     |      Args:
     |          filename: Filename for saving the source
     |              (defaults to ``name`` + ``'.gv'``).
     |          directory: (Sub)directory for source saving and rendering.
     |          cleanup (bool): Delete the source file after successful rendering.
     |          quiet (bool): Suppress ``stderr`` output from the layout subprocess.
     |          quiet_view (bool): Suppress ``stderr`` output
     |              from the viewer process (ineffective on Windows).
     |
     |      Returns:
     |          The (possibly relative) path of the rendered file.
     |
     |      Raises:
     |          graphviz.ExecutableNotFound: If the Graphviz executable
     |              is not found.
     |          graphviz.CalledProcessError: If the exit status is non-zero.
     |          RuntimeError: If opening the viewer is not supported.
     |
     |      Short-cut method for calling :meth:`.render` with ``view=True``.
     |
     |      Note:
     |          There is no option to wait for the application to close,
     |          and no way to retrieve the application's exit status.
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.saving.Save:
     |
     |  save(
     |      self,
     |      filename: os.PathLike[str] | str | None = None,
     |      directory: os.PathLike[str] | str | None = None,
     |      *,
     |      skip_existing: bool | None = False
     |  ) -> str
     |      Save the DOT source to file. Ensure the file ends with a newline.
     |
     |      Args:
     |          filename: Filename for saving the source (defaults to ``name`` + ``'.gv'``)
     |          directory: (Sub)directory for source saving and rendering.
     |          skip_existing: Skip write if file exists (default: ``False``).
     |
     |      Returns:
     |          The (possibly relative) path of the saved source file.
     |
     |  ----------------------------------------------------------------------
     |  Readonly properties inherited from graphviz.saving.Save:
     |
     |  filepath
     |      The target path for saving the DOT source file.
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from graphviz.saving.Save:
     |
     |  directory = ''
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.piping.Pipe:
     |
     |  pipe(
     |      self,
     |      format: str | None = None,
     |      renderer: str | None = None,
     |      formatter: str | None = None,
     |      neato_no_op: bool | int | None = None,
     |      quiet: bool = False,
     |      *,
     |      y_invert: bool = False,
     |      engine: str | None = None,
     |      encoding: str | None = None
     |  ) -> bytes | str
     |      Return the source piped through the Graphviz layout command.
     |
     |      Args:
     |          format: The output format used for rendering
     |              (``'pdf'``, ``'png'``, etc.).
     |          renderer: The output renderer used for rendering
     |              (``'cairo'``, ``'gd'``, ...).
     |          formatter: The output formatter used for rendering
     |              (``'cairo'``, ``'gd'``, ...).
     |          neato_no_op: Neato layout engine no-op flag.
     |          quiet (bool): Suppress ``stderr`` output
     |              from the layout subprocess.
     |          y_invert: Invert y coordinates in the rendered output.
     |          engine: Layout engine for rendering
     |              (``'dot'``, ``'neato'``, ...).
     |          encoding: Encoding for decoding the stdout.
     |
     |      Returns:
     |          Bytes or if encoding is given decoded string
     |              (stdout of the layout command).
     |
     |      Raises:
     |          ValueError: If ``engine``, ``format``, ``renderer``, or ``formatter``
     |              are unknown.
     |          graphviz.RequiredArgumentError: If ``formatter`` is given
     |              but ``renderer`` is None.
     |          graphviz.ExecutableNotFound: If the Graphviz ``dot`` executable
     |              is not found.
     |          graphviz.CalledProcessError: If the returncode (exit status)
     |              of the rendering ``dot`` subprocess is non-zero.
     |
     |      Example:
     |          >>> doctest_mark_exe()
     |          >>> import graphviz
     |          >>> source = 'graph { spam }'
     |          >>> graphviz.Source(source, format='svg').pipe()[:14]
     |          b'<?xml version='
     |          >>> graphviz.Source(source, format='svg').pipe(encoding='ascii')[:14]
     |          '<?xml version='
     |          >>> graphviz.Source(source, format='svg').pipe(encoding='utf-8')[:14]
     |          '<?xml version='
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.unflattening.Unflatten:
     |
     |  unflatten(
     |      self,
     |      stagger: int | None = None,
     |      fanout: bool = False,
     |      chain: int | None = None
     |  ) -> graphviz.Source
     |      Return a new :class:`.Source` instance with the source
     |          piped through the Graphviz *unflatten* preprocessor.
     |
     |      Args:
     |          stagger: Stagger the minimum length
     |              of leaf edges between 1 and this small integer.
     |          fanout: Fanout nodes with indegree = outdegree = 1
     |              when staggering (requires ``stagger``).
     |          chain: Form disconnected nodes into chains
     |              of up to this many nodes.
     |
     |      Returns:
     |          Prepocessed DOT source code (improved layout aspect ratio).
     |
     |      Raises:
     |          graphviz.RequiredArgumentError: If ``fanout`` is given
     |              but ``stagger`` is None.
     |          graphviz.ExecutableNotFound: If the Graphviz ``unflatten`` executable
     |              is not found.
     |          graphviz.CalledProcessError: If the returncode (exit status)
     |              of the unflattening 'unflatten' subprocess is non-zero.
     |
     |      See also:
     |          Upstream documentation:
     |          https://www.graphviz.org/pdf/unflatten.1.pdf
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from graphviz.encoding.Encoding:
     |
     |  encoding
     |      The encoding for the saved source file.
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.base.Base:
     |
     |  __str__(self) -> str
     |      The DOT source code as string.
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from graphviz.parameters.engines.Engine:
     |
     |  engine
     |      The layout engine used for rendering
     |      (``'dot'``, ``'neato'``, ...).
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from graphviz.parameters.formats.Format:
     |
     |  format
     |      The output format used for rendering
     |      (``'pdf'``, ``'png'``, ...).
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from graphviz.parameters.renderers.Renderer:
     |
     |  renderer
     |      The output renderer used for rendering
     |      (``'cairo'``, ``'gd'``, ...).
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from graphviz.parameters.formatters.Formatter:
     |
     |  formatter
     |      The output formatter used for rendering
     |      (``'cairo'``, ``'gd'``, ...).
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.copying.CopyBase:
     |
     |  copy(self)
     |      Return a copied instance of the object.
     |
     |      Returns:
     |          An independent copy of the current object.
    <BLANKLINE>


Digraph
"""""""

Partially symntax-highlighed:
https://github.com/xflr6/graphviz/blob/master/docs/api.rst#digraph-1

.. doctest::

    >>> import graphviz
    >>> help(graphviz.Digraph)  # doctest: +NORMALIZE_WHITESPACE +SKIP
    Help on class Digraph in module graphviz.graphs:
    <BLANKLINE>
    class Digraph(graphviz.dot.DigraphSyntax, BaseGraph)
     |  Digraph(
     |      name: str | None = None,
     |      comment: str | None = None,
     |      filename=None,
     |      directory=None,
     |      format: str | None = None,
     |      engine: str | None = None,
     |      encoding: str | None = 'utf-8',
     |      graph_attr: Mapping[str, str] | None = None,
     |      node_attr: Mapping[str, str] | None = None,
     |      edge_attr: Mapping[str, str] | None = None,
     |      body: Iterable[str] | None = None,
     |      strict: bool = False,
     |      *,
     |      renderer: str | None = None,
     |      formatter: str | None = None
     |  ) -> None
     |
     |  Directed graph source code in the DOT language.
     |
     |  Args:
     |      name: Graph name used in the source code.
     |      comment: Comment added to the first line of the source.
     |      filename: Filename for saving the source
     |          (defaults to ``name`` + ``'.gv'``).
     |      directory: (Sub)directory for source saving and rendering.
     |      format: Rendering output format (``'pdf'``, ``'png'``, ...).
     |      engine: Layout command used (``'dot'``, ``'neato'``, ...).
     |      renderer: Output renderer used (``'cairo'``, ``'gd'``, ...).
     |      formatter: Output formatter used (``'cairo'``, ``'gd'``, ...).
     |      encoding: Encoding for saving the source.
     |      graph_attr: Mapping of ``(attribute, value)`` pairs for the graph.
     |      node_attr: Mapping of ``(attribute, value)`` pairs set for all nodes.
     |      edge_attr: Mapping of ``(attribute, value)`` pairs set for all edges.
     |      body: Iterable of verbatim lines (including their final newline)
     |          to add to the graph ``body``.
     |      strict (bool): Rendering should merge multi-edges.
     |
     |  Note:
     |      All parameters are `optional` and can be changed under their
     |      corresponding attribute name after instance creation.
     |
     |  Method resolution order:
     |      Digraph
     |      graphviz.dot.DigraphSyntax
     |      BaseGraph
     |      graphviz.dot.Dot
     |      graphviz.quoting.Quote
     |      graphviz.rendering.Render
     |      graphviz.saving.Save
     |      graphviz.jupyter_integration.JupyterIntegration
     |      graphviz.piping.Pipe
     |      graphviz.unflattening.Unflatten
     |      graphviz.encoding.Encoding
     |      graphviz.base.Base
     |      graphviz.base.LineIterable
     |      graphviz.backend.mixins.Render
     |      graphviz.backend.mixins.Pipe
     |      graphviz.parameters.mixins.Parameters
     |      graphviz.parameters.engines.Engine
     |      graphviz.parameters.formats.Format
     |      graphviz.parameters.renderers.Renderer
     |      graphviz.parameters.formatters.Formatter
     |      graphviz.parameters.base.ParameterBase
     |      graphviz.copying.CopyBase
     |      graphviz.backend.mixins.View
     |      graphviz.backend.mixins.Unflatten
     |      builtins.object
     |
     |  Readonly properties defined here:
     |
     |  directed
     |      ``True``
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from graphviz.dot.DigraphSyntax:
     |
     |  __dict__
     |      dictionary for instance variables
     |
     |  __weakref__
     |      list of weak references to the object
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from BaseGraph:
     |
     |  __init__(
     |      self,
     |      name: str | None = None,
     |      comment: str | None = None,
     |      filename=None,
     |      directory=None,
     |      format: str | None = None,
     |      engine: str | None = None,
     |      encoding: str | None = 'utf-8',
     |      graph_attr: Mapping[str, str] | None = None,
     |      node_attr: Mapping[str, str] | None = None,
     |      edge_attr: Mapping[str, str] | None = None,
     |      body: Iterable[str] | None = None,
     |      strict: bool = False,
     |      *,
     |      renderer: str | None = None,
     |      formatter: str | None = None
     |  ) -> None
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  ----------------------------------------------------------------------
     |  Readonly properties inherited from BaseGraph:
     |
     |  source
     |      The generated DOT source code as string.
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.dot.Dot:
     |
     |  __iter__(self, subgraph: bool = False) -> Iterator[str]
     |      Yield the DOT source code line by line (as graph or subgraph).
     |
     |      Yields: Line ending with a newline (``'\n'``).
     |
     |  attr(self, kw: str | None = None, _attributes=None, **attrs: str) -> None
     |      Add a general or graph/node/edge attribute statement.
     |
     |      Args:
     |          kw: Attributes target
     |              (``None`` or ``'graph'``, ``'node'``, ``'edge'``).
     |          attrs: Attributes to be set (must be strings, may be empty).
     |
     |      See the :ref:`usage examples in the User Guide <attributes>`.
     |
     |  clear(self, keep_attrs: bool = False) -> None
     |      Reset content to an empty body, clear graph/node/egde_attr mappings.
     |
     |      Args:
     |          keep_attrs (bool): preserve graph/node/egde_attr mappings
     |
     |  edge(
     |      self,
     |      tail_name: str,
     |      head_name: str,
     |      label: str | None = None,
     |      _attributes=None,
     |      **attrs: str
     |  ) -> None
     |      Create an edge between two nodes.
     |
     |      Args:
     |          tail_name: Start node identifier
     |              (format: ``node[:port[:compass]]``).
     |          head_name: End node identifier
     |              (format: ``node[:port[:compass]]``).
     |          label: Caption to be displayed near the edge.
     |          attrs: Any additional edge attributes (must be strings).
     |
     |      Note:
     |          The ``tail_name`` and ``head_name`` strings are separated
     |          by (optional) colon(s) into ``node`` name, ``port`` name,
     |          and ``compass`` (e.g. ``sw``).
     |          See :ref:`details in the User Guide <node-ports-compass>`.
     |
     |      Attention:
     |          When rendering ``label``, backslash-escapes
     |          and strings of the form ``<...>`` have a special meaning.
     |          See the sections :ref:`backslash-escapes` and
     |          :ref:`quoting-and-html-like-labels` in the user guide for details.
     |
     |  edges(self, tail_head_iter: Iterable[tuple[str, str]]) -> None
     |      Create a bunch of edges.
     |
     |      Args:
     |          tail_head_iter: Iterable of ``(tail_name, head_name)`` pairs
     |              (format:``node[:port[:compass]]``).
     |
     |
     |      Note:
     |          The ``tail_name`` and ``head_name`` strings are separated
     |          by (optional) colon(s) into ``node`` name, ``port`` name,
     |          and ``compass`` (e.g. ``sw``).
     |          See :ref:`details in the User Guide <node-ports-compass>`.
     |
     |  node(self,
             name: str,
             label: str | None = None,
             _attributes=None, **attrs: str) -> None
     |      Create a node.
     |
     |      Args:
     |          name: Unique identifier for the node inside the source.
     |          label: Caption to be displayed (defaults to the node ``name``).
     |          attrs: Any additional node attributes (must be strings).
     |
     |      Attention:
     |          When rendering ``label``, backslash-escapes
     |          and strings of the form ``<...>`` have a special meaning.
     |          See the sections :ref:`backslash-escapes` and
     |          :ref:`quoting-and-html-like-labels` in the user guide for details.
     |
     |  subgraph(
     |      self,
     |      graph=None,
     |      name: str | None = None,
     |      comment: str | None = None,
     |      graph_attr: Mapping[str, str] | None = None,
     |      node_attr: Mapping[str, str] | None = None,
     |      edge_attr: Mapping[str, str] | None = None,
     |      body=None
     |  )
     |      Add the current content of the given sole ``graph`` argument
     |          as subgraph or return a context manager
     |          returning a new graph instance
     |          created with the given (``name``, ``comment``, etc.) arguments
     |          whose content is added as subgraph
     |          when leaving the context manager's ``with``-block.
     |
     |      Args:
     |          graph: An instance of the same kind
     |              (:class:`.Graph`, :class:`.Digraph`) as the current graph
     |              (sole argument in non-with-block use).
     |          name: Subgraph name (``with``-block use).
     |          comment: Subgraph comment (``with``-block use).
     |          graph_attr: Subgraph-level attribute-value mapping
     |              (``with``-block use).
     |          node_attr: Node-level attribute-value mapping
     |              (``with``-block use).
     |          edge_attr: Edge-level attribute-value mapping
     |              (``with``-block use).
     |          body: Verbatim lines to add to the subgraph ``body``
     |              (``with``-block use).
     |
     |      See the :ref:`usage examples in the User Guide <subgraphs-clusters>`.
     |
     |      When used as a context manager, the returned new graph instance
     |      uses ``strict=None`` and the parent graph's values
     |      for ``directory``, ``format``, ``engine``, and ``encoding`` by default.
     |
     |      Note:
     |          If the ``name`` of the subgraph begins with
     |          ``'cluster'`` (all lowercase)
     |          the layout engine will treat it as a special cluster subgraph.
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.rendering.Render:
     |
     |  render(
     |      self,
     |      filename: os.PathLike[str] | str | None = None,
     |      directory: os.PathLike[str] | str | None = None,
     |      view: bool = False,
     |      cleanup: bool = False,
     |      format: str | None = None,
     |      renderer: str | None = None,
     |      formatter: str | None = None,
     |      neato_no_op: bool | int | None = None,
     |      quiet: bool = False,
     |      quiet_view: bool = False,
     |      *,
     |      y_invert: bool = False,
     |      outfile: os.PathLike[str] | str | None = None,
     |      engine: str | None = None,
     |      raise_if_result_exists: bool = False,
     |      overwrite_source: bool = False
     |  ) -> str
     |      Save the source to file and render with the Graphviz engine.
     |
     |      Args:
     |          filename: Filename for saving the source
     |              (defaults to ``name`` + ``'.gv'``).s
     |          directory: (Sub)directory for source saving and rendering.
     |          view (bool): Open the rendered result
     |              with the default application.
     |          cleanup (bool): Delete the source file
     |              after successful rendering.
     |          format: The output format used for rendering
     |              (``'pdf'``, ``'png'``, etc.).
     |          renderer: The output renderer used for rendering
     |              (``'cairo'``, ``'gd'``, ...).
     |          formatter: The output formatter used for rendering
     |              (``'cairo'``, ``'gd'``, ...).
     |          neato_no_op: Neato layout engine no-op flag.
     |          quiet (bool): Suppress ``stderr`` output
     |              from the layout subprocess.
     |          quiet_view (bool): Suppress ``stderr`` output
     |              from the viewer process
     |              (implies ``view=True``, ineffective on Windows platform).
     |          y_invert: Invert y coordinates in the rendered output.
     |          outfile: Path for the rendered output file.
     |          engine: Layout engine for rendering
     |              (``'dot'``, ``'neato'``, ...).
     |          raise_if_result_exists: Raise :exc:`graphviz.FileExistsError`
     |              if the result file exists.
     |          overwrite_source: Allow ``dot`` to write to the file it reads from.
     |              Incompatible with ``raise_if_result_exists``.
     |
     |      Returns:
     |          The (possibly relative) path of the rendered file.
     |
     |      Raises:
     |          ValueError: If ``engine``, ``format``, ``renderer``, or ``formatter``
     |              are unknown.
     |          graphviz.RequiredArgumentError: If ``formatter`` is given
     |              but ``renderer`` is None.
     |          ValueError: If ``outfile`` is the same file as the source file
     |              unless ``overwite_source=True``.
     |          graphviz.ExecutableNotFound: If the Graphviz ``dot`` executable
     |              is not found.
     |          graphviz.CalledProcessError: If the returncode (exit status)
     |              of the rendering ``dot`` subprocess is non-zero.
     |          RuntimeError: If viewer opening is requested but not supported.
     |
     |      Example:
     |          >>> doctest_mark_exe()
     |          >>> import graphviz
     |          >>> dot = graphviz.Graph(name='spam', directory='doctest-output')
     |          >>> dot.render(format='png').replace('\', '/')
     |          'doctest-output/spam.gv.png'
     |          >>> dot.render(outfile='spam.svg').replace('\', '/')
     |          'doctest-output/spam.svg'
     |
     |      Note:
     |          The layout command is started from the directory of ``filepath``,
     |          so that references to external files
     |          (e.g. ``[image=images/camelot.png]``)
     |          can be given as paths relative to the DOT source file.
     |
     |  view(
     |      self,
     |      filename: os.PathLike[str] | str | None = None,
     |      directory: os.PathLike[str] | str | None = None,
     |      cleanup: bool = False,
     |      quiet: bool = False,
     |      quiet_view: bool = False
     |  ) -> str
     |      Save the source to file, open the rendered result in a viewer.
     |
     |      Convenience short-cut for running ``.render(view=True)``.
     |
     |      Args:
     |          filename: Filename for saving the source
     |              (defaults to ``name`` + ``'.gv'``).
     |          directory: (Sub)directory for source saving and rendering.
     |          cleanup (bool): Delete the source file after successful rendering.
     |          quiet (bool): Suppress ``stderr`` output from the layout subprocess.
     |          quiet_view (bool): Suppress ``stderr`` output
     |              from the viewer process (ineffective on Windows).
     |
     |      Returns:
     |          The (possibly relative) path of the rendered file.
     |
     |      Raises:
     |          graphviz.ExecutableNotFound: If the Graphviz executable
     |              is not found.
     |          graphviz.CalledProcessError: If the exit status is non-zero.
     |          RuntimeError: If opening the viewer is not supported.
     |
     |      Short-cut method for calling :meth:`.render` with ``view=True``.
     |
     |      Note:
     |          There is no option to wait for the application to close,
     |          and no way to retrieve the application's exit status.
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.saving.Save:
     |
     |  save(
     |      self,
     |      filename: os.PathLike[str] | str | None = None,
     |      directory: os.PathLike[str] | str | None = None,
     |      *,
     |      skip_existing: bool | None = False
     |  ) -> str
     |      Save the DOT source to file. Ensure the file ends with a newline.
     |
     |      Args:
     |          filename: Filename for saving the source (defaults to ``name`` + ``'.gv'``)
     |          directory: (Sub)directory for source saving and rendering.
     |          skip_existing: Skip write if file exists (default: ``False``).
     |
     |      Returns:
     |          The (possibly relative) path of the saved source file.
     |
     |  ----------------------------------------------------------------------
     |  Readonly properties inherited from graphviz.saving.Save:
     |
     |  filepath
     |      The target path for saving the DOT source file.
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from graphviz.saving.Save:
     |
     |  directory = ''
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.piping.Pipe:
     |
     |  pipe(
     |      self,
     |      format: str | None = None,
     |      renderer: str | None = None,
     |      formatter: str | None = None,
     |      neato_no_op: bool | int | None = None,
     |      quiet: bool = False,
     |      *,
     |      y_invert: bool = False,
     |      engine: str | None = None,
     |      encoding: str | None = None
     |  ) -> bytes | str
     |      Return the source piped through the Graphviz layout command.
     |
     |      Args:
     |          format: The output format used for rendering
     |              (``'pdf'``, ``'png'``, etc.).
     |          renderer: The output renderer used for rendering
     |              (``'cairo'``, ``'gd'``, ...).
     |          formatter: The output formatter used for rendering
     |              (``'cairo'``, ``'gd'``, ...).
     |          neato_no_op: Neato layout engine no-op flag.
     |          quiet (bool): Suppress ``stderr`` output
     |              from the layout subprocess.
     |          y_invert: Invert y coordinates in the rendered output.
     |          engine: Layout engine for rendering
     |              (``'dot'``, ``'neato'``, ...).
     |          encoding: Encoding for decoding the stdout.
     |
     |      Returns:
     |          Bytes or if encoding is given decoded string
     |              (stdout of the layout command).
     |
     |      Raises:
     |          ValueError: If ``engine``, ``format``, ``renderer``, or ``formatter``
     |              are unknown.
     |          graphviz.RequiredArgumentError: If ``formatter`` is given
     |              but ``renderer`` is None.
     |          graphviz.ExecutableNotFound: If the Graphviz ``dot`` executable
     |              is not found.
     |          graphviz.CalledProcessError: If the returncode (exit status)
     |              of the rendering ``dot`` subprocess is non-zero.
     |
     |      Example:
     |          >>> doctest_mark_exe()
     |          >>> import graphviz
     |          >>> source = 'graph { spam }'
     |          >>> graphviz.Source(source, format='svg').pipe()[:14]
     |          b'<?xml version='
     |          >>> graphviz.Source(source, format='svg').pipe(encoding='ascii')[:14]
     |          '<?xml version='
     |          >>> graphviz.Source(source, format='svg').pipe(encoding='utf-8')[:14]
     |          '<?xml version='
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.unflattening.Unflatten:
     |
     |  unflatten(
     |      self,
     |      stagger: int | None = None,
     |      fanout: bool = False,
     |      chain: int | None = None
     |  ) -> graphviz.Source
     |      Return a new :class:`.Source` instance with the source
     |          piped through the Graphviz *unflatten* preprocessor.
     |
     |      Args:
     |          stagger: Stagger the minimum length
     |              of leaf edges between 1 and this small integer.
     |          fanout: Fanout nodes with indegree = outdegree = 1
     |              when staggering (requires ``stagger``).
     |          chain: Form disconnected nodes into chains
     |              of up to this many nodes.
     |
     |      Returns:
     |          Prepocessed DOT source code (improved layout aspect ratio).
     |
     |      Raises:
     |          graphviz.RequiredArgumentError: If ``fanout`` is given
     |              but ``stagger`` is None.
     |          graphviz.ExecutableNotFound: If the Graphviz ``unflatten`` executable
     |              is not found.
     |          graphviz.CalledProcessError: If the returncode (exit status)
     |              of the unflattening 'unflatten' subprocess is non-zero.
     |
     |      See also:
     |          Upstream documentation:
     |          https://www.graphviz.org/pdf/unflatten.1.pdf
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from graphviz.encoding.Encoding:
     |
     |  encoding
     |      The encoding for the saved source file.
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.base.Base:
     |
     |  __str__(self) -> str
     |      The DOT source code as string.
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from graphviz.parameters.engines.Engine:
     |
     |  engine
     |      The layout engine used for rendering
     |      (``'dot'``, ``'neato'``, ...).
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from graphviz.parameters.formats.Format:
     |
     |  format
     |      The output format used for rendering
     |      (``'pdf'``, ``'png'``, ...).
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from graphviz.parameters.renderers.Renderer:
     |
     |  renderer
     |      The output renderer used for rendering
     |      (``'cairo'``, ``'gd'``, ...).
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from graphviz.parameters.formatters.Formatter:
     |
     |  formatter
     |      The output formatter used for rendering
     |      (``'cairo'``, ``'gd'``, ...).
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.copying.CopyBase:
     |
     |  copy(self)
     |      Return a copied instance of the object.
     |
     |      Returns:
     |          An independent copy of the current object.
    <BLANKLINE>


Source
""""""

Partially syntax-highlighted:
https://github.com/xflr6/graphviz/blob/master/docs/api.rst#source-1

.. doctest::

    >>> import graphviz
    >>> help(graphviz.Source)  # doctest: +NORMALIZE_WHITESPACE +SKIP
    Help on class Source in module graphviz.sources:
    <BLANKLINE>
    class Source(graphviz.rendering.Render,
                 graphviz.saving.Save,
                 graphviz.jupyter_integration.JupyterIntegration,
                 graphviz.piping.Pipe,
                 graphviz.unflattening.Unflatten)
     |  Source(
     |      source: str,
     |      filename: os.PathLike[str] | str | None = None,
     |      directory: os.PathLike[str] | str | None = None,
     |      format: str | None = None,
     |      engine: str | None = None,
     |      encoding: str | None = 'utf-8',
     |      *,
     |      renderer: str | None = None,
     |      formatter: str | None = None,
     |      loaded_from_path: os.PathLike[str] | None = None
     |  ) -> None
     |
     |  Verbatim DOT source code string to be rendered by Graphviz.
     |
     |  Args:
     |      source: The verbatim DOT source code string.
     |      filename: Filename for saving the source (defaults to ``'Source.gv'``).
     |      directory: (Sub)directory for source saving and rendering.
     |      format: Rendering output format (``'pdf'``, ``'png'``, ...).
     |      engine: Layout engine used (``'dot'``, ``'neato'``, ...).
     |      encoding: Encoding for saving the source.
     |
     |  Note:
     |      All parameters except ``source`` are optional. All of them
     |      can be changed under their corresponding attribute name
     |      after instance creation.
     |
     |  Method resolution order:
     |      Source
     |      graphviz.rendering.Render
     |      graphviz.saving.Save
     |      graphviz.jupyter_integration.JupyterIntegration
     |      graphviz.piping.Pipe
     |      graphviz.unflattening.Unflatten
     |      graphviz.encoding.Encoding
     |      graphviz.base.Base
     |      graphviz.base.LineIterable
     |      graphviz.backend.mixins.Render
     |      graphviz.backend.mixins.Pipe
     |      graphviz.parameters.mixins.Parameters
     |      graphviz.parameters.engines.Engine
     |      graphviz.parameters.formats.Format
     |      graphviz.parameters.renderers.Renderer
     |      graphviz.parameters.formatters.Formatter
     |      graphviz.parameters.base.ParameterBase
     |      graphviz.copying.CopyBase
     |      graphviz.backend.mixins.View
     |      graphviz.backend.mixins.Unflatten
     |      builtins.object
     |
     |  Methods defined here:
     |
     |  __init__(
     |      self,
     |      source: str,
     |      filename: os.PathLike[str] | str | None = None,
     |      directory: os.PathLike[str] | str | None = None,
     |      format: str | None = None,
     |      engine: str | None = None,
     |      encoding: str | None = 'utf-8',
     |      *,
     |      renderer: str | None = None,
     |      formatter: str | None = None,
     |      loaded_from_path: os.PathLike[str] | None = None
     |  ) -> None
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  __iter__(self) -> Iterator[str]
     |      Yield the DOT source code read from file line by line.
     |
     |      Yields: Line ending with a newline (``'\n'``).
     |
     |  save(
     |      self,
     |      filename: os.PathLike[str] | str | None = None,
     |      directory: os.PathLike[str] | str | None = None,
     |      *,
     |      skip_existing: bool | None = None
     |  ) -> str
     |      Save the DOT source to file. Ensure the file ends with a newline.
     |
     |      Args:
     |          filename: Filename for saving the source (defaults to ``name`` + ``'.gv'``)
     |          directory: (Sub)directory for source saving and rendering.
     |          skip_existing: Skip write if file exists (default: ``None``).
     |              By default skips if instance was loaded from the target path:
     |              ``.from_file(self.filepath)``.
     |
     |      Returns:
     |          The (possibly relative) path of the saved source file.
     |
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |
     |  from_file(
     |      filename: os.PathLike[str] | str,
     |      directory: os.PathLike[str] | str | None = None,
     |      format: str | None = None,
     |      engine: str | None = None,
     |      encoding: str | None = 'utf-8',
     |      renderer: str | None = None,
     |      formatter: str | None = None
     |  ) -> Source
     |      Return an instance with the source string read from the given file.
     |
     |      Args:
     |          filename: Filename for loading/saving the source.
     |          directory: (Sub)directory for source loading/saving and rendering.
     |          format: Rendering output format (``'pdf'``, ``'png'``, ...).
     |          engine: Layout command used (``'dot'``, ``'neato'``, ...).
     |          encoding: Encoding for loading/saving the source.
     |
     |  ----------------------------------------------------------------------
     |  Readonly properties defined here:
     |
     |  source
     |      The DOT source code as string.
     |
     |      Normalizes so that the string always ends in a final newline.
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.rendering.Render:
     |
     |  render(
     |      self,
     |      filename: os.PathLike[str] | str | None = None,
     |      directory: os.PathLike[str] | str | None = None,
     |      view: bool = False,
     |      cleanup: bool = False,
     |      format: str | None = None,
     |      renderer: str | None = None,
     |      formatter: str | None = None,
     |      neato_no_op: bool | int | None = None,
     |      quiet: bool = False,
     |      quiet_view: bool = False,
     |      *,
     |      y_invert: bool = False,
     |      outfile: os.PathLike[str] | str | None = None,
     |      engine: str | None = None,
     |      raise_if_result_exists: bool = False,
     |      overwrite_source: bool = False
     |  ) -> str
     |      Save the source to file and render with the Graphviz engine.
     |
     |      Args:
     |          filename: Filename for saving the source
     |              (defaults to ``name`` + ``'.gv'``).s
     |          directory: (Sub)directory for source saving and rendering.
     |          view (bool): Open the rendered result
     |              with the default application.
     |          cleanup (bool): Delete the source file
     |              after successful rendering.
     |          format: The output format used for rendering
     |              (``'pdf'``, ``'png'``, etc.).
     |          renderer: The output renderer used for rendering
     |              (``'cairo'``, ``'gd'``, ...).
     |          formatter: The output formatter used for rendering
     |              (``'cairo'``, ``'gd'``, ...).
     |          neato_no_op: Neato layout engine no-op flag.
     |          quiet (bool): Suppress ``stderr`` output
     |              from the layout subprocess.
     |          quiet_view (bool): Suppress ``stderr`` output
     |              from the viewer process
     |              (implies ``view=True``, ineffective on Windows platform).
     |          y_invert: Invert y coordinates in the rendered output.
     |          outfile: Path for the rendered output file.
     |          engine: Layout engine for rendering
     |              (``'dot'``, ``'neato'``, ...).
     |          raise_if_result_exists: Raise :exc:`graphviz.FileExistsError`
     |              if the result file exists.
     |          overwrite_source: Allow ``dot`` to write to the file it reads from.
     |              Incompatible with ``raise_if_result_exists``.
     |
     |      Returns:
     |          The (possibly relative) path of the rendered file.
     |
     |      Raises:
     |          ValueError: If ``engine``, ``format``, ``renderer``, or ``formatter``
     |              are unknown.
     |          graphviz.RequiredArgumentError: If ``formatter`` is given
     |              but ``renderer`` is None.
     |          ValueError: If ``outfile`` is the same file as the source file
     |              unless ``overwite_source=True``.
     |          graphviz.ExecutableNotFound: If the Graphviz ``dot`` executable
     |              is not found.
     |          graphviz.CalledProcessError: If the returncode (exit status)
     |              of the rendering ``dot`` subprocess is non-zero.
     |          RuntimeError: If viewer opening is requested but not supported.
     |
     |      Example:
     |          >>> doctest_mark_exe()
     |          >>> import graphviz
     |          >>> dot = graphviz.Graph(name='spam', directory='doctest-output')
     |          >>> dot.render(format='png').replace('\', '/')
     |          'doctest-output/spam.gv.png'
     |          >>> dot.render(outfile='spam.svg').replace('\', '/')
     |          'doctest-output/spam.svg'
     |
     |      Note:
     |          The layout command is started from the directory of ``filepath``,
     |          so that references to external files
     |          (e.g. ``[image=images/camelot.png]``)
     |          can be given as paths relative to the DOT source file.
     |
     |  view(
     |      self,
     |      filename: os.PathLike[str] | str | None = None,
     |      directory: os.PathLike[str] | str | None = None,
     |      cleanup: bool = False,
     |      quiet: bool = False,
     |      quiet_view: bool = False
     |  ) -> str
     |      Save the source to file, open the rendered result in a viewer.
     |
     |      Convenience short-cut for running ``.render(view=True)``.
     |
     |      Args:
     |          filename: Filename for saving the source
     |              (defaults to ``name`` + ``'.gv'``).
     |          directory: (Sub)directory for source saving and rendering.
     |          cleanup (bool): Delete the source file after successful rendering.
     |          quiet (bool): Suppress ``stderr`` output from the layout subprocess.
     |          quiet_view (bool): Suppress ``stderr`` output
     |              from the viewer process (ineffective on Windows).
     |
     |      Returns:
     |          The (possibly relative) path of the rendered file.
     |
     |      Raises:
     |          graphviz.ExecutableNotFound: If the Graphviz executable
     |              is not found.
     |          graphviz.CalledProcessError: If the exit status is non-zero.
     |          RuntimeError: If opening the viewer is not supported.
     |
     |      Short-cut method for calling :meth:`.render` with ``view=True``.
     |
     |      Note:
     |          There is no option to wait for the application to close,
     |          and no way to retrieve the application's exit status.
     |
     |  ----------------------------------------------------------------------
     |  Readonly properties inherited from graphviz.saving.Save:
     |
     |  filepath
     |      The target path for saving the DOT source file.
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from graphviz.saving.Save:
     |
     |  directory = ''
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.piping.Pipe:
     |
     |  pipe(
     |      self,
     |      format: str | None = None,
     |      renderer: str | None = None,
     |      formatter: str | None = None,
     |      neato_no_op: bool | int | None = None,
     |      quiet: bool = False,
     |      *,
     |      y_invert: bool = False,
     |      engine: str | None = None,
     |      encoding: str | None = None
     |  ) -> bytes | str
     |      Return the source piped through the Graphviz layout command.
     |
     |      Args:
     |          format: The output format used for rendering
     |              (``'pdf'``, ``'png'``, etc.).
     |          renderer: The output renderer used for rendering
     |              (``'cairo'``, ``'gd'``, ...).
     |          formatter: The output formatter used for rendering
     |              (``'cairo'``, ``'gd'``, ...).
     |          neato_no_op: Neato layout engine no-op flag.
     |          quiet (bool): Suppress ``stderr`` output
     |              from the layout subprocess.
     |          y_invert: Invert y coordinates in the rendered output.
     |          engine: Layout engine for rendering
     |              (``'dot'``, ``'neato'``, ...).
     |          encoding: Encoding for decoding the stdout.
     |
     |      Returns:
     |          Bytes or if encoding is given decoded string
     |              (stdout of the layout command).
     |
     |      Raises:
     |          ValueError: If ``engine``, ``format``, ``renderer``, or ``formatter``
     |              are unknown.
     |          graphviz.RequiredArgumentError: If ``formatter`` is given
     |              but ``renderer`` is None.
     |          graphviz.ExecutableNotFound: If the Graphviz ``dot`` executable
     |              is not found.
     |          graphviz.CalledProcessError: If the returncode (exit status)
     |              of the rendering ``dot`` subprocess is non-zero.
     |
     |      Example:
     |          >>> doctest_mark_exe()
     |          >>> import graphviz
     |          >>> source = 'graph { spam }'
     |          >>> graphviz.Source(source, format='svg').pipe()[:14]
     |          b'<?xml version='
     |          >>> graphviz.Source(source, format='svg').pipe(encoding='ascii')[:14]
     |          '<?xml version='
     |          >>> graphviz.Source(source, format='svg').pipe(encoding='utf-8')[:14]
     |          '<?xml version='
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.unflattening.Unflatten:
     |
     |  unflatten(
     |      self,
     |      stagger: int | None = None,
     |      fanout: bool = False,
     |      chain: int | None = None
     |  ) -> graphviz.Source
     |      Return a new :class:`.Source` instance with the source
     |          piped through the Graphviz *unflatten* preprocessor.
     |
     |      Args:
     |          stagger: Stagger the minimum length
     |              of leaf edges between 1 and this small integer.
     |          fanout: Fanout nodes with indegree = outdegree = 1
     |              when staggering (requires ``stagger``).
     |          chain: Form disconnected nodes into chains
     |              of up to this many nodes.
     |
     |      Returns:
     |          Prepocessed DOT source code (improved layout aspect ratio).
     |
     |      Raises:
     |          graphviz.RequiredArgumentError: If ``fanout`` is given
     |              but ``stagger`` is None.
     |          graphviz.ExecutableNotFound: If the Graphviz ``unflatten`` executable
     |              is not found.
     |          graphviz.CalledProcessError: If the returncode (exit status)
     |              of the unflattening 'unflatten' subprocess is non-zero.
     |
     |      See also:
     |          Upstream documentation:
     |          https://www.graphviz.org/pdf/unflatten.1.pdf
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from graphviz.encoding.Encoding:
     |
     |  encoding
     |      The encoding for the saved source file.
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.base.Base:
     |
     |  __str__(self) -> str
     |      The DOT source code as string.
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from graphviz.base.LineIterable:
     |
     |  __dict__
     |      dictionary for instance variables
     |
     |  __weakref__
     |      list of weak references to the object
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from graphviz.parameters.engines.Engine:
     |
     |  engine
     |      The layout engine used for rendering
     |      (``'dot'``, ``'neato'``, ...).
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from graphviz.parameters.formats.Format:
     |
     |  format
     |      The output format used for rendering
     |      (``'pdf'``, ``'png'``, ...).
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from graphviz.parameters.renderers.Renderer:
     |
     |  renderer
     |      The output renderer used for rendering
     |      (``'cairo'``, ``'gd'``, ...).
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from graphviz.parameters.formatters.Formatter:
     |
     |  formatter
     |      The output formatter used for rendering
     |      (``'cairo'``, ``'gd'``, ...).
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.copying.CopyBase:
     |
     |  copy(self)
     |      Return a copied instance of the object.
     |
     |      Returns:
     |          An independent copy of the current object.
    <BLANKLINE>

.. _api:

API Reference
=============

.. autosummary::
    :nosignatures:

    graphviz.Graph
    graphviz.Digraph
    graphviz.Source
    graphviz.render
    graphviz.pipe
    graphviz.pipe_string
    graphviz.pipe_lines
    graphviz.pipe_lines_string
    graphviz.unflatten
    graphviz.view

.. note::

    The two main classes :class:`.Graph` and :class:`.Digraph` (for creating
    `undirected` vs. `directed` graphs) have exactly the same API.
    Their division reflects the fact that both graph types cannot be mixed.


Graph
-----

.. autoclass:: graphviz.Graph
    :members:
        __iter__,
        source,
        node, edge, edges, attr, subgraph,
        format, engine, encoding,
        clear, copy, unflatten, pipe, save, render, view,
        directed


Digraph
-------

.. autoclass:: graphviz.Digraph
    :members:
        __iter__,
        source,
        node, edge, edges, attr, subgraph,
        format, engine, encoding,
        clear, copy, unflatten, pipe, save, render, view,
        directed


Source
------

.. autoclass:: graphviz.Source
    :members:
        __iter__,
        source,
        format, engine, encoding,
        copy, unflatten, pipe, save, render, view,
        from_file


Low-level functions
-------------------

The functions in this section are provided to work directly with existing
files and strings instead of using the object-oriented DOT creation methods
documented above.

.. autofunction:: graphviz.render
.. autofunction:: graphviz.pipe
.. autofunction:: graphviz.pipe_string
.. autofunction:: graphviz.pipe_lines
.. autofunction:: graphviz.pipe_lines_string
.. autofunction:: graphviz.unflatten
.. autofunction:: graphviz.view


Other
-----

.. autodata:: graphviz.ExecutableNotFound
   :annotation:

.. autodata:: graphviz.RequiredArgumentError
   :annotation:

.. autofunction:: graphviz.version

.. autofunction:: graphviz.escape

.. autofunction:: graphviz.nohtml

Manually maintained whitelists (see https://graphviz.gitlab.io/_pages/pdf/dot.1.pdf,
http://www.graphviz.org/doc/info/output.html, and ``dot -T:`` output):

.. autodata:: graphviz.ENGINES
   :annotation:

.. autodata:: graphviz.FORMATS
   :annotation:

.. autodata:: graphviz.RENDERERS
   :annotation:

.. autodata:: graphviz.FORMATTERS
   :annotation:

Names of upstream binaries:

.. autodata:: graphviz.backend.DOT_BINARY
   :annotation:

.. autodata:: graphviz.backend.UNFLATTEN_BINARY
   :annotation:


Online ``help()``
-----------------

Results of :func:`help` for :class:`.Graph`, :class:`.Digraph`,
and :class:`.Source` for reference:


Graph
"""""

.. code:: python

    >>> import graphviz
    >>> help(graphviz.Graph)  # doctest: +NORMALIZE_WHITESPACE +SKIP
    Help on class Graph in module graphviz.graphs:
    <BLANKLINE>
    class Graph(BaseGraph)
     |  Graph(name=None, comment=None,
              filename=None, directory=None,
              format=None, engine=None,
              encoding='utf-8',
              graph_attr=None, node_attr=None, edge_attr=None,
              body=None,
              strict=False)
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
     |      encoding: Encoding for saving the source.
     |      graph_attr: Mapping of ``(attribute, value)`` pairs for the graph.
     |      node_attr: Mapping of ``(attribute, value)`` pairs set for all nodes.
     |      edge_attr: Mapping of ``(attribute, value)`` pairs set for all edges.
     |      body: Iterable of verbatim lines to add to the graph ``body``.
     |      strict (bool): Rendering should merge multi-edges.
     |
     |  Note:
     |      All parameters are `optional` and can be changed under their
     |      corresponding attribute name after instance creation.
     |
     |  Method resolution order:
     |      Graph
     |      BaseGraph
     |      graphviz.dot.Dot
     |      graphviz.rendering.Rendering
     |      graphviz.rendering.Render
     |      graphviz.files.File
     |      graphviz.jupyter_integration.JupyterSvgIntegration
     |      graphviz.rendering.Pipe
     |      graphviz.unflattening.Unflatten
     |      graphviz.base.Base
     |      graphviz.base.SourceLineIterator
     |      graphviz.backend.Graphviz
     |      graphviz.encoding.Encoding
     |      graphviz.backend.View
     |      builtins.object
     |
     |  Readonly properties defined here:
     |
     |  directed
     |      ``False``
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from BaseGraph:
     |
     |  __init__(self, name=None, comment=None,
                 filename=None, directory=None,
                 format=None, engine=None,
                 encoding='utf-8',
                 graph_attr=None, node_attr=None, edge_attr=None,
                 body=None,
                 strict=False)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.dot.Dot:
     |
     |  __iter__(self, subgraph=False) -> Iterator[str]
     |      Yield the DOT source code line by line (as graph or subgraph).
     |
     |      Yields: Line ending with a newline (``'\n'``).
     |
     |  attr(self, kw=None, _attributes=None, **attrs)
     |      Add a general or graph/node/edge attribute statement.
     |
     |      Args:
     |          kw: Attributes target
     |              (``None`` or ``'graph'``, ``'node'``, ``'edge'``).
     |          attrs: Attributes to be set (must be strings, may be empty).
     |
     |      See the :ref:`usage examples in the User Guide <attributes>`.
     |
     |  clear(self, keep_attrs=False)
     |      Reset content to an empty body, clear graph/node/egde_attr mappings.
     |
     |      Args:
     |          keep_attrs (bool): preserve graph/node/egde_attr mappings
     |
     |  edge(self, tail_name, head_name, label=None, _attributes=None, **attrs)
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
     |          See :ref:`details in the User Guide <ports>`.
     |
     |  edges(self, tail_head_iter)
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
     |          See :ref:`details in the User Guide <ports>`.
     |
     |  node(self, name, label=None, _attributes=None, **attrs)
     |      Create a node.
     |
     |      Args:
     |          name: Unique identifier for the node inside the source.
     |          label: Caption to be displayed (defaults to the node ``name``).
     |          attrs: Any additional node attributes (must be strings).
     |
     |  subgraph(self, graph=None,
                 name=None, comment=None,
                 graph_attr=None, node_attr=None, edge_attr=None,
                 body=None)
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
     |      See the :ref:`usage examples in the User Guide <subgraphs>`.
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
     |  Data and other attributes inherited from graphviz.dot.Dot:
     |
     |  __annotations__ = {'_edge': <class 'str'>, '_edge_plain': <class 'str'...
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.rendering.Render:
     |
     |  render(self, filename=None, directory=None,
               view=False, cleanup=False,
               format=None, renderer=None, formatter=None,
               quiet=False, quiet_view=False)
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
     |          quiet (bool): Suppress ``stderr`` output
     |              from the layout subprocess.
     |          quiet_view (bool): Suppress ``stderr`` output
     |              from the viewer process
     |              (implies ``view=True``, ineffective on Windows).
     |
     |      Returns:
     |          The (possibly relative) path of the rendered file.
     |
     |      Raises:
     |          ValueError: If ``engine``, ``format``, ``renderer``, or ``formatter``
     |              are not known.
     |          graphviz.RequiredArgumentError: If ``formatter`` is given
     |              but ``renderer`` is None.
     |          graphviz.ExecutableNotFound: If the Graphviz 'dot' executable
     |              is not found.
     |          subprocess.CalledProcessError: If the returncode (exit status)
     |              of the rendering 'dot' subprocess is non-zero.
     |          RuntimeError: If viewer opening is requested but not supported.
     |
     |      Note:
     |          The layout command is started from the directory of ``filepath``,
     |          so that references to external files
     |          (e.g. ``[image=images/camelot.png]``)
     |          can be given as paths relative to the DOT source file.
     |
     |  view(self, filename=None, directory=None,
             cleanup=False, quiet=False, quiet_view=False)
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
     |          subprocess.CalledProcessError: If the exit status is non-zero.
     |          RuntimeError: If opening the viewer is not supported.
     |
     |      Short-cut method for calling :meth:`.render` with ``view=True``.
     |
     |      Note:
     |          There is no option to wait for the application to close,
     |          and no way to retrieve the application's exit status.
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.files.File:
     |
     |  save(self, filename=None, directory=None, *,
             skip_existing: Optional[bool] = False)
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
     |  Readonly properties inherited from graphviz.files.File:
     |
     |  filepath
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from graphviz.files.File:
     |
     |  directory = ''
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.rendering.Pipe:
     |
     |  pipe(self,
             format: Optional[str] = None,
             renderer: Optional[str] = None,
             formatter: Optional[str] = None,
             quiet: bool = False, *,
             encoding: Optional[str] = None) -> Union[bytes, str]
     |      Return the source piped through the Graphviz layout command.
     |
     |      Args:
     |          format: The output format used for rendering
     |              (``'pdf'``, ``'png'``, etc.).
     |          renderer: The output renderer used for rendering
     |              (``'cairo'``, ``'gd'``, ...).
     |          formatter: The output formatter used for rendering
     |              (``'cairo'``, ``'gd'``, ...).
     |          quiet (bool): Suppress ``stderr`` output
     |              from the layout subprocess.
     |          encoding: Encoding for decoding the stdout.
     |
     |      Returns:
     |          Bytes or if encoding is given decoded string
     |              (stdout of the layout command).
     |
     |      Raises:
     |          ValueError: If ``engine``, ``format``, ``renderer``, or ``formatter``
     |              are not known.
     |          graphviz.RequiredArgumentError: If ``formatter`` is given
     |              but ``renderer`` is None.
     |          graphviz.ExecutableNotFound: If the Graphviz 'dot' executable
     |              is not found.
     |          subprocess.CalledProcessError: If the returncode (exit status)
     |              of the rendering 'dot' subprocess is non-zero.
     |
     |      Example:
     |          >>> import graphviz
     |
     |          >>> source = 'graph { spam }'
     |
     |          >>> graphviz.Source(source, format='svg').pipe()[:14]
     |          b'<?xml version='
     |
     |          >>> graphviz.Source(source, format='svg').pipe(encoding='ascii')[:14]
     |          '<?xml version='
     |
     |          >>> graphviz.Source(source, format='svg').pipe(encoding='utf-8')[:14]
     |          '<?xml version='
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.unflattening.Unflatten:
     |
     |  unflatten(self, stagger=None, fanout=False, chain=None)
     |      Return a new :class:`.Source` instance with the source
     |          piped through the Graphviz *unflatten* preprocessor.
     |
     |      Args:
     |          stagger (int): Stagger the minimum length
     |              of leaf edges between 1 and this small integer.
     |          fanout (bool): Fanout nodes with indegree = outdegree = 1
     |              when staggering (requires ``stagger``).
     |          chain (int): Form disconnected nodes into chains
     |              of up to this many nodes.
     |
     |      Returns:
     |          Source: Prepocessed DOT source code (improved layout aspect ratio).
     |
     |      Raises:
     |          graphviz.RequiredArgumentError: If ``fanout`` is given
     |              but ``stagger`` is None.
     |          graphviz.ExecutableNotFound: If the Graphviz 'unflatten' executable
     |              is not found.
     |      subprocess.CalledProcessError: If the returncode (exit status)
     |          of the unflattening 'unflatten' subprocess is non-zero.
     |
     |      See also:
     |          https://www.graphviz.org/pdf/unflatten.1.pdf
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.base.Base:
     |
     |  copy(self)
     |      Return a copied instance of the object.
     |
     |      Returns:
     |          An independent copy of the current object.
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.base.SourceLineIterator:
     |
     |  __str__(self)
     |      The DOT source code as string.
     |
     |  ----------------------------------------------------------------------
     |  Readonly properties inherited from graphviz.base.SourceLineIterator:
     |
     |  source
     |      The generated DOT source code as string.
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from graphviz.base.SourceLineIterator:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from graphviz.backend.Graphviz:
     |
     |  engine
     |      The layout engine used for rendering (``'dot'``, ``'neato'``, ...).
     |
     |  format
     |      The output format used for rendering (``'pdf'``, ``'png'``, ...).
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from graphviz.encoding.Encoding:
     |
     |  encoding
     |      The encoding for the saved source file.
    <BLANKLINE>


Digraph
"""""""

.. code:: python

    >>> import graphviz
    >>> help(graphviz.Graph)  # doctest: +NORMALIZE_WHITESPACE +SKIP
    Help on class Graph in module graphviz.graphs:
    <BLANKLINE>
    class Graph(BaseGraph)
     |  Graph(name=None, comment=None,
              filename=None, directory=None,
              format=None, engine=None,
              encoding='utf-8',
              graph_attr=None, node_attr=None, edge_attr=None,
              body=None,
              strict=False)
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
     |      encoding: Encoding for saving the source.
     |      graph_attr: Mapping of ``(attribute, value)`` pairs for the graph.
     |      node_attr: Mapping of ``(attribute, value)`` pairs set for all nodes.
     |      edge_attr: Mapping of ``(attribute, value)`` pairs set for all edges.
     |      body: Iterable of verbatim lines to add to the graph ``body``.
     |      strict (bool): Rendering should merge multi-edges.
     |
     |  Note:
     |      All parameters are `optional` and can be changed under their
     |      corresponding attribute name after instance creation.
     |
     |  Method resolution order:
     |      Graph
     |      BaseGraph
     |      graphviz.dot.Dot
     |      graphviz.rendering.Rendering
     |      graphviz.rendering.Render
     |      graphviz.files.File
     |      graphviz.jupyter_integration.JupyterSvgIntegration
     |      graphviz.rendering.Pipe
     |      graphviz.unflattening.Unflatten
     |      graphviz.base.Base
     |      graphviz.base.SourceLineIterator
     |      graphviz.backend.Graphviz
     |      graphviz.encoding.Encoding
     |      graphviz.backend.View
     |      builtins.object
     |
     |  Readonly properties defined here:
     |
     |  directed
     |      ``False``
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from BaseGraph:
     |
     |  __init__(self, name=None, comment=None,
                 filename=None, directory=None,
                 format=None, engine=None,
                 encoding='utf-8',
                 graph_attr=None, node_attr=None, edge_attr=None,
                 body=None,
                 strict=False)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.dot.Dot:
     |
     |  __iter__(self, subgraph=False) -> Iterator[str]
     |      Yield the DOT source code line by line (as graph or subgraph).
     |
     |      Yields: Line ending with a newline (``'\n'``).
     |
     |  attr(self, kw=None, _attributes=None, **attrs)
     |      Add a general or graph/node/edge attribute statement.
     |
     |      Args:
     |          kw: Attributes target
     |              (``None`` or ``'graph'``, ``'node'``, ``'edge'``).
     |          attrs: Attributes to be set (must be strings, may be empty).
     |
     |      See the :ref:`usage examples in the User Guide <attributes>`.
     |
     |  clear(self, keep_attrs=False)
     |      Reset content to an empty body, clear graph/node/egde_attr mappings.
     |
     |      Args:
     |          keep_attrs (bool): preserve graph/node/egde_attr mappings
     |
     |  edge(self, tail_name, head_name, label=None, _attributes=None, **attrs)
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
     |          See :ref:`details in the User Guide <ports>`.
     |
     |  edges(self, tail_head_iter)
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
     |          See :ref:`details in the User Guide <ports>`.
     |
     |  node(self, name, label=None, _attributes=None, **attrs)
     |      Create a node.
     |
     |      Args:
     |          name: Unique identifier for the node inside the source.
     |          label: Caption to be displayed (defaults to the node ``name``).
     |          attrs: Any additional node attributes (must be strings).
     |
     |  subgraph(self, graph=None,
                 name=None, comment=None,
                 graph_attr=None, node_attr=None, edge_attr=None,
                 body=None)
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
     |      See the :ref:`usage examples in the User Guide <subgraphs>`.
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
     |  Data and other attributes inherited from graphviz.dot.Dot:
     |
     |  __annotations__ = {'_edge': <class 'str'>, '_edge_plain': <class 'str'...
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.rendering.Render:
     |
     |  render(self, filename=None, directory=None,
               view=False, cleanup=False,
               format=None, renderer=None, formatter=None,
               quiet=False, quiet_view=False)
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
     |          quiet (bool): Suppress ``stderr`` output
     |              from the layout subprocess.
     |          quiet_view (bool): Suppress ``stderr`` output
     |              from the viewer process
     |              (implies ``view=True``, ineffective on Windows).
     |
     |      Returns:
     |          The (possibly relative) path of the rendered file.
     |
     |      Raises:
     |          ValueError: If ``engine``, ``format``, ``renderer``, or ``formatter``
     |              are not known.
     |          graphviz.RequiredArgumentError: If ``formatter`` is given
     |              but ``renderer`` is None.
     |          graphviz.ExecutableNotFound: If the Graphviz 'dot' executable
     |              is not found.
     |          subprocess.CalledProcessError: If the returncode (exit status)
     |              of the rendering 'dot' subprocess is non-zero.
     |          RuntimeError: If viewer opening is requested but not supported.
     |
     |      Note:
     |          The layout command is started from the directory of ``filepath``,
     |          so that references to external files
     |          (e.g. ``[image=images/camelot.png]``)
     |          can be given as paths relative to the DOT source file.
     |
     |  view(self, filename=None, directory=None,
             cleanup=False, quiet=False, quiet_view=False)
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
     |          subprocess.CalledProcessError: If the exit status is non-zero.
     |          RuntimeError: If opening the viewer is not supported.
     |
     |      Short-cut method for calling :meth:`.render` with ``view=True``.
     |
     |      Note:
     |          There is no option to wait for the application to close,
     |          and no way to retrieve the application's exit status.
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.files.File:
     |
     |  save(self, filename=None, directory=None, *, skip_existing: Optional[bool] = False)
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
     |  Readonly properties inherited from graphviz.files.File:
     |
     |  filepath
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from graphviz.files.File:
     |
     |  directory = ''
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.rendering.Pipe:
     |
     |  pipe(self,
             format: Optional[str] = None,
             renderer: Optional[str] = None,
             formatter: Optional[str] = None,
             quiet: bool = False, *,
             encoding: Optional[str] = None) -> Union[bytes, str]
     |      Return the source piped through the Graphviz layout command.
     |
     |      Args:
     |          format: The output format used for rendering
     |              (``'pdf'``, ``'png'``, etc.).
     |          renderer: The output renderer used for rendering
     |              (``'cairo'``, ``'gd'``, ...).
     |          formatter: The output formatter used for rendering
     |              (``'cairo'``, ``'gd'``, ...).
     |          quiet (bool): Suppress ``stderr`` output
     |              from the layout subprocess.
     |          encoding: Encoding for decoding the stdout.
     |
     |      Returns:
     |          Bytes or if encoding is given decoded string
     |              (stdout of the layout command).
     |
     |      Raises:
     |          ValueError: If ``engine``, ``format``, ``renderer``, or ``formatter``
     |              are not known.
     |          graphviz.RequiredArgumentError: If ``formatter`` is given
     |              but ``renderer`` is None.
     |          graphviz.ExecutableNotFound: If the Graphviz 'dot' executable
     |              is not found.
     |          subprocess.CalledProcessError: If the returncode (exit status)
     |              of the rendering 'dot' subprocess is non-zero.
     |
     |      Example:
     |          >>> import graphviz
     |
     |          >>> source = 'graph { spam }'
     |
     |          >>> graphviz.Source(source, format='svg').pipe()[:14]
     |          b'<?xml version='
     |
     |          >>> graphviz.Source(source, format='svg').pipe(encoding='ascii')[:14]
     |          '<?xml version='
     |
     |          >>> graphviz.Source(source, format='svg').pipe(encoding='utf-8')[:14]
     |          '<?xml version='
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.unflattening.Unflatten:
     |
     |  unflatten(self, stagger=None, fanout=False, chain=None)
     |      Return a new :class:`.Source` instance with the source
     |          piped through the Graphviz *unflatten* preprocessor.
     |
     |      Args:
     |          stagger (int): Stagger the minimum length
     |              of leaf edges between 1 and this small integer.
     |          fanout (bool): Fanout nodes with indegree = outdegree = 1
     |              when staggering (requires ``stagger``).
     |          chain (int): Form disconnected nodes into chains
     |              of up to this many nodes.
     |
     |      Returns:
     |          Source: Prepocessed DOT source code (improved layout aspect ratio).
     |
     |      Raises:
     |          graphviz.RequiredArgumentError: If ``fanout`` is given
     |              but ``stagger`` is None.
     |          graphviz.ExecutableNotFound: If the Graphviz 'unflatten' executable
     |              is not found.
     |      subprocess.CalledProcessError: If the returncode (exit status)
     |          of the unflattening 'unflatten' subprocess is non-zero.
     |
     |      See also:
     |          https://www.graphviz.org/pdf/unflatten.1.pdf
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.base.Base:
     |
     |  copy(self)
     |      Return a copied instance of the object.
     |
     |      Returns:
     |          An independent copy of the current object.
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.base.SourceLineIterator:
     |
     |  __str__(self)
     |      The DOT source code as string.
     |
     |  ----------------------------------------------------------------------
     |  Readonly properties inherited from graphviz.base.SourceLineIterator:
     |
     |  source
     |      The generated DOT source code as string.
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from graphviz.base.SourceLineIterator:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from graphviz.backend.Graphviz:
     |
     |  engine
     |      The layout engine used for rendering (``'dot'``, ``'neato'``, ...).
     |
     |  format
     |      The output format used for rendering (``'pdf'``, ``'png'``, ...).
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from graphviz.encoding.Encoding:
     |
     |  encoding
     |      The encoding for the saved source file.
    <BLANKLINE>


Source
""""""

.. code:: python

    >>> import graphviz
    >>> help(graphviz.Source)  # doctest: +NORMALIZE_WHITESPACE +SKIP
    Help on class Source in module graphviz.sources:
    <BLANKLINE>
    class Source(graphviz.rendering.Rendering, graphviz.files.File,
                 graphviz.jupyter_integration.JupyterSvgIntegration,
                 graphviz.base.Base)
     |  Source(source,
               filename=None, directory=None,
               format=None, engine=None,
               encoding='utf-8', *,
               loaded_from_path: Optional[os.PathLike] = None)
     |
     |  Verbatim DOT source code string to be rendered by Graphviz.
     |
     |  Args:
     |      source: The verbatim DOT source code string.
     |      filename: Filename for saving the source (defaults to ``'Source.gv'``).
     |      directory: (Sub)directory for source saving and rendering.
     |      format: Rendering output format (``'pdf'``, ``'png'``, ...).
     |      engine: Layout command used (``'dot'``, ``'neato'``, ...).
     |      encoding: Encoding for saving the source.
     |
     |  Note:
     |      All parameters except ``source`` are optional. All of them
     |      can be changed under their corresponding attribute name
     |      after instance creation.
     |
     |  Method resolution order:
     |      Source
     |      graphviz.rendering.Rendering
     |      graphviz.rendering.Render
     |      graphviz.files.File
     |      graphviz.jupyter_integration.JupyterSvgIntegration
     |      graphviz.rendering.Pipe
     |      graphviz.unflattening.Unflatten
     |      graphviz.base.Base
     |      graphviz.base.SourceLineIterator
     |      graphviz.backend.Graphviz
     |      graphviz.encoding.Encoding
     |      graphviz.backend.View
     |      builtins.object
     |
     |  Methods defined here:
     |
     |  __init__(self, source,
                 filename=None, directory=None,
                 format=None, engine=None,
                 encoding='utf-8', *,
                 loaded_from_path: Optional[os.PathLike] = None)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  __iter__(self)
     |      Yield the DOT source code read from file line by line.
     |
     |      Yields: Line ending with a newline (``'\n'``).
     |
     |  save(self, filename=None, directory=None, *, skip_existing: Optional[bool] = None)
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
     |  from_file(filename, directory=None,
                  format=None, engine=None,
                  encoding='utf-8') from builtins.type
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
     |      The DOT source code as string (read from file).
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.rendering.Render:
     |
     |  render(self, filename=None, directory=None,
               view=False, cleanup=False,
               format=None, renderer=None, formatter=None,
               quiet=False, quiet_view=False)
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
     |          quiet (bool): Suppress ``stderr`` output
     |              from the layout subprocess.
     |          quiet_view (bool): Suppress ``stderr`` output
     |              from the viewer process
     |              (implies ``view=True``, ineffective on Windows).
     |
     |      Returns:
     |          The (possibly relative) path of the rendered file.
     |
     |      Raises:
     |          ValueError: If ``engine``, ``format``, ``renderer``, or ``formatter``
     |              are not known.
     |          graphviz.RequiredArgumentError: If ``formatter`` is given
     |              but ``renderer`` is None.
     |          graphviz.ExecutableNotFound: If the Graphviz 'dot' executable
     |              is not found.
     |          subprocess.CalledProcessError: If the returncode (exit status)
     |              of the rendering 'dot' subprocess is non-zero.
     |          RuntimeError: If viewer opening is requested but not supported.
     |
     |      Note:
     |          The layout command is started from the directory of ``filepath``,
     |          so that references to external files
     |          (e.g. ``[image=images/camelot.png]``)
     |          can be given as paths relative to the DOT source file.
     |
     |  view(self, filename=None, directory=None,
             cleanup=False, quiet=False, quiet_view=False)
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
     |          subprocess.CalledProcessError: If the exit status is non-zero.
     |          RuntimeError: If opening the viewer is not supported.
     |
     |      Short-cut method for calling :meth:`.render` with ``view=True``.
     |
     |      Note:
     |          There is no option to wait for the application to close,
     |          and no way to retrieve the application's exit status.
     |
     |  ----------------------------------------------------------------------
     |  Readonly properties inherited from graphviz.files.File:
     |
     |  filepath
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from graphviz.files.File:
     |
     |  directory = ''
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.rendering.Pipe:
     |
     |  pipe(self,
             format: Optional[str] = None,
             renderer: Optional[str] = None,
             formatter: Optional[str] = None,
             quiet: bool = False, *,
             encoding: Optional[str] = None) -> Union[bytes, str]
     |      Return the source piped through the Graphviz layout command.
     |
     |      Args:
     |          format: The output format used for rendering
     |              (``'pdf'``, ``'png'``, etc.).
     |          renderer: The output renderer used for rendering
     |              (``'cairo'``, ``'gd'``, ...).
     |          formatter: The output formatter used for rendering
     |              (``'cairo'``, ``'gd'``, ...).
     |          quiet (bool): Suppress ``stderr`` output
     |              from the layout subprocess.
     |          encoding: Encoding for decoding the stdout.
     |
     |      Returns:
     |          Bytes or if encoding is given decoded string
     |              (stdout of the layout command).
     |
     |      Raises:
     |          ValueError: If ``engine``, ``format``, ``renderer``, or ``formatter``
     |              are not known.
     |          graphviz.RequiredArgumentError: If ``formatter`` is given
     |              but ``renderer`` is None.
     |          graphviz.ExecutableNotFound: If the Graphviz 'dot' executable
     |              is not found.
     |          subprocess.CalledProcessError: If the returncode (exit status)
     |              of the rendering 'dot' subprocess is non-zero.
     |
     |      Example:
     |          >>> import graphviz
     |
     |          >>> source = 'graph { spam }'
     |
     |          >>> graphviz.Source(source, format='svg').pipe()[:14]
     |          b'<?xml version='
     |
     |          >>> graphviz.Source(source, format='svg').pipe(encoding='ascii')[:14]
     |          '<?xml version='
     |
     |          >>> graphviz.Source(source, format='svg').pipe(encoding='utf-8')[:14]
     |          '<?xml version='
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.unflattening.Unflatten:
     |
     |  unflatten(self, stagger=None, fanout=False, chain=None)
     |      Return a new :class:`.Source` instance with the source
     |          piped through the Graphviz *unflatten* preprocessor.
     |
     |      Args:
     |          stagger (int): Stagger the minimum length
     |              of leaf edges between 1 and this small integer.
     |          fanout (bool): Fanout nodes with indegree = outdegree = 1
     |              when staggering (requires ``stagger``).
     |          chain (int): Form disconnected nodes into chains
     |              of up to this many nodes.
     |
     |      Returns:
     |          Source: Prepocessed DOT source code (improved layout aspect ratio).
     |
     |      Raises:
     |          graphviz.RequiredArgumentError: If ``fanout`` is given
     |              but ``stagger`` is None.
     |          graphviz.ExecutableNotFound: If the Graphviz 'unflatten' executable
     |              is not found.
     |      subprocess.CalledProcessError: If the returncode (exit status)
     |          of the unflattening 'unflatten' subprocess is non-zero.
     |
     |      See also:
     |          https://www.graphviz.org/pdf/unflatten.1.pdf
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.base.Base:
     |
     |  copy(self)
     |      Return a copied instance of the object.
     |
     |      Returns:
     |          An independent copy of the current object.
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from graphviz.base.SourceLineIterator:
     |
     |  __str__(self)
     |      The DOT source code as string.
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from graphviz.base.SourceLineIterator:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from graphviz.backend.Graphviz:
     |
     |  engine
     |      The layout engine used for rendering (``'dot'``, ``'neato'``, ...).
     |
     |  format
     |      The output format used for rendering (``'pdf'``, ``'png'``, ...).
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from graphviz.encoding.Encoding:
     |
     |  encoding
     |      The encoding for the saved source file.
    <BLANKLINE>

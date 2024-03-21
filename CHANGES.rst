Changelog
=========


Version 0.20.3
--------------

Revert improvements to the internal ``tools.deprecate_positional_args()``
decorator that caused false positive
``PendingDeprecationWarning: The signature of ... will be reduced``
warnings that have been misinterpreted in the 0.20.2 release process.


Version 0.20.2
--------------

Drop Python 3.7 support (end of life 27 Jun 2023).

Tag Python 3.11 and 3.12 support.

Add caveat about ``labe`` escaping/quoting to ``.node()`` and ``.render()``
API docs.

Document that ``doctest_skip_exe()`` lines in doctest should be ignored.

Improve internal ``tools.deprecate_positional_args()`` decorator
and fix incorect test assertion.

Update GitHub actions.

Pin ``pytest`` test dependency to ``<8.1`` as a workaround
for ``import file mismatch error`` related to ``conftest.py`` files,
in ``pytest 8.1.1``, see https://github.com/pytest-dev/pytest/issues/12123.


Version 0.20.1
--------------

Fix documentation building: upgrade to Sphinx 5.0.

Fix broken user guide links in API documentation.


Version 0.20
------------

Add keyword-only ``neato_no_op`` argument to ``.render()``, ``.pipe()``,
and stand-alone ``graphviz.render()`` and ``graphviz.pipe()``.

When building a ``Graph`` or ``Digraph``,
warn about an expected DOT syntax error in rendering
when passing a string that ends with an odd number of backslashes
(e.g. invalid ``dot.node('spam', label='\\')``
instead of correct ``..., label=r'\\'``
for a node labled as a backslash).

Increase visibility of ``graphviz.escape()`` in the documentation.


Version 0.19.2
--------------

Drop Python 3.6 support (end of life 23 Dec 2021).

Fix ``ExecutableNotFound`` and ``CalledProcessError`` in ``graphviz.__all__``.

Better document ``0.18`` change of behaviour for the ``body`` argument/attribute
(lines need to include their final newline).


Version 0.19.1
--------------

Fix undecoded ``CalledProcessError.stdout`` and ``.stderr`` when ``.pipe()`` call
with an ``encoding`` different from ``self.encoding`` fails.

Fix missing project root ``conftest.py`` in source distribution.

Extend ``examples/graphviz-escapes.ipynb``.

Improve test coverage.

Increase build scripts verbosity.


Version 0.19
------------

Add ``PendingDeprecationWarning`` to calls using positional arguments
that will be **deprecated in a later version**.
The future API will allow from one to three positional arguments
depending on the method or function.
Keyword-only arguments where not around when this library was created.
This signals dependents and in general users to start updating
or pinning to the wanted version (or range).
Crucially, this helps new users with a safer API
that allows to avoid some common mistakes.
Warnings reported in tests.

Add keyword-only ``outfile`` argument to ``.render()``
and stand-alone ``graphviz.render()``.
Allows to override the rendered output file name:
``.render(filename='spam.gv', outfile='spam.pdf')``
Allows to derive the ``format`` and the ``filename``
from the rendered ``outfile`` name:
``.render(outfile='spam.svg')``
Tries to infer default ``format`` from the ``outfile`` suffix.
You can override by setting ``format`` explicitly.
Warns with a ``graphviz.FormatSuffixMismatchWarning``
if there is a mismatch between given ``format``
and the inferred format from ``outfile`` suffix.
Warns with a ``graphviz.UnknownSuffixWarning``
if ``format`` is given and ``outfile`` uses a suffix
that cannot be mapped to a supported format.

Add ``graphviz.set_jupyter_format()`` to set the output ``format``
used by the Jupyter visualization of ``graphviz.Graph``, ``graphviz.Digraph``,
and ``graphviz.Source`` (supported formats: ``'svg'``, ``'png'``, ``'jpeg'``).
Replace ``_repr_svg_()`` internally with ``_repr_mimebundle_(include, exclude)``
returning a mimebundle ``{'image/svg+xml', '<?xml version=...'}`` by default.
Adds support for ``IPython.display.display_png()``.
Adds support for ``IPython.display.display_jpeg()``.
PR `#150 <https://github.com/xflr6/graphviz/pull/150>`_ Christoph Boeddeker.

Add keyword-only ``raise_if_result_exists`` argument to ``.render()``
and stand-alone ``graphviz.render()``.
Raises ``graphviz.FileExistsError`` if the rendered file already exists.

Add support to for ``.render()`` and stand-alone ``.render()``
to overwrite the input source file with the rendered output
when using the ``outfile`` keyword-only argument.
This probably only makes sense for text-based Graphviz formats
such as ``dot`` or ``plain``.
You need to specify ``overwrite_filepath=True`` to enable this.

Add ``graphviz.CalledProcessError`` derived from ``subprocess.CalledProcessError``
so users can choose either one in their excepts.

Add ``graphviz.FileExistsError`` derived from ``FileExistsError``
so users can choose either one in their excepts.

Add ``--only-exe`` flag to ``run-tests.py`` (overrides ``--skip-exe``).

Add ``--no-open`` and ``--open`` flags to ``build-docs.py``.

Add ``lint-code.py`` and use in build job.

Increase doctest coverage.

Extend type annotations.
Accept path-like objects for ``filename``, ``directory``, and ``filepath``.

Extend and improve documentation.

Improve build tests.


Version 0.18.2
--------------

Fix ``filepath`` fallback to ``name`` of ``Graph/Digraph`` for 
when filepath is not present (restore
``graphviz.Graph('spam').filename == 'spam.gv'`` broken in 0.18).

Fix unintended API docs reference to internal ``backend`` name for 
``DOT_BINARY`` and ``UNFLATTEN_BINARY``. Moved to public API
as ``graphviz.DOT_BINARY`` and ``graphviz.UNFLATTEN_BINARY``.

Fix broken documentation links.

Docs: re-render most SVGs and notebooks with upstream Graphviz 2.49.3.


Version 0.18.1
--------------

Fix ``TypeError: argument of type 'WindowsPath' is not iterable``
on Windows platform under Python 3.6 and 3.7
(work around https://bugs.python.org/issue41649).

Update outdated examples source links.

Improve mode structure and separation of concerns.

Improve test structure and coverage.

Improve output of ``try-examples.py``.
Add exit status for CI. Disable `view()`.

Add ``build-docs.py`` script for development.

Add ``update-help.py`` script for development.


Version 0.18
------------

Change of beaviour:
File endings are now normalized so that all DOT source outputs
end with a final newline (Unix convention, simplifies concatenation).
This includes DOT source files written by ``.render()``, ``.view()``,
or ``.save()`` as well was ``.source`` generated or loaded from ``Source``
(or ``Source.from_file()``).

Change of behaviour:
``Source`` instances created by ``Source.from_file()``
no nonger write the content read into ``.source`` back into the file.
Use ``.save(skip_existing=False)`` before calling ``.render()`` or ``.view()``
if you want to overwrite the file to produce the previous (less safe) behaviour.

Change of undocumented behaviour:
When iterating over a ``Graph``, ``Digraph``, or ``Source`` instance,
the yielded lines now include a final newline (``'\n'``).
This mimics iteration over ``file`` object lines in text mode.

Change of behaviour:
When adding custom DOT statements using the ``body`` argument
of ``Graph`` or ``Digraph`` or appending to the ``body`` attribute
of an instance, the lines now need to include their final newline (``'\n'``).

When passing invalid parameters such as unknown ``engine``, ``format``, etc.,
``.render()`` now raises early before writing the file.
Call ``.save()`` explicitly to produce the previous (less safe) behaviour.

Add optional keyword-only ``encoding`` argument to ``pipe()``.
Returns the decoded stdout from the rendering process
(e.g. ``format='svg'``).
Delegates encoding/decoding to ``subprocess`` in the common case
(input and output encoding are the same, e.g. default ``encoding='utf-8'``).
Used by the Jupyter notebook integration.

Add optional keyword-only ``engine`` argument to ``.pipe()`` and ``.render()``.

Add optional keyword-only ``renderer`` and ``formatter`` arguments to ``Graph()``,
``Digraph()``, ``Source()`` and ``Source.from_file()``
to set default renderers and formatters (similar to ``format``).
Used by ``.pipe()``, ``.render()``, and ``.view()`` if not given as method-argument.

Add ``pipe_string()``, ``pipe_lines()``, and ``pipe_lines_string()``.
Pipe ``input_string``, return ``string``.
Pipe ``input_lines`` incrementally, return ``bytes``.
Pipe ``input_lines`` incrementally, return ``string``.

Add ``set_default_engine()`` and ``set_default_format()``

Add ``DOT_BINARY`` and ``UNFLATTEN_BINARY``.

Restructure the internal class hierarchy using multiple-inheritance
with cooperative ``super()`` calling:
``Graph`` now inherits both from ``Dot`` and from ``Render``,
and both of them inherit from ``Base`` which defines their common interface:
Lines of DOT source code that ``Dot`` generates (also ``Source``)
and rendering iterates over.
This might break some undocumented use of subclassing and require adatation
(e.g. if the methods don't use cooperative ``super()`` calling convention
or if the MRO has conflicts, supposedly rare).

Improve test separation. Improve test coverage of running the tests with ``--skip-exe``.

Add ``pytype`` checking and ``flake8`` to build workflow.

Extend type annotations.

Add https://mybinder.org config with head development environment.
Add launch badge to code repository.

Improve documentation and examples.

Add development docs.

Document release process.


Version 0.17
------------

Drop Python 2 support. Tag Python 3.10 support.

Migrate CI to GitHub actions. Add ``pypy3`` to matrix.

Tests: implement ``--skip-exe`` via custom ``pytest`` marker.

Documentation: point Anaconda users to ``conda-forge/python-graphviz``.

Move type hints from docstrings to type annotations. Improve doctests.

Examples: standardize import convention and modernize.

Re-render example notebooks with Graphviz 2.46.1.


Version 0.16
------------

Add ``.unflatten()`` method to ``Graph``, ``Digraph``, and ``Source``. Add
standalone ``unflatten()``.

Make ``Source.__str__()`` return the ``.source`` instead of the ``repr()``
(like ``Graph`` and ``Digraph``).

Render with ``dot -K<engine> ...`` instead of ``<engine> ...`` internally
(work around `upstream issue
<https://gitlab.com/graphviz/graphviz/-/issues/1753>`_).

Add documentation hint to archived upstream version for Windows.

Re-render most documentation graphs with Graphviz 2.44.1.


Version 0.15
------------

``Graph`` and ``Digraph`` instances created via the context-manager
returned by ``subgraph()`` now (re)use
``directory``, ``format``, ``engine``, and ``encoding`` from the parent
instead of using defaults (behavioral change).
Note that these attributes are only relevant
when rendering the subgraph independently (i.e. as a stand-alone graph)
from within the ``with``-block, which was previously underdocumented.
PR `#116 <https://github.com/xflr6/graphviz/pull/116>`_ BMaxV.
To reflect that the DOT language does not allow subgraph statements
to specify ``strict``
(i.e. no way to override the setting of the containing graph),
instances created via the context-manager are now ``strict=None`` instead of ``False``
(so they continue to render stand-alone as non-strict by default).

Drop Python 3.5 support and tag Python 3.9 support.

Add documentation link to new upstream installation procedure for Windows.


Version 0.14.2
--------------

Adapt ``graphviz.version()`` to support the Graphviz Release version entry
format introduced with ``2.44.2`` (``version()`` is needed to run the tests).


Version 0.14.1
--------------

Document the colon-separated ``node[:port[:compass]]`` format used for
``tail`` and ``head`` points in the ``edge()``- and ``edges()``-methods.
PR `#101 <https://github.com/xflr6/graphviz/pull/101>`_ Michał Góral.


Version 0.14
------------

Improve handling of escaped quotes (``\"``). Different from other layout engine
escapes sequences such as ``\l`` and ``\N`` (which are passed on as is by
default), there is no use case for backslash-escaping a literal quote character
because escaping of quotes is done by this library. Therefore, a
backslash-escaped quote (e.g. in ``label='\\"'``) is now treated the same as a
plain unescaped quote, i.e. both ``label='"'`` and ``label='\\"'`` produce
the same DOT source ``[label="\""]`` (a label that renders as a literal quote).
Before this change, use of ``'\\"'`` could break the quoting mechanism creating
invalid or unintended DOT, possibly leading to syntax errors from the rendering
process.

Add notebook section to documentation.

Add ``sphinx.ext.viewcode`` to docs (note that this currently lacks links for
methods, so that not all of the code is linked; use the source repo for reading
on).

Improve test and doc building config.


Version 0.13.2
--------------

Fix missing support for four-part versions in ``graphviz.version()``.



Version 0.13.1
--------------

Tag Python 3.8 support.

Fix quoting for non-ASCII numerals.


Version 0.13
------------

Add explicit support for layout engine escape sequences such as ``\l`` and
``\N``. These already worked implicitly before but where broken by backslash
escaping in ``0.12``, which is reverted by this release. Escaping now resembles
the stdlib ``re`` module: literal backslashes need to be escaped (doubled),
which is most conveniently done by using raw string literals for strings that
use escape sequences (including escaped backslashes), e.g. ``label=r'\\'``.

Add ``escape()`` function (resembling ``re.escape()``) for disabling all
meta-characters in a string for rendering.

Use ``logging`` in example notebook, add notebooks demonstrating layout engines
and escape sequence usage, improve tests with parametrization.


Version 0.12
------------

Fix missing escaping of backslashes, e.g. in labels (pull request DNGros).

Add ``quiet`` argument to standalone ``view()`` function, and ``quiet_view``
argument on ``.render()`` and ``.view()`` methods. Suppresses the ``stderr``
output of started viewer processes (unavailable on Windows).

Add basic debug logging via the stdlib ``logging`` module.

Reformatted some examples, improved tests by using autospec for mocks.


Version 0.11.1
--------------

Include ``stderr`` in ``str()`` of raised ``subprocess.CalledProcessError``.


Version 0.11
------------

Add ``quiet`` argument to ``.render()`` and ``.pipe()`` methods of ``Graph``,
``Digraph``, and ``Source`` objects, allowing to suppress ``stderr`` of the
layout subprocess (parity with stand-alone ``render()`` and ``pipe()``
functions).

The rendering process for ``render()`` methods and stand-alone function is now
started from the directory of the rendered dot source file. This allows to
render graph descriptions that use relative paths inline (e.g. for referring to
image files to be included) by using paths relative to the source file
location. Previously, such relative paths would need to be given relative to
the directory from which ``render()`` was  started, so this change is backwards
incompatible for code that relied on the previous behaviour.

Drop Python 3.4 support.


Version 0.10.1
--------------

Fix broken renderer argument in ``pipe()`` method and function.


Version 0.10
------------

Add ``format`` argument to ``Graph/Digraph.render()``. This follows stand-alone
``render()`` function and mirrors the ``Graph/Digraph.pipe()`` method (usually,
``format`` is set on the instance).

Add ``renderer`` and ``formatter`` arguments to ``Graph/Digraph.render()`` and
``pipe()`` methods, as well as stand-alone ``render()`` and ``pipe()`` functions.


Version 0.9
-----------

Use ``sys.stderr`` to write stderr output from rendering process to stderr
(instead of file descriptor inheritance). Ensures stderr is passed in special
environments such as IDLE.

Suppress rendering process ``stdout`` in ``render()``.

Make ``quiet=True`` also suppress ``stderr`` on success of ``render()`` and
``pipe()`` (exit-status ``0``).

Include ``stderr`` from rendering process in ``CalledProcessError`` exception.


Version 0.8.4
-------------

Tag Python 3.7 support (work around subprocess ``close_fds`` issue on Windows).


Version 0.8.3
-------------

Fix compatibility with ``python -OO``.


Version 0.8.2
-------------

Add ``nohtml()`` to support labels of the form ``'<...>'`` (disabling their default
treatment as HTML strings).

Make default ``'utf-8'`` ``encoding`` more visible.

Set ``encoding = locale.getpreferredencoding()`` when ``encoding`` argument/property is
set to ``None`` explicitly (follow stdlib ``io.open()`` behaviour).


Version 0.8.1
-------------

Add ``Source.from_file()``-classmethod (simpler in-line SVG display of ready-made
.gv files within Jupyter).

Drop Python 3.3 support.


Version 0.8
-----------

Add ``clear()``-method for ``Graph`` and ``Digraph``. 

Add ``grapviz.version()`` function.

Drop dot source extra indent for edge statements following dotguide examples.

Include LICENSE file in wheel.


Version 0.7.1
-------------

Fix ``TypeError`` in ``graphviz.pipe()`` with invalid dot code under Python 3.

Add ``copy()``-method for ``Graph``, ``Digraph``, and ``Source``.

Add ``graphviz.render(..., quiet=True)``.

Fix ``graphivz.view()`` exception on unsupported platform.

Raise a dedicated ``RuntimeError`` subclass ``graphviz.ExecutableNotFound`` when the
Graphviz executables are not found.

Port tests from ``nose/unittest`` to ``pytest``, extend, use mocks.


Version 0.7
-----------

Support setting top-level attrs with ``g.attr(key=value)``.

Add context manager usage of ``subgraph()`` for adding a subgraph in a with-block.

Add json-based output formats to known ``FORMATS`` (Graphviz 2.40+).

Drop extra indent level for DOT source with nonempty ``graph/node/edge_attr``.

Add a final newline to a saved DOT source file if it does not end with one.

Raise ``subprocess.CalledProcessError`` on non-zero exit status from rendering.

Raise early when adding a ``subgraph()`` with ``strict=True`` (avoid DOT syntax error).

Make undocumented ``quote()``, ``quote_edge()``, and ``attributes()`` methods private.


Version 0.6
-----------

Drop Python 2.6 support (use ``graphviz<0.6`` there).

Improve tests for ``mkdirs()``.

Better document adding custom DOT using the ``body`` attribute.

Add ``view()``-support for FreeBSD (pull request Julien Gamba).


Version 0.5.2
-------------

Add ``ENGINES`` and ``FORMATS`` to the documented public API.


Version 0.5.1
-------------

Fixed PY3 compatibility.


Version 0.5
-----------

Add low-level functions ``render()``, ``pipe()``, and ``view()`` for directly working with
existing files and strings.

Support all ``render()``-arguments in the ``view()``-short-cut-method.


Version 0.4.10
--------------

Added ``'patchwork'`` engine.


Version 0.4.9
-------------

Add support for ``strict`` graphs and digraphs.

Hide ``render/pipe()`` subprocess console window on Windows when invoked from
non-console process (e.g. from IDLE).

Improve documentation markup/wording.

Make ``TestNoent`` more robust.


Version 0.4.8
-------------

Make ``_repr_svg_()`` available on ``Source`` (pull request RafalSkolasinski).


Version 0.4.7
-------------

Fixed ``view()``-method on Linux under Python 3 (pull request Antony Lee).


Version 0.4.6
-------------

Fixed ``view()``-method on Linux and Darwin (pull request Eric L. Frederich).


Version 0.4.5
-------------

Added example for HTML-like labels (``structs.py``).

Added ``Source`` class for rendering verbatim DOT source code. 

Added Python 2.6 support (pull request Jim Crist).


Version 0.4.4
-------------

Added the ``pipe()``-method directly returning the ``stdout`` of rendering.

Added ``_repr_svg_()`` for inline rendering in IPython notebooks.


Version 0.4.3
-------------

Added examples generating some of the graphs from the Graphviz Gallery.

Added sphinx-based API documentation.


Version 0.4.2
-------------

Added support for HTML-like labels.


Version 0.4.1
-------------

Added support for less common output formats. Removed dropped formats (``'dia'``, ``'pcl'``).

Added ``'osage'`` layout engine.

Documented ``format`` and ``engine`` options in the README.

The ``view()`` convenience method now returns the result file name (like render()).


Version 0.4
-----------

Added ``attr()`` method for inline switching of node/edge attributes.

Added ``subgraph()`` method (obsoletes separate ``Subgraph`` class).

Add ``cleanup`` option to ``render()``.

Replaced ``dry`` option on ``render()`` with separate ``save()`` method.

Removed undocumented ``append()`` and ``extend()`` methods (if needed, the ``body``
attribute can be edited directly).


Version 0.3.5
-------------

Skip empty ``comment`` when creating DOT source.

Document ``graph_attr``, ``node_attr``, and ``edge_attr`` in the README.

More informative exception when Graphviz executables cannot be called.


Version 0.3.4
-------------

Fixed missing identifier quoting for DOT keywords (thanks to Paulo Urio).


Version 0.3.3
-------------

Made ``format`` and ``engine`` case-insensitive.


Version 0.3.2
-------------

Indent ``graph_attr``, ``node_attr``, and ``edge_attr`` lines, adapt nodes and edges.


Version 0.3.1
-------------

Fixed ``view()`` failing on paths with forward slashes on Windows.


Version 0.3
-----------

Added Python 3.3+ support.

Made attributes order stable (sorting plain dicts).

Fixed edgeop in undirected graphs.


Version 0.2.2
-------------

Support pdf opening on Linux.

Fixed rendering filenames w/spaces.


Version 0.2.1
-------------

Fixed rendering on Mac OS X.


Version 0.2
-----------

Added format selection, use ``'PDF``' as default.
Added engines selection, use ``'dot'`` as default.
Added source encoding, use ``'UTF-8'`` as default.

Changed constructor arguments order, removed ``compile()`` and ``save()``-method,
reimplemented compilation in ``render()`` method, make interface more similar to
gv.3python (backwards incompatible change).

Double-quote-sign escaping, attribute list quoting.

``mkdirs()`` now correctly supports current directory filenames.


Version 0.1.1
-------------

Removed automatic ``'-'`` to ``'&minus;'`` replacement from labels.

Fixed documentation typos.


Version 0.1
-----------

First public release.

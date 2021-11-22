r"""Render DOT source files with Graphviz ``dot``.

>>> doctest_mark_exe()

>>> import pathlib
>>> import warnings
>>> import graphviz

>>> graphviz.render('dot')
Traceback (most recent call last):
    ...
graphviz.exceptions.RequiredArgumentError: format: (required if outfile is not given, got None)

>>> graphviz.render('dot', 'svg')
Traceback (most recent call last):
    ...
graphviz.exceptions.RequiredArgumentError: filepath: (required if outfile is not given, got None)

>>> graphviz.render('dot', outfile='spam.mp3')  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
Traceback (most recent call last):
    ...
graphviz.exceptions.RequiredArgumentError: cannot infer rendering format from outfile: 'spam.mp3'
(provide format or outfile with a suffix from [...])

>>> source = pathlib.Path('doctest-output/spam.gv')
>>> source.write_text('graph { spam }', encoding='ascii')
14

>>> graphviz.render('dot', 'png', source).replace('\\', '/')
'doctest-output/spam.gv.png'

>>> outfile_png =source.with_suffix('.png')
>>> graphviz.render('dot', 'png', source, outfile=outfile_png).replace('\\', '/')
'doctest-output/spam.png'

>>> outfile_dot = source.with_suffix('.dot')
>>> with warnings.catch_warnings(record=True) as catched_warnings:
...     graphviz.render('dot', 'plain', source, outfile=outfile_dot).replace('\\', '/')
'doctest-output/spam.dot'
>>> print(*[repr(w.message) for w in catched_warnings])  # doctest: +NORMALIZE_WHITESPACE
UserWarning("expected format 'dot' from outfile differs from given format: 'plain'")

>>> graphviz.render('dot', 'gv', source, outfile=str(source))
Traceback (most recent call last):
    ...
ValueError: outfile 'spam.gv' must be different from input file 'spam.gv'

>>> graphviz.render('dot', outfile=source.with_suffix('.pdf')).replace('\\', '/')
'doctest-output/spam.pdf'

>>> import os
>>> render = source.parent / 'render'
>>> os.makedirs(render, exist_ok=True)
>>> outfile_render = render / source.with_suffix('.pdf').name
>>> graphviz.render('dot', filepath=source, outfile=outfile_render).replace('\\', '/')
'doctest-output/render/spam.pdf'

"""

import os
import typing
import warnings

from .._defaults import DEFAULT_SOURCE_EXTENSION
from .. import _tools
from .. import exceptions
from .. import parameters

from . import dot_command
from . import execute

__all__ = ['render']


@typing.overload
def render(engine: str,
           format: str,
           filepath: typing.Union[os.PathLike, str],
           renderer: typing.Optional[str] = ...,
           formatter: typing.Optional[str] = ...,
           quiet: bool = ..., *,
           outfile: None = ...) -> str:
    """Require ``format`` and ``filepath`` with default ``outfile=None``."""


@typing.overload
def render(engine: str,
           format: typing.Optional[str] = ...,
           filepath: typing.Optional[typing.Union[os.PathLike, str]] = ...,
           renderer: typing.Optional[str] = ...,
           formatter: typing.Optional[str] = ...,
           quiet: bool = ..., *,
           outfile: str) -> str:
    """Optional ``format`` and ``filepath`` with given ``outfile``."""


@typing.overload
def render(engine: str,
           format: typing.Optional[str] = ...,
           filepath: typing.Optional[typing.Union[os.PathLike, str]] = ...,
           renderer: typing.Optional[str] = ...,
           formatter: typing.Optional[str] = ...,
           quiet: bool = ..., *,
           outfile: typing.Optional[str]) -> str:
    """Required/optional ``format`` and ``filepath`` depending on ``outfile``."""


@_tools.deprecate_positional_args(supported_number=3)
def render(engine: str,
           format: typing.Optional[str] = None,
           filepath: typing.Optional[typing.Union[os.PathLike, str]] = None,
           renderer: typing.Optional[str] = None,
           formatter: typing.Optional[str] = None,
           quiet: bool = False, *,
           outfile: typing.Optional[str] = None) -> str:
    """Render file with ``engine`` into ``format`` and return result filename.

    Args:
        engine: Layout engine for rendering (``'dot'``, ``'neato'``, ...).
        format: Output format for rendering (``'pdf'``, ``'png'``, ...).
        filepath: Path to the DOT source file to render.
        renderer: Output renderer (``'cairo'``, ``'gd'``, ...).
        formatter: Output formatter (``'cairo'``, ``'gd'``, ...).
        quiet: Suppress ``stderr`` output from the layout subprocess.
        outfile: Path for the rendered output file.

    Returns:
        The (possibly relative) path of the rendered file.

    Raises:
        ValueError: If ``engine``, ``format``, ``renderer``, or ``formatter``
            are unknown.
        graphviz.RequiredArgumentError: If ``format`` or ``filepath`` are None
            unless ``outfile`` is given.
        graphviz.RequiredArgumentError: If ``formatter`` is given
            but ``renderer`` is None.
        graphviz.ExecutableNotFound: If the Graphviz 'dot' executable
            is not found.
        graphviz.CalledProcessError: If the returncode (exit status)
            of the rendering 'dot' subprocess is non-zero.

    Note:
        The layout command is started from the directory of ``filepath``,
        so that references to external files
        (e.g. ``[image=images/camelot.png]``)
        can be given as paths relative to the DOT source file.
    """
    if outfile is not None:
        try:
            suffix_format = get_rendering_format(outfile)
        except ValueError:
            if format is None:
                msg = ('cannot infer rendering format from outfile:'
                       f' {outfile!r} (provide format or outfile'
                       f' with a suffix from {sorted(parameters.FORMATS)})')
                raise exceptions.RequiredArgumentError(msg)
        else:
            assert suffix_format is not None
            if format is not None and format.lower() != suffix_format:
                warnings.warn(f'expected format {suffix_format!r} from outfile'
                              f' differs from given format: {format!r}')
            format = suffix_format

        if filepath is None:
            outfile_stem, _ = os.path.splitext(outfile)
            filepath = f'{outfile_stem}.{DEFAULT_SOURCE_EXTENSION}'
    elif format is None:
        raise exceptions.RequiredArgumentError('format: (required if outfile is not given,'
                                             f' got {format!r})')
    elif filepath is None:
        raise exceptions.RequiredArgumentError('filepath: (required if outfile is not given,'
                                             f' got {filepath!r})')

    cmd = dot_command.command(engine, format,
                              renderer=renderer, formatter=formatter)

    dirname, filename = os.path.split(filepath)
    del filepath

    if outfile is not None:
        outfile_dirname, outfile_filename = os.path.split(outfile)

        if (outfile_filename == filename
            and os.path.abspath(outfile_dirname) == os.path.abspath(dirname)):  # noqa: E129
            raise ValueError(f'outfile {outfile_filename!r} must be different'
                             f' from input file {filename!r}')

        rendered = outfile_filename

        if outfile_dirname != dirname:
            outfile_filename = os.path.abspath(outfile)

        cmd += ['-o', outfile_filename]  # https://www.graphviz.org/doc/info/command.html#-o
        rendered_dirname = outfile_dirname
    else:
        cmd.append('-O')  # https://www.graphviz.org/doc/info/command.html#-O
        suffix_args = (formatter, renderer, format)
        suffix = '.'.join(a for a in suffix_args if a is not None)
        rendered = f'{filename}.{suffix}'
        rendered_dirname = dirname

    cmd.append(filename)

    rendered = os.path.join(rendered_dirname, rendered)

    execute.run_check(cmd, cwd=dirname or None,
                      quiet=quiet, capture_output=True,)
    return rendered


def get_rendering_format(outfile: typing.Union[os.PathLike, str]) -> str:
    """Return rendering format inferred from rendered filename suffix.

    >>> get_rendering_format('spam.pdf')  # doctest: +NO_EXE
    'pdf'

    >>> import pathlib
    >>> get_rendering_format(pathlib.Path('spam.gv.svg'))
    'svg'

    >>> get_rendering_format('spam.PNG')
    'png'

    >>> get_rendering_format('spam')
    Traceback (most recent call last):
        ...
    ValueError: cannot infer rendering format from outfile: 'spam' (missing suffix)

    >>> get_rendering_format('spam.mp3')  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    ValueError: cannot infer rendering format from outfile: 'spam.mp3'
        (unknown format: 'mp3' must be one of [...])
    """
    _, suffix = os.path.splitext(outfile)
    if not suffix:
        raise ValueError('cannot infer rendering format from outfile:'
                         f' {outfile!r} (missing suffix)')

    start, sep, format_ = suffix.partition('.')
    assert sep and not start, f"{suffix}.startswith('.')"
    format_ = format_.lower()

    try:
        parameters.verify_format(format_)
    except ValueError:
        raise ValueError('cannot infer rendering format from outfile:'
                         f' {outfile!r} (unknown format: {format_!r}'
                         f' must be one of {sorted(parameters.FORMATS)})')
    return format_

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
graphviz.exceptions.RequiredArgumentError:
cannot infer rendering format from suffix '.mp3' of outfile: 'spam.mp3'
(provide format or outfile with a suffix from ['.bmp', ...])

>>> source = pathlib.Path('doctest-output/spam.gv')
>>> source.write_text('graph { spam }', encoding='ascii')
14

>>> graphviz.render('dot', 'png', source) # doctest: +ELLIPSIS
'doctest-output...spam.gv.png'

>>> outfile_png =source.with_suffix('.png')
>>> graphviz.render('dot', 'png', source, outfile=outfile_png)  # doctest: +ELLIPSIS
'doctest-output...spam.png'

>>> outfile_dot = source.with_suffix('.dot')
>>> with warnings.catch_warnings(record=True) as captured:
...     graphviz.render('dot', 'plain', source, outfile=outfile_dot)  # doctest: +ELLIPSIS
'doctest-output...spam.dot'
>>> print(*[repr(w.message) for w in captured])  # doctest: +NORMALIZE_WHITESPACE
UserWarning("expected format 'dot' from outfile differs from given format: 'plain'")

>>> graphviz.render('dot', 'gv', source, outfile=str(source))
Traceback (most recent call last):
    ...
ValueError: outfile 'spam.gv' must be different from input file 'spam.gv'

>>> graphviz.render('dot', outfile=source.with_suffix('.pdf'))  # doctest: +ELLIPSIS
'doctest-output...spam.pdf'

>>> import os
>>> render = source.parent / 'render'
>>> os.makedirs(render, exist_ok=True)
>>> outfile_render = render / source.with_suffix('.pdf').name
>>> graphviz.render('dot', filepath=source, outfile=outfile_render)  # doctest: +ELLIPSIS
'doctest-output...render...spam.pdf'

>>> graphviz.render('dot', outfile='spam.png', raise_if_result_exists=True, overwrite_filepath=True)
Traceback (most recent call last):
    ...
ValueError: overwrite_filepath cannot be combined with raise_if_result_exists

>>> graphviz.render('dot', outfile=outfile_png, raise_if_result_exists=True)  # doctest: +ELLIPSIS
Traceback (most recent call last):
graphviz.exceptions.FileExistsError: output file exists: 'doctest-output...spam.png'

>>> graphviz.render('dot', 'jpg', outfile='doctest-output/spam.jpeg')  # doctest: +ELLIPSIS
'doctest-output...spam.jpeg'

>>> with warnings.catch_warnings(record=True) as captured:
...     graphviz.render('dot', 'png', outfile='doctest-output/spam.peng')  # doctest: +ELLIPSIS
'doctest-output...spam.peng'
>>> print(*[repr(w.message) for w in captured])  # doctest: +NORMALIZE_WHITESPACE
UserWarning("unknown outfile suffix '.peng' (expected: '.png')")
"""

import os
import pathlib
import typing
import warnings

from .._defaults import DEFAULT_SOURCE_EXTENSION
from .. import _tools
from .. import exceptions
from .. import parameters

from . import dot_command
from . import execute

__all__ = ['render']


def get_supported_formats() -> typing.List[str]:
    """Return a sorted list of supported formats for exception/warning messages.

    >>> get_supported_formats()  # doctest: +ELLIPSIS
    ['bmp', ...]
    """
    return sorted(parameters.FORMATS)


def get_supported_suffixes() -> typing.List[str]:
    """Return a sorted list of supported outfile suffixes for exception/warning messages.

    >>> get_supported_suffixes()  # doctest: +ELLIPSIS
    ['.bmp', ...]
    """
    return [f'.{format}' for format in get_supported_formats()]


def promote_pathlike(filepath: typing.Union[os.PathLike, str, None]
                     ) -> typing.Optional[pathlib.Path]:
    """Return path-like object ``filepath`` promoted into a path object.

    See also:
        https://docs.python.org/3/glossary.html#term-path-like-object
    """
    if filepath is None:
        return None
    return pathlib.Path(filepath)


@typing.overload
def render(engine: str,
           format: str,
           filepath: typing.Union[os.PathLike, str],
           renderer: typing.Optional[str] = ...,
           formatter: typing.Optional[str] = ...,
           quiet: bool = ..., *,
           outfile: typing.Union[os.PathLike, str, None] = ...,
           raise_if_result_exists: bool = ...,
           overwrite_filepath: bool = ...) -> str:
    """Require ``format`` and ``filepath`` with default ``outfile=None``."""


@typing.overload
def render(engine: str,
           format: typing.Optional[str] = ...,
           filepath: typing.Union[os.PathLike, str, None] = ...,
           renderer: typing.Optional[str] = ...,
           formatter: typing.Optional[str] = ...,
           quiet: bool = False, *,
           outfile: typing.Union[os.PathLike, str, None] = ...,
           raise_if_result_exists: bool = ...,
           overwrite_filepath: bool = ...) -> str:
    """Optional ``format`` and ``filepath`` with given ``outfile``."""


@typing.overload
def render(engine: str,
           format: typing.Optional[str] = ...,
           filepath: typing.Union[os.PathLike, str, None] = ...,
           renderer: typing.Optional[str] = ...,
           formatter: typing.Optional[str] = ...,
           quiet: bool = False, *,
           outfile: typing.Union[os.PathLike, str, None] = ...,
           raise_if_result_exists: bool = ...,
           overwrite_filepath: bool = ...) -> str:
    """Required/optional ``format`` and ``filepath`` depending on ``outfile``."""


@_tools.deprecate_positional_args(supported_number=3)
def render(engine: str,
           format: typing.Optional[str] = None,
           filepath: typing.Union[os.PathLike, str, None] = None,
           renderer: typing.Optional[str] = None,
           formatter: typing.Optional[str] = None,
           quiet: bool = False, *,
           outfile: typing.Union[os.PathLike, str, None] = None,
           raise_if_result_exists: bool = False,
           overwrite_filepath: bool = False) -> str:
    """Render file with ``engine`` into ``format`` and return result filename.

    Args:
        engine: Layout engine for rendering (``'dot'``, ``'neato'``, ...).
        format: Output format for rendering (``'pdf'``, ``'png'``, ...).
        filepath: Path to the DOT source file to render.
        renderer: Output renderer (``'cairo'``, ``'gd'``, ...).
        formatter: Output formatter (``'cairo'``, ``'gd'``, ...).
        quiet: Suppress ``stderr`` output from the layout subprocess.
        outfile: Path for the rendered output file.
        raise_if_result_exits: Raise :exc:`.FileExistsError`
            if the result file exists.
        overwrite_filepath: Allow ``dot`` to write to the file it reads from.
            Incompatible with raise_if_outfile_exists.

    Returns:
        The (possibly relative) path of the rendered file.

    Raises:
        ValueError: If ``engine``, ``format``, ``renderer``, or ``formatter``
            are unknown.
        graphviz.RequiredArgumentError: If ``format`` or ``filepath`` are None
            unless ``outfile`` is given.
        graphviz.RequiredArgumentError: If ``formatter`` is given
            but ``renderer`` is None.
        ValueError: If ``outfile`` and ``filename`` are the same file
            unless ``overwite=True``.
        graphviz.ExecutableNotFound: If the Graphviz 'dot' executable
            is not found.
        graphviz.CalledProcessError: If the returncode (exit status)
            of the rendering 'dot' subprocess is non-zero.
        graphviz.FileExistsError: If ``raise_if_exists``
            and the result file exists.

    Note:
        The layout command is started from the directory of ``filepath``,
        so that references to external files
        (e.g. ``[image=images/camelot.png]``)
        can be given as paths relative to the DOT source file.
    """
    if raise_if_result_exists and overwrite_filepath:
        raise ValueError('overwrite_filepath cannot be combined'
                         ' with raise_if_result_exists')

    filepath, outfile = map(promote_pathlike, (filepath, outfile))

    if outfile is not None:
        format = get_rendering_format(outfile, format=format)

        cmd = dot_command.command(engine, format,
                                  renderer=renderer, formatter=formatter)

        if filepath is None:
            filepath = outfile.with_suffix(f'.{DEFAULT_SOURCE_EXTENSION}')

        if (not overwrite_filepath and outfile.name == filepath.name
            and outfile.resolve() == filepath.resolve()):  # noqa: E129
            raise ValueError(f'outfile {outfile.name!r} must be different'
                             f' from input file {filepath.name!r}')

        outfile_arg = (outfile.resolve() if outfile.parent != filepath.parent
                       else outfile.name)

        # https://www.graphviz.org/doc/info/command.html#-o
        cmd += ['-o', outfile_arg, filepath.name]

        rendered = outfile
    elif format is None:
        raise exceptions.RequiredArgumentError('format: (required if outfile is not given,'
                                               f' got {format!r})')
    elif filepath is None:
        raise exceptions.RequiredArgumentError('filepath: (required if outfile is not given,'
                                               f' got {filepath!r})')
    else:
        cmd = dot_command.command(engine, format,
                                  renderer=renderer, formatter=formatter)

        # https://www.graphviz.org/doc/info/command.html#-O
        cmd += ['-O', filepath.name]

        suffix_args = (formatter, renderer, format)
        suffix = '.'.join(a for a in suffix_args if a is not None)

        rendered = filepath.parent / f'{filepath.name}.{suffix}'

    if raise_if_result_exists and os.path.exists(rendered):
        raise exceptions.FileExistsError(f'output file exists: {os.fspath(rendered)!r}')

    cwd = os.fspath(filepath.parent) if filepath.parent.parts else None

    execute.run_check(cmd, cwd=cwd, quiet=quiet,
                      capture_output=True)

    return os.fspath(rendered)


def get_rendering_format(outfile: pathlib.Path, *,
                         format: typing.Optional[str]) -> str:
    """Return format from outfile suffix and/or given format."""
    try:
        result = _get_rendering_format(outfile)
    except ValueError:
        if format is None:
            msg = ('cannot infer rendering format'
                   f' from suffix {outfile.suffix!r}'
                   f' of outfile: {os.fspath(outfile)!r}'
                   ' (provide format or outfile with a suffix'
                   f' from {get_supported_suffixes()!r})')
            raise exceptions.RequiredArgumentError(msg)

        warnings.warn(f'unknown outfile suffix {outfile.suffix!r}'
                      f' (expected: {"." + format!r})')
        return format
    else:
        assert result is not None
        if format is not None and format.lower() != result:
            warnings.warn(f'expected format {result!r} from outfile'
                          f' differs from given format: {format!r}')

        return result


def _get_rendering_format(outfile: pathlib.Path) -> str:
    """Return format inferred from outfile suffix.

    >>> _get_rendering_format(pathlib.Path('spam.pdf'))  # doctest: +NO_EXE
    'pdf'

    >>> import pathlib
    >>> _get_rendering_format(pathlib.Path('spam.gv.svg'))
    'svg'

    >>> _get_rendering_format(pathlib.Path('spam.PNG'))
    'png'

    >>> _get_rendering_format(pathlib.Path('spam'))
    Traceback (most recent call last):
        ...
    ValueError: cannot infer rendering format from outfile: 'spam' (missing suffix)

    >>> _get_rendering_format(pathlib.Path('spam.mp3'))  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    ValueError: cannot infer rendering format from outfile: 'spam.mp3'
        (unknown format: 'mp3' must be one of [...])
    """
    if not outfile.suffix:
        raise ValueError('cannot infer rendering format from outfile:'
                         f' {os.fspath(outfile)!r} (missing suffix)')

    start, sep, format_ = outfile.suffix.partition('.')
    assert sep and not start, f"{outfile.suffix!r}.startswith('.')"
    format_ = format_.lower()

    try:
        parameters.verify_format(format_)
    except ValueError:
        raise ValueError('cannot infer rendering format'
                         f' from outfile: {os.fspath(outfile)!r}'
                         f' (unknown format: {format_!r}'
                         f' must be one of {get_supported_formats()!r})')
    return format_

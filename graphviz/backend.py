# backend.py - execute rendering, open files in viewer

import os
import io
import re
import sys
import errno
import platform
import subprocess
import contextlib

from ._compat import CalledProcessError, stderr_write_bytes

from . import tools

__all__ = ['render', 'pipe', 'version', 'view']

ENGINES = {  # http://www.graphviz.org/pdf/dot.1.pdf
    'dot', 'neato', 'twopi', 'circo', 'fdp', 'sfdp', 'patchwork', 'osage',
}

FORMATS = {  # http://www.graphviz.org/doc/info/output.html
    'bmp',
    'canon', 'dot', 'gv', 'xdot', 'xdot1.2', 'xdot1.4',
    'cgimage',
    'cmap',
    'eps',
    'exr',
    'fig',
    'gd', 'gd2',
    'gif',
    'gtk',
    'ico',
    'imap', 'cmapx',
    'imap_np', 'cmapx_np',
    'ismap',
    'jp2',
    'jpg', 'jpeg', 'jpe',
    'json', 'json0', 'dot_json', 'xdot_json',  # Graphviz 2.40
    'pct', 'pict',
    'pdf',
    'pic',
    'plain', 'plain-ext',
    'png',
    'pov',
    'ps',
    'ps2',
    'psd',
    'sgi',
    'svg', 'svgz',
    'tga',
    'tif', 'tiff',
    'tk',
    'vml', 'vmlz',
    'vrml',
    'wbmp',
    'webp',
    'xlib',
    'x11',
}

PLATFORM = platform.system().lower()

POPEN_KWARGS = {}

if PLATFORM == 'windows':  # pragma: no cover
    POPEN_KWARGS['startupinfo'] = subprocess.STARTUPINFO()
    POPEN_KWARGS['startupinfo'].dwFlags |= subprocess.STARTF_USESHOWWINDOW
    POPEN_KWARGS['startupinfo'].wShowWindow = subprocess.SW_HIDE
    # work around WinError 87 from https://bugs.python.org/issue19764
    # https://github.com/python/cpython/commit/b2a6083eb0384f38839d3f1ed32262a3852026fa
    # TODO: consider not reusing the instance instead (adapt test code for this)
    if sys.version_info >= (3, 7):
        POPEN_KWARGS['close_fds'] = False


class ExecutableNotFound(RuntimeError):
    """Exception raised if the Graphviz executable is not found."""

    _msg = ('failed to execute %r, '
            'make sure the Graphviz executables are on your systems\' PATH')

    def __init__(self, args):
        super(ExecutableNotFound, self).__init__(self._msg % args)


def command(engine, format, filepath=None):
    """Return args list for ``subprocess.Popen`` and name of the rendered file."""
    if engine not in ENGINES:
        raise ValueError('unknown engine: %r' % engine)
    if format not in FORMATS:
        raise ValueError('unknown format: %r' % format)

    cmd = [engine, '-T%s' % format]
    rendered = None
    if filepath is not None:
        cmd.extend(['-O', filepath])
        rendered = '%s.%s' % (filepath, format)

    return cmd, rendered


def run(cmd, input=None, capture_output=False, check=False, quiet=False, **kwargs):
    if input is not None:
        kwargs['stdin'] = subprocess.PIPE
    if capture_output:
        kwargs['stdout'] = kwargs['stderr'] = subprocess.PIPE
    kwargs.update(POPEN_KWARGS)

    try:
        proc = subprocess.Popen(cmd, **kwargs)
    except OSError as e:
        if e.errno == errno.ENOENT:
            raise ExecutableNotFound(cmd)
        else:  # pragma: no cover
            raise

    out, err = proc.communicate(input)
    if not quiet and err:
        stderr_write_bytes(err, flush=True)
    if check and proc.returncode:
        raise CalledProcessError(proc.returncode, cmd, output=out, stderr=err)
    return out, err


def render(engine, format, filepath, quiet=False):
    """Render file with Graphviz ``engine`` into ``format``,  return result filename.

    Args:
        engine: The layout commmand used for rendering (``'dot'``, ``'neato'``, ...).
        format: The output format used for rendering (``'pdf'``, ``'png'``, ...).
        filepath: Path to the DOT source file to render.
        quiet (bool): Suppress ``stderr`` output.
    Returns:
        The (possibly relative) path of the rendered file.
    Raises:
        ValueError: If ``engine`` or ``format`` are not known.
        graphviz.ExecutableNotFound: If the Graphviz executable is not found.
        subprocess.CalledProcessError: If the exit status is non-zero.
    """
    cmd, rendered = command(engine, format, filepath)
    run(cmd, capture_output=True, check=True, quiet=quiet)
    return rendered


def pipe(engine, format, data, quiet=False):
    """Return ``data`` piped through Graphviz ``engine`` into ``format``.

    Args:
        engine: The layout commmand used for rendering (``'dot'``, ``'neato'``, ...).
        format: The output format used for rendering (``'pdf'``, ``'png'``, ...).
        data: The binary (encoded) DOT source string to render.
        quiet (bool): Suppress ``stderr`` output.
    Returns:
        Binary (encoded) stdout of the layout command.
    Raises:
        ValueError: If ``engine`` or ``format`` are not known.
        graphviz.ExecutableNotFound: If the Graphviz executable is not found.
        subprocess.CalledProcessError: If the exit status is non-zero.
    """
    cmd, _ = command(engine, format)
    out, _ = run(cmd, input=data, capture_output=True, check=True, quiet=quiet)
    return out


def version():
    """Return the version number tuple from the ``stderr`` output of ``dot -V``.

    Returns:
        Two or three ``int`` version ``tuple``.
    Raises:
        graphviz.ExecutableNotFound: If the Graphviz executable is not found.
        subprocess.CalledProcessError: If the exit status is non-zero.
        RuntimmeError: If the output cannot be parsed into a version number.
    """
    cmd = ['dot', '-V']
    out, _ = run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    info = out.decode('ascii')
    ma = re.search(r'graphviz version (\d+\.\d+(?:\.\d+)?) ', info)
    if ma is None:
        raise RuntimeError
    return tuple(int(d) for d in ma.group(1).split('.'))


def view(filepath):
    """Open filepath with its default viewing application (platform-specific).

    Args:
        filepath: Path to the file to open in viewer.
    Raises:
        RuntimeError: If the current platform is not supported.
    """
    try:
        view_func = getattr(view, PLATFORM)
    except AttributeError:
        raise RuntimeError('platform %r not supported' % PLATFORM)
    view_func(filepath)


@tools.attach(view, 'darwin')
def view_darwin(filepath):
    """Open filepath with its default application (mac)."""
    subprocess.Popen(['open', filepath])


@tools.attach(view, 'linux')
@tools.attach(view, 'freebsd')
def view_unixoid(filepath):
    """Open filepath in the user's preferred application (linux, freebsd)."""
    subprocess.Popen(['xdg-open', filepath])


@tools.attach(view, 'windows')
def view_windows(filepath):
    """Start filepath with its associated application (windows)."""
    os.startfile(os.path.normpath(filepath))

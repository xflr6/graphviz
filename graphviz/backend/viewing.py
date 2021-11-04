"""Open files in platform-specific default viewing application."""

import logging
import os
import platform
import subprocess

from .. import tools

__all__ = ['view']

PLATFORM = platform.system().lower()


log = logging.getLogger(__name__)


def view(filepath, quiet: bool = False) -> None:
    """Open filepath with its default viewing application
        (platform-specific).

    Args:
        filepath: Path to the file to open in viewer.
        quiet: Suppress ``stderr`` output
            from the viewer process (ineffective on Windows).

    Returns:
        ``None``

    Raises:
        RuntimeError: If the current platform is not supported.

    Note:
        There is no option to wait for the application to close,
        and no way to retrieve the application's exit status.
    """
    try:
        view_func = getattr(view, PLATFORM)
    except AttributeError:
        raise RuntimeError(f'platform {PLATFORM!r} not supported')
    view_func(filepath, quiet=quiet)


@tools.attach(view, 'darwin')
def view_darwin(filepath, *, quiet: bool) -> None:
    """Open filepath with its default application (mac)."""
    cmd = ['open', filepath]
    log.debug('view: %r', cmd)
    kwargs = {'stderr': subprocess.DEVNULL} if quiet else {}
    subprocess.Popen(cmd, **kwargs)


@tools.attach(view, 'linux')
@tools.attach(view, 'freebsd')
def view_unixoid(filepath, *, quiet: bool) -> None:
    """Open filepath in the user's preferred application (linux, freebsd)."""
    cmd = ['xdg-open', filepath]
    log.debug('view: %r', cmd)
    kwargs = {'stderr': subprocess.DEVNULL} if quiet else {}
    subprocess.Popen(cmd, **kwargs)


@tools.attach(view, 'windows')
def view_windows(filepath, *, quiet: bool) -> None:
    """Start filepath with its associated application (windows)."""
    # TODO: implement quiet=True
    filepath = os.path.normpath(filepath)
    log.debug('view: %r', filepath)
    os.startfile(filepath)  # pytype: disable=module-attr

# utils.py

import contextlib
import os
import pathlib


@contextlib.contextmanager
def as_cwd(path):
    """Return a context manager, which changes to the path’s dir during the managed “with” context."""
    cwd = pathlib.Path().resolve()
    os.chdir(path)
    yield
    os.chdir(cwd)

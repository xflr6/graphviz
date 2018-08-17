# test_tools.py

import os
import functools

import pytest

from graphviz.tools import mkdirs


def itertree(root):
    for path, dirs, files in os.walk(root):
        base = os.path.relpath(path, root)
        rel_path = functools.partial(os.path.join, base if base != '.' else '')
        for is_file, names in enumerate((dirs, files)):
            for n in names:
                yield bool(is_file), rel_path(n).replace('\\', '/')


def test_mkdirs_invalid(tmpdir):
    with tmpdir.as_cwd():
        (tmpdir / 'spam.eggs').write_binary(b'')
        with pytest.raises(OSError):
            mkdirs('spam.eggs/spam')


def test_mkdirs(tmpdir):
    with tmpdir.as_cwd():
        mkdirs('spam.eggs')
        assert list(itertree(str(tmpdir))) == []
        for _ in range(2):
            mkdirs('spam/eggs/spam.eggs')
            assert list(itertree(str(tmpdir))) == [(False, 'spam'), (False, 'spam/eggs')]

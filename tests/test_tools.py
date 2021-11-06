import functools
import os

import pytest

from graphviz import tools

import _common


def itertree(root):
    for path, dirs, files in os.walk(root):
        base = os.path.relpath(path, root)
        rel_path = functools.partial(os.path.join, base if base != '.' else '')
        for is_file, names in enumerate((dirs, files)):
            for n in names:
                yield bool(is_file), rel_path(n).replace('\\', '/')


def test_mkdirs_invalid(tmp_path):
    with _common.as_cwd(tmp_path):
        (tmp_path / 'spam.eggs').write_bytes(b'')
        with pytest.raises(OSError):
            tools.mkdirs('spam.eggs/spam')


def test_mkdirs(tmp_path):
    with _common.as_cwd(tmp_path):
        tools.mkdirs('spam.eggs')
        assert list(itertree(str(tmp_path))) == []
        for _ in range(2):
            tools.mkdirs('spam/eggs/spam.eggs')
            assert list(itertree(str(tmp_path))) == [(False, 'spam'),
                                                     (False, 'spam/eggs')]

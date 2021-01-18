# test_tools.py

import pytest

from graphviz.tools import mkdirs

import utils


def itertree(root):
    for path in root.rglob('*'):
        yield path.is_file(), str(path.relative_to(root))


def test_mkdirs_invalid(tmp_path):
    with utils.as_cwd(tmp_path):
        (tmp_path / 'spam.eggs').write_bytes(b'')
        with pytest.raises(OSError):
            mkdirs('spam.eggs/spam')


def test_mkdirs(tmp_path):
    with utils.as_cwd(tmp_path):
        mkdirs('spam.eggs')
        assert list(itertree(tmp_path)) == []
        for _ in range(2):
            mkdirs('spam/eggs/spam.eggs')
            assert list(itertree(tmp_path)) == [(False, 'spam'),
                                                (False, 'spam/eggs')]

import functools
import os
import warnings

import pytest

from graphviz import _tools

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
            _tools.mkdirs('spam.eggs/spam')


def test_mkdirs(tmp_path):
    with _common.as_cwd(tmp_path):
        _tools.mkdirs('spam.eggs')
        assert list(itertree(str(tmp_path))) == []
        for _ in range(2):
            _tools.mkdirs('spam/eggs/spam.eggs')
            assert list(itertree(str(tmp_path))) == [(False, 'spam'),
                                                     (False, 'spam/eggs')]


@pytest.mark.parametrize('category, match',
                         [(FutureWarning, r" third='third' "),
                          (DeprecationWarning, r" third='third' "),
                          (PendingDeprecationWarning, r" third='third' "),
                          (None, None)])
def test_deprecate_positional_args(category, match):
    @_tools.deprecate_positional_args(supported_number=2, category=category)
    def func(first, second, third=None, **kwargs):
        pass

    with warnings.catch_warnings():
        warnings.simplefilter('error')
        func('first', 'second', third='third', extra='extra')

    if category is not None:
        with pytest.warns(category, match=match):
            func('first', 'second', 'third', extra='extra')
    else:
        with warnings.catch_warnings():
            warnings.simplefilter('error')
            func('first', 'second', 'third', extra='extra')

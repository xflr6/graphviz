import subprocess

import pytest

import graphviz


def test_view_unknown_platform(unknown_platform):
    with pytest.raises(RuntimeError, match=r'platform'):
        graphviz.view('nonfilepath')


def test_view(mocker, mock_platform, Popen, startfile, quiet):  # noqa: N803
    assert graphviz.view('nonfilepath', quiet=quiet) is None

    if mock_platform == 'windows':
        startfile.assert_called_once_with('nonfilepath')
        return

    if quiet:
        kwargs = {'stderr': subprocess.DEVNULL}
    else:
        kwargs = {}

    if mock_platform == 'darwin':
        Popen.assert_called_once_with(['open', 'nonfilepath'], **kwargs)
    elif mock_platform in ('linux', 'freebsd'):
        Popen.assert_called_once_with(['xdg-open', 'nonfilepath'], **kwargs)
    else:
        raise RuntimeError

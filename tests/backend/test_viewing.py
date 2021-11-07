import subprocess

import pytest

import graphviz


@pytest.mark.usefixtures('unknown_platform')
def test_view_unknown_platform():
    with pytest.raises(RuntimeError, match=r'platform'):
        graphviz.view('nonfilepath')


def test_view_mocked(mocker, mock_platform, mock_popen, mock_startfile, quiet):
    assert graphviz.view('nonfilepath', quiet=quiet) is None

    if mock_platform == 'windows':
        mock_startfile.assert_called_once_with('nonfilepath')
        return

    if quiet:
        kwargs = {'stderr': subprocess.DEVNULL}
    else:
        kwargs = {}

    if mock_platform == 'darwin':
        mock_popen.assert_called_once_with(['open', 'nonfilepath'], **kwargs)
    elif mock_platform in ('linux', 'freebsd'):
        mock_popen.assert_called_once_with(['xdg-open', 'nonfilepath'], **kwargs)
    else:
        raise RuntimeError

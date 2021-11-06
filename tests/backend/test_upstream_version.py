import subprocess

import pytest

import graphviz

import _common


@pytest.mark.exe(xfail=True, raises=graphviz.ExecutableNotFound)
def test_version(capsys):
    result = graphviz.version()
    assert isinstance(result, tuple) and result
    assert all(isinstance(d, int) for d in result)
    assert capsys.readouterr() == ('', '')


def test_version_parsefail_mocked(sentinel, run):
    run.return_value = subprocess.CompletedProcess(sentinel.cmd,
                                                   returncode=0,
                                                   stdout='nonversioninfo',
                                                   stderr=None)

    with pytest.raises(RuntimeError, match=r'nonversioninfo'):
        graphviz.version()

    run.assert_called_once_with([_common.EXPECTED_DOT_BINARY, '-V'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                startupinfo=_common.StartupinfoMatcher(),
                                encoding='ascii')


@pytest.mark.parametrize(
    'stdout, expected',
    [('dot - graphviz version 1.2.3 (mocked)', (1, 2, 3)),
     ('dot - graphviz version 2.43.20190912.0211 (20190912.0211)\n', (2, 43, 20190912, 211)),
     ('dot - graphviz version 2.44.2~dev.20200927.0217 (20200927.0217)\n', (2, 44, 2)),
     ('dot - graphviz version 2.44.1 (mocked)\n', (2, 44, 1)),
     ('dot - graphviz version 2.44.2~dev.20200704.1652 (mocked)\n', (2, 44, 2))])
def test_version_mocked(sentinel, run, stdout, expected):
    run.return_value = subprocess.CompletedProcess(sentinel.cmd,
                                                   returncode=0,
                                                   stdout=stdout, stderr=None)

    assert graphviz.version() == expected

    run.assert_called_once_with([_common.EXPECTED_DOT_BINARY, '-V'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                startupinfo=_common.StartupinfoMatcher(),
                                encoding='ascii')

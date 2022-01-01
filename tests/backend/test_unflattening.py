import re
import subprocess

import pytest

import graphviz

import _common


def test_unflatten_stagger_missing():
    with pytest.raises(graphviz.RequiredArgumentError, match=r'without stagger'):
        graphviz.unflatten('graph {}', fanout=True)


@pytest.mark.exe
@pytest.mark.parametrize(
    'source, kwargs, expected',
    [('digraph {1 -> 2; 1 -> 3; 1 -> 4}',
      {'stagger': 3, 'fanout': True, 'chain': 42},
      'digraph { 1 -> 2 [minlen=1]; 1 -> 3 [minlen=2]; 1 -> 4 [minlen=3]; }')])
def test_unflatten(source, kwargs, expected):
    result = graphviz.unflatten(source, **kwargs)
    normalized = re.sub(r'\s+', ' ', result.strip())
    assert normalized == expected


def test_unflatten_mocked(capsys, sentinel, mock_run,
                          stagger=10, fanout=True, chain=23):
    mock_run.return_value = subprocess.CompletedProcess(_common.INVALID_CMD,
                                                        returncode=0,
                                                        stdout=sentinel.stdout,
                                                        stderr='')

    result = graphviz.unflatten('nonsource',
                                stagger=stagger, fanout=fanout, chain=chain)
    assert result is sentinel.stdout

    mock_run.assert_called_once_with([_common.EXPECTED_UNFLATTEN_BINARY,
                                      '-l', '10', '-f', '-c', '23'],
                                     input='nonsource',
                                     capture_output=True,
                                     startupinfo=_common.StartupinfoMatcher(),
                                     encoding='utf-8')
    assert capsys.readouterr() == ('', '')

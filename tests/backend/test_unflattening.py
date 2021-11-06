import pathlib
import re
import subprocess

import pytest

import graphviz

import _utils

EXPECTED_UNFLATTEN_BINARY = pathlib.Path('unflatten')


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


def test_unflatten_mocked(capsys, mocker, sentinel, run):
    run.return_value = subprocess.CompletedProcess(sentinel.cmd,
                                                   returncode=0,
                                                   stdout='nonresult',
                                                   stderr='')

    assert graphviz.unflatten('nonsource') == 'nonresult'

    run.assert_called_once_with([EXPECTED_UNFLATTEN_BINARY],
                                input='nonsource',
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                startupinfo=mocker.ANY,
                                encoding='utf-8')
    _utils.check_startupinfo(run.call_args.kwargs['startupinfo'])
    assert capsys.readouterr() == ('', '')


def test_unflatten_stagger_missing():
    with pytest.raises(graphviz.RequiredArgumentError, match=r'without stagger'):
        graphviz.unflatten('graph {}', fanout=True)

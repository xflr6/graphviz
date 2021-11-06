import pathlib
import re
import subprocess

import pytest

from graphviz.backend import (render, pipe, unflatten, version, view,
                              ExecutableNotFound, RequiredArgumentError)

import _utils

DOT_BINARY = pathlib.Path('dot')

UNFLATTEN_BINARY = pathlib.Path('unflatten')

SVG_PATTERN = r'(?s)^<\?xml .+</svg>\s*$'


@pytest.mark.usefixtures('empty_path')
@pytest.mark.parametrize('func, args', [
    (render, ['dot', 'pdf', 'nonfilepath']),
    (pipe, ['dot', 'pdf', b'nongraph']),
    (unflatten, ['graph {}']),
    (version, []),
])
def test_missing_executable(func, args):
    with pytest.raises(ExecutableNotFound, match=r'execute'):
        func(*args)


@pytest.mark.exe
@pytest.mark.xfail('version() == (2, 36, 0)',
                   reason='https://bugs.launchpad.net/ubuntu/+source/graphviz/+bug/1694108')
def test_pipe_invalid_data(capsys, quiet, engine='dot', format_='svg'):
    with pytest.raises(subprocess.CalledProcessError) as e:
        pipe(engine, format_, b'nongraph', quiet=quiet)

    assert e.value.returncode == 1
    assert 'syntax error in line' in str(e.value)
    out, err = capsys.readouterr()
    assert out == ''
    if quiet:
        assert err == ''
    else:
        assert 'syntax error in line' in err


@pytest.mark.exe
@pytest.mark.parametrize('engine, format_, renderer, formatter, pattern', [
    ('dot', 'svg', None, None, SVG_PATTERN),
    ('dot', 'ps', 'ps', 'core', r'%!PS-'),
    # Error: remove_overlap: Graphviz not built with triangulation library
    pytest.param('sfdp', 'svg', None, None, SVG_PATTERN,
        marks=pytest.mark.xfail('version() > (2, 38, 0)'
                                " and platform.system().lower() == 'windows'",
        reason='https://gitlab.com/graphviz/graphviz/-/issues/1269')),
])
def test_pipe(capsys, engine, format_, renderer, formatter, pattern,
              data=b'graph { spam }'):
    out = pipe(engine, format_, data, renderer, formatter).decode('ascii')

    if pattern is not None:
        assert re.match(pattern, out)
    assert capsys.readouterr() == ('', '')


def test_pipe_pipe_invalid_data_mocked(mocker, run, quiet):
    mock_sys_stderr = mocker.patch('sys.stderr', autospec=True,
                               **{'flush': mocker.Mock(),
                                  'encoding': mocker.sentinel.encoding})

    mock_out = mocker.create_autospec(bytes, instance=True, name='mock_out')
    mock_err = mocker.create_autospec(bytes, instance=True, name='mock_err',
                                      **{'__len__.return_value': 1})

    run.return_value = subprocess.CompletedProcess(mocker.sentinel.cmd,
                                                   returncode=5,
                                                   stdout=mock_out,
                                                   stderr=mock_err)

    with pytest.raises(subprocess.CalledProcessError) as e:
        pipe('dot', 'png', b'nongraph', quiet=quiet)

    assert e.value.returncode == 5
    assert e.value.cmd is mocker.sentinel.cmd
    assert e.value.stdout is mock_out
    assert e.value.stderr is mock_err
    e.value.stdout = mocker.sentinel.new_stdout
    assert e.value.stdout is mocker.sentinel.new_stdout
    run.assert_called_once_with([DOT_BINARY, '-Kdot', '-Tpng'],
                                input=b'nongraph',
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                startupinfo=mocker.ANY)
    _utils.check_startupinfo(run.call_args.kwargs['startupinfo'])
    if not quiet:
        mock_out.decode.assert_not_called()
        mock_err.decode.assert_called_once_with(mocker.sentinel.encoding)
        mock_sys_stderr.write.assert_called_once_with(mock_err.decode.return_value)
        mock_sys_stderr.flush.assert_called_once_with()


def test_pipe_mocked(capsys, mocker, run, quiet):
    run.return_value = subprocess.CompletedProcess(mocker.sentinel.cmd,
                                                   returncode=0,
                                                   stdout=b'stdout',
                                                   stderr=b'stderr')

    assert pipe('dot', 'png', b'nongraph', quiet=quiet) == b'stdout'

    run.assert_called_once_with([DOT_BINARY, '-Kdot', '-Tpng'],
                                input=b'nongraph',
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                startupinfo=mocker.ANY)
    _utils.check_startupinfo(run.call_args.kwargs['startupinfo'])
    assert capsys.readouterr() == ('', '' if quiet else 'stderr')


@pytest.mark.exe
@pytest.mark.parametrize('source, kwargs, expected', [
    ('digraph {1 -> 2; 1 -> 3; 1 -> 4}',
     {'stagger': 3, 'fanout': True, 'chain': 42},
     'digraph { 1 -> 2 [minlen=1]; 1 -> 3 [minlen=2]; 1 -> 4 [minlen=3]; }'),
])
def test_unflatten(source, kwargs, expected):
    result = unflatten(source, **kwargs)
    normalized = re.sub(r'\s+', ' ', result.strip())
    assert normalized == expected


def test_unflatten_mocked(capsys, mocker, run):
    run.return_value = subprocess.CompletedProcess(mocker.sentinel.cmd,
                                                   returncode=0,
                                                   stdout='nonresult',
                                                   stderr='')

    assert unflatten('nonsource') == 'nonresult'

    run.assert_called_once_with([UNFLATTEN_BINARY],
                                input='nonsource',
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                startupinfo=mocker.ANY,
                                encoding='utf-8')
    _utils.check_startupinfo(run.call_args.kwargs['startupinfo'])
    assert capsys.readouterr() == ('', '')


def test_unflatten_stagger_missing():
    with pytest.raises(RequiredArgumentError, match=r'without stagger'):
        unflatten('graph {}', fanout=True)


@pytest.mark.exe(xfail=True, raises=ExecutableNotFound)
def test_version(capsys):
    result = version()
    assert isinstance(result, tuple) and result
    assert all(isinstance(d, int) for d in result)
    assert capsys.readouterr() == ('', '')


def test_version_parsefail_mocked(mocker, run):
    run.return_value = subprocess.CompletedProcess(mocker.sentinel.cmd,
                                                   returncode=0,
                                                   stdout='nonversioninfo',
                                                   stderr=None)

    with pytest.raises(RuntimeError, match=r'nonversioninfo'):
        version()

    run.assert_called_once_with([DOT_BINARY, '-V'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                startupinfo=mocker.ANY,
                                encoding='ascii')
    _utils.check_startupinfo(run.call_args.kwargs['startupinfo'])


@pytest.mark.parametrize('stdout, expected', [
    ('dot - graphviz version 1.2.3 (mocked)', (1, 2, 3)),
    ('dot - graphviz version 2.43.20190912.0211 (20190912.0211)\n', (2, 43, 20190912, 211)),
    ('dot - graphviz version 2.44.2~dev.20200927.0217 (20200927.0217)\n', (2, 44, 2)),
    ('dot - graphviz version 2.44.1 (mocked)\n', (2, 44, 1)),
    ('dot - graphviz version 2.44.2~dev.20200704.1652 (mocked)\n', (2, 44, 2)),
])
def test_version_mocked(mocker, run, stdout, expected):
    run.return_value = subprocess.CompletedProcess(mocker.sentinel.cmd,
                                                   returncode=0,
                                                   stdout=stdout, stderr=None)

    assert version() == expected

    run.assert_called_once_with([DOT_BINARY, '-V'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                startupinfo=mocker.ANY,
                                encoding='ascii')
    _utils.check_startupinfo(run.call_args.kwargs['startupinfo'])


def test_view_unknown_platform(unknown_platform):
    with pytest.raises(RuntimeError, match=r'platform'):
        view('nonfilepath')


def test_view(mocker, mock_platform, Popen, startfile, quiet):  # noqa: N803
    assert view('nonfilepath', quiet=quiet) is None

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

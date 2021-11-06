import re
import subprocess

import pytest

import graphviz

import _utils

SVG_PATTERN = r'(?s)^<\?xml .+</svg>\s*$'


@pytest.mark.exe
@pytest.mark.xfail('graphviz.version() == (2, 36, 0)',
                   reason='https://bugs.launchpad.net/ubuntu/+source/graphviz/+bug/1694108')
def test_pipe_invalid_data(capsys, quiet, engine='dot', format_='svg'):
    with pytest.raises(subprocess.CalledProcessError) as e:
        graphviz.pipe(engine, format_, b'nongraph', quiet=quiet)

    assert e.value.returncode == 1
    assert 'syntax error in line' in str(e.value)
    out, err = capsys.readouterr()
    assert out == ''
    if quiet:
        assert err == ''
    else:
        assert 'syntax error in line' in err


@pytest.mark.exe
@pytest.mark.parametrize(
    'engine, format_, renderer, formatter, pattern',
    [('dot', 'svg', None, None, SVG_PATTERN),
     ('dot', 'ps', 'ps', 'core', r'%!PS-'),
     # Error: remove_overlap: Graphviz not built with triangulation library
     pytest.param('sfdp', 'svg', None, None, SVG_PATTERN,
         marks=pytest.mark.xfail('graphviz.version() > (2, 38, 0)'
                                " and platform.system().lower() == 'windows'",
         reason='https://gitlab.com/graphviz/graphviz/-/issues/1269'))])
def test_pipe(capsys, engine, format_, renderer, formatter, pattern,
              data=b'graph { spam }'):
    out = graphviz.pipe(engine, format_, data, renderer, formatter).decode('ascii')

    if pattern is not None:
        assert re.match(pattern, out)
    assert capsys.readouterr() == ('', '')


def test_pipe_pipe_invalid_data_mocked(mocker, sentinel, run, quiet):
    mock_sys_stderr = mocker.patch('sys.stderr', autospec=True,
                               **{'flush': mocker.Mock(),
                                  'encoding': sentinel.encoding})

    mock_out = mocker.create_autospec(bytes, instance=True, name='mock_out')
    mock_err = mocker.create_autospec(bytes, instance=True, name='mock_err',
                                      **{'__len__.return_value': 1})

    run.return_value = subprocess.CompletedProcess(sentinel.cmd,
                                                   returncode=5,
                                                   stdout=mock_out,
                                                   stderr=mock_err)

    with pytest.raises(subprocess.CalledProcessError) as e:
        graphviz.pipe('dot', 'png', b'nongraph', quiet=quiet)

    assert e.value.returncode == 5
    assert e.value.cmd is sentinel.cmd
    assert e.value.stdout is mock_out
    assert e.value.stderr is mock_err
    e.value.stdout = sentinel.new_stdout
    assert e.value.stdout is sentinel.new_stdout
    run.assert_called_once_with([_utils.EXPECTED_DOT_BINARY, '-Kdot', '-Tpng'],
                                input=b'nongraph',
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                startupinfo=mocker.ANY)
    _utils.check_startupinfo(run.call_args.kwargs['startupinfo'])
    if not quiet:
        mock_out.decode.assert_not_called()
        mock_err.decode.assert_called_once_with(sentinel.encoding)
        mock_sys_stderr.write.assert_called_once_with(mock_err.decode.return_value)
        mock_sys_stderr.flush.assert_called_once_with()


def test_pipe_mocked(capsys, mocker, sentinel, run, quiet):
    run.return_value = subprocess.CompletedProcess(sentinel.cmd,
                                                   returncode=0,
                                                   stdout=b'stdout',
                                                   stderr=b'stderr')

    assert graphviz.pipe('dot', 'png', b'nongraph', quiet=quiet) == b'stdout'

    run.assert_called_once_with([_utils.EXPECTED_DOT_BINARY, '-Kdot', '-Tpng'],
                                input=b'nongraph',
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                startupinfo=mocker.ANY)
    _utils.check_startupinfo(run.call_args.kwargs['startupinfo'])
    assert capsys.readouterr() == ('', '' if quiet else 'stderr')

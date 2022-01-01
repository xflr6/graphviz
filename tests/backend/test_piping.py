import io
import re
import subprocess

import pytest

import graphviz

import _common

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


def test_pipe_pipe_invalid_data_mocked(mocker, sentinel, mock_run, quiet):
    mock_sys_stderr = mocker.patch('sys.stderr', autospec=True,
                                   flush=mocker.Mock(),
                                   encoding=sentinel.encoding)

    mock_out = mocker.create_autospec(bytes, instance=True, name='mock_out')
    mock_err = mocker.create_autospec(bytes, instance=True, name='mock_err',
                                      **{'__len__.return_value': 1})

    mock_run.return_value = subprocess.CompletedProcess(_common.INVALID_CMD,
                                                        returncode=5,
                                                        stdout=mock_out,
                                                        stderr=mock_err)

    with pytest.raises(subprocess.CalledProcessError) as e:
        graphviz.pipe('dot', 'png', b'nongraph', quiet=quiet)

    assert e.value.returncode == 5
    assert e.value.cmd == _common.INVALID_CMD
    assert e.value.stdout is mock_out
    assert e.value.stderr is mock_err
    e.value.stdout = sentinel.new_stdout
    assert e.value.stdout is sentinel.new_stdout
    mock_run.assert_called_once_with([_common.EXPECTED_DOT_BINARY,
                                      '-Kdot', '-Tpng'],
                                     input=b'nongraph',
                                     capture_output=True,
                                     startupinfo=_common.StartupinfoMatcher())
    if not quiet:
        mock_out.decode.assert_not_called()
        mock_err.decode.assert_called_once_with(sentinel.encoding)
        mock_sys_stderr.write.assert_called_once_with(mock_err.decode.return_value)
        mock_sys_stderr.flush.assert_called_once_with()


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
    with pytest.deprecated_call():
        out = graphviz.pipe(engine, format_, data,
                            renderer, formatter).decode('ascii')

    if pattern is not None:
        assert re.match(pattern, out)
    assert capsys.readouterr() == ('', '')


def test_pipe_mocked(capsys, mock_run, quiet):
    mock_run.return_value = subprocess.CompletedProcess(_common.INVALID_CMD,
                                                        returncode=0,
                                                        stdout=b'stdout',
                                                        stderr=b'stderr')

    assert graphviz.pipe('dot', 'png', b'nongraph',
                         quiet=quiet) == b'stdout'

    mock_run.assert_called_once_with([_common.EXPECTED_DOT_BINARY,
                                      '-Kdot', '-Tpng'],
                                     input=b'nongraph',
                                     capture_output=True,
                                     startupinfo=_common.StartupinfoMatcher())
    assert capsys.readouterr() == ('', '' if quiet else 'stderr')


def test_pipe_string_mocked(capsys, mock_run, quiet,
                            encoding='ascii'):
    mock_run.return_value = subprocess.CompletedProcess(_common.INVALID_CMD,
                                                        returncode=0,
                                                        stdout='stdout',
                                                        stderr='stderr')

    assert graphviz.pipe_string('dot', 'png', 'nongraph',
                                encoding=encoding, quiet=quiet) == 'stdout'

    mock_run.assert_called_once_with([_common.EXPECTED_DOT_BINARY, '-Kdot', '-Tpng'],
                                     input='nongraph',
                                     encoding=encoding,
                                     capture_output=True,
                                     startupinfo=_common.StartupinfoMatcher())
    assert capsys.readouterr() == ('', '' if quiet else 'stderr')


def test_pipe_lines_mocked(capsys, mock_popen, quiet,
                           input_encoding='ascii'):
    proc = mock_popen.return_value
    proc.configure_mock(args=_common.EXPECTED_DOT_BINARY,
                        returncode=0,
                        stdin=io.BytesIO(),
                        stdout=io.BytesIO(b'stdout'),
                        stderr=io.BytesIO(b'stderr'))
    proc.communicate.side_effect = lambda: (proc.stdout.read(), proc.stderr.read())

    assert graphviz.pipe_lines('dot', 'png', iter(['nongraph\n']),
                               input_encoding=input_encoding,
                               quiet=quiet) == b'stdout'

    assert proc.stdin.getvalue() == b'nongraph\n'

    mock_popen.assert_called_once_with([_common.EXPECTED_DOT_BINARY,
                                        '-Kdot', '-Tpng'],
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       startupinfo=_common.StartupinfoMatcher())
    assert capsys.readouterr() == ('', '' if quiet else 'stderr')


def test_pipe_lines_string_mocked(capsys, mock_popen, quiet,
                                  encoding='ascii'):
    proc = mock_popen.return_value
    proc.configure_mock(args=_common.INVALID_CMD,
                        returncode=0,
                        stdin=io.StringIO(),
                        stdout=io.StringIO('stdout'),
                        stderr=io.StringIO('stderr'))
    proc.communicate.side_effect = lambda: (proc.stdout.read(), proc.stderr.read())

    assert graphviz.pipe_lines_string('dot', 'png', iter(['nongraph\n']),
                                      encoding=encoding,
                                      quiet=quiet) == 'stdout'

    assert proc.stdin.getvalue() == 'nongraph\n'

    mock_popen.assert_called_once_with([_common.EXPECTED_DOT_BINARY,
                                        '-Kdot', '-Tpng'],
                                       encoding=encoding,
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       startupinfo=_common.StartupinfoMatcher())
    assert capsys.readouterr() == ('', '' if quiet else 'stderr')

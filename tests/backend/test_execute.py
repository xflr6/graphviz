import errno
import io
import subprocess

import pytest

import graphviz
from graphviz.backend import execute

import _utils

INVALID_CMD = ['']


def test_run_check_oserror():
    with pytest.raises(OSError) as e:
        execute.run_check(INVALID_CMD)

    assert e.value.errno in (errno.EACCES, errno.EINVAL)


def test_run_check_input_lines_mocked(mocker, sentinel, Popen,
                                      line=b'sp\xc3\xa4m'):  # noqa: N803
    mock_sys_stderr = mocker.patch('sys.stderr', autospec=True,
                                   **{'flush': mocker.Mock(),
                                      'encoding': sentinel.encoding})

    mock_out = mocker.create_autospec(bytes, instance=True, name='mock_out')
    mock_err = mocker.create_autospec(bytes, instance=True, name='mock_err',
                                      **{'__len__.return_value': 1})

    popen = Popen.return_value
    popen.returncode = 0
    popen.args = sentinel.cmd
    popen.stdin = mocker.create_autospec(io.BytesIO, instance=True)
    popen.communicate.return_value = (mock_out, mock_err)

    result = execute.run_check(popen.args, input_lines=iter([line]),
                               capture_output=True)

    # subprocess.CompletedProcess.__eq__() is not implemented
    assert isinstance(result, subprocess.CompletedProcess)
    assert result.args is popen.args
    assert result.returncode == popen.returncode
    assert result.stdout is mock_out
    assert result.stderr is mock_err

    Popen.assert_called_once_with(sentinel.cmd,
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  startupinfo=mocker.ANY)
    _utils.check_startupinfo(Popen.call_args.kwargs['startupinfo'])
    popen.communicate.assert_called_once_with()
    mock_out.decode.assert_not_called()
    mock_err.decode.assert_called_once_with(sentinel.encoding)
    mock_sys_stderr.write.assert_called_once_with(mock_err.decode.return_value)
    mock_sys_stderr.flush.assert_called_once_with()


@pytest.mark.usefixtures('empty_path')
@pytest.mark.parametrize(
    'func, args',
    [(graphviz.render, ['dot', 'pdf', 'nonfilepath']),
     (graphviz.pipe, ['dot', 'pdf', b'nongraph']),
     (graphviz.unflatten, ['graph {}']),
     (graphviz.version, [])])
def test_missing_executable(func, args):
    with pytest.raises(graphviz.ExecutableNotFound, match=r'execute'):
        func(*args)


def test_run_check_called_process_error_mocked(capsys, sentinel, run,
                                               stdout='I am the messiah',
                                               stderr='I am not the messiah!'):
    run.return_value = subprocess.CompletedProcess(INVALID_CMD, returncode=500,
                                                   stdout=stdout, stderr=stderr)
    with pytest.raises(execute.CalledProcessError, match=stderr):
        execute.run_check(INVALID_CMD, capture_output=True)

    assert capsys.readouterr() == ('', stderr)

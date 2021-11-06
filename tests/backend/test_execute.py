import errno
import io
import subprocess

import pytest

from graphviz.backend.execute import run_check

import _utils


@pytest.mark.exe
def test_run_check_oserror():
    with pytest.raises(OSError) as e:
        run_check([''])
    assert e.value.errno in (errno.EACCES, errno.EINVAL)


def test_run_check_input_lines_mocked(mocker, Popen, line=b'sp\xc3\xa4m'):  # noqa: N803
    mock_sys_stderr = mocker.patch('sys.stderr', autospec=True,
                                   **{'flush': mocker.Mock(),
                                      'encoding': mocker.sentinel.encoding})

    mock_out = mocker.create_autospec(bytes, instance=True, name='mock_out')
    mock_err = mocker.create_autospec(bytes, instance=True, name='mock_err',
                                      **{'__len__.return_value': 1})

    popen = Popen.return_value
    popen.returncode = 0
    popen.args = mocker.sentinel.cmd
    popen.stdin = mocker.create_autospec(io.BytesIO, instance=True)
    popen.communicate.return_value = (mock_out, mock_err)

    result = run_check(popen.args, input_lines=iter([line]), capture_output=True)

    # subprocess.CompletedProcess.__eq__() is not implemented
    assert isinstance(result, subprocess.CompletedProcess)
    assert result.args is popen.args
    assert result.returncode == popen.returncode
    assert result.stdout is mock_out
    assert result.stderr is mock_err

    Popen.assert_called_once_with(mocker.sentinel.cmd,
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  startupinfo=mocker.ANY)
    _utils.check_startupinfo(Popen.call_args.kwargs['startupinfo'])
    popen.communicate.assert_called_once_with()
    mock_out.decode.assert_not_called()
    mock_err.decode.assert_called_once_with(mocker.sentinel.encoding)
    mock_sys_stderr.write.assert_called_once_with(mock_err.decode.return_value)
    mock_sys_stderr.flush.assert_called_once_with()

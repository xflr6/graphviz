# test_backend.py

import subprocess

import pytest

from graphviz.backend import (render, pipe, version, view,
                              ExecutableNotFound, STARTUPINFO)


def test_render_engine_unknown():
    with pytest.raises(ValueError, match=r'engine'):
        render('', 'pdf', 'nonfilepath')


def test_render_format_unknown():
    with pytest.raises(ValueError, match=r'format'):
        render('dot', '', 'nonfilepath')


def test_render_missing_executable(empty_path):
    with pytest.raises(ExecutableNotFound, match=r'execute'):
        render('dot', 'pdf', 'nonfilepath')


@pytest.exe
def test_render_missing_file(quiet, engine='dot', format_='pdf'):
    with pytest.raises(subprocess.CalledProcessError) as e:
        render(engine, format_, '', quiet=quiet)
    assert e.value.returncode == 2


@pytest.exe
def test_render(capsys, tmpdir, engine='dot', format_='pdf',
                filename='hello.gv', data=b'digraph { hello -> world }'):
    source = tmpdir.join(filename)
    source.write(data)
    rendered = source.new(ext='%s.%s' % (source.ext, format_))

    assert render(engine, format_, str(source)) == str(rendered)

    assert rendered.size()
    assert capsys.readouterr() == ('', '')


def test_render_mocked(mocker, check_call, quiet):
    open_ = mocker.patch('io.open', mocker.mock_open())
    mocker.patch('os.devnull', mocker.sentinel.devnull)

    assert render('dot', 'pdf', 'nonfilepath', quiet=quiet) == 'nonfilepath.pdf'

    if quiet:
        open_.assert_called_once_with(mocker.sentinel.devnull, 'w')
        stderr = open_.return_value
    else:
        stderr = None
    check_call.assert_called_once_with(['dot', '-Tpdf', '-O', 'nonfilepath'],
                                       startupinfo=STARTUPINFO, stderr=stderr)


def test_pipe_missing_executable(empty_path):
    with pytest.raises(ExecutableNotFound, match=r'execute'):
        pipe('dot', 'pdf', b'nongraph')


@pytest.exe
@pytest.mark.xfail('version() == (2, 36, 0)', reason='https://bugs.launchpad.net/ubuntu/+source/graphviz/+bug/1694108')
def test_pipe_invalid_data(capsys, quiet, engine='dot', format_='svg'):
    with pytest.raises(subprocess.CalledProcessError) as e:
        pipe(engine, format_, b'nongraph', quiet=quiet)

    assert e.value.returncode == 1
    out, err = capsys.readouterr()
    assert out == ''
    if quiet:
        assert err == ''
    else:
        assert 'syntax error' in err


@pytest.exe
def test_pipe(capsys, svg_pattern, engine='dot', format_='svg',
              data=b'graph { spam }'):
    src = pipe(engine, format_, data).decode('ascii')

    assert svg_pattern.match(src)
    assert capsys.readouterr() == ('', '')


def test_pipe_pipe_invalid_data_mocked(mocker, py2, Popen, quiet):  # noqa: N803
    stderr = mocker.patch('sys.stderr')
    proc = Popen.return_value
    proc.returncode = mocker.sentinel.returncode
    errs = mocker.Mock()
    proc.communicate.return_value = mocker.sentinel.outs, errs

    with pytest.raises(subprocess.CalledProcessError) as e:
        pipe('dot', 'png', b'nongraph', quiet=quiet)

    assert e.value.returncode is mocker.sentinel.returncode
    Popen.assert_called_once_with(['dot', '-Tpng'],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, startupinfo=STARTUPINFO)
    proc.communicate.assert_called_once_with(b'nongraph')
    if not quiet:
        if py2:
            stderr.write.assert_called_once_with(errs)
        else:
            errs.decode.assert_called_once_with(stderr.encoding)
            stderr.write.assert_called_once_with(errs.decode.return_value)
        stderr.flush.assert_called_once_with()


def test_pipe_mocked(mocker, Popen):  # noqa: N803
    proc = Popen.return_value
    proc.returncode = 0
    proc.communicate.return_value = mocker.sentinel.outs, mocker.sentinel.errs

    assert pipe('dot', 'png', b'nongraph') is mocker.sentinel.outs

    Popen.assert_called_once_with(['dot', '-Tpng'],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, startupinfo=STARTUPINFO)
    proc.communicate.assert_called_once_with(b'nongraph')


def test_version_missing_executable(empty_path):
    with pytest.raises(ExecutableNotFound, match=r'execute'):
        version()


@pytest.exe
def test_version(capsys):
    assert version() is not None
    assert capsys.readouterr() == ('', '')


def test_version_mocked(check_output):
    check_output.return_value = b'dot - graphviz version 1.2.3 (mocked)'
    assert version() == (1, 2, 3)
    check_output.assert_called_once_with(['dot', '-V'], startupinfo=STARTUPINFO,
                                         stderr=subprocess.STDOUT)


def test_view(platform, Popen, startfile):  # noqa: N803
    if platform == 'nonplatform':
        with pytest.raises(RuntimeError, match=r'platform'):
            view('nonfilepath')
    else:
        view('nonfilepath')
        if platform == 'darwin':
            Popen.assert_called_once_with(['open', 'nonfilepath'])
        elif platform in ('linux', 'freebsd'):
            Popen.assert_called_once_with(['xdg-open', 'nonfilepath'])
        elif platform == 'windows':
            startfile.assert_called_once_with('nonfilepath')
        else:
            raise RuntimeError

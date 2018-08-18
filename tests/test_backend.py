# test_backend.py

import platform
import subprocess

import pytest

from graphviz.backend import render, pipe, version, view, ExecutableNotFound


if platform.system().lower() == 'windows':
    def check_startupinfo(Popen):
        startupinfo = Popen.call_args[1]['startupinfo']
        assert isinstance(startupinfo, subprocess.STARTUPINFO)
        assert startupinfo.dwFlags & subprocess.STARTF_USESHOWWINDOW
        assert startupinfo.wShowWindow == subprocess.SW_HIDE
else:
    def check_startupinfo(Popen):
        assert Popen.call_args[1]['startupinfo'] is None


def test_render_engine_unknown():
    with pytest.raises(ValueError, match=r'engine'):
        render('', 'pdf', 'nonfilepath')


def test_render_format_unknown():
    with pytest.raises(ValueError, match=r'format'):
        render('dot', '', 'nonfilepath')


@pytest.mark.usefixtures('empty_path')
def test_render_missing_executable():
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
    lpath = tmpdir / filename
    lpath.write_binary(data)
    rendered = lpath.new(ext='%s.%s' % (lpath.ext, format_))

    assert render(engine, format_, str(lpath)) == str(rendered)

    assert rendered.size()
    assert capsys.readouterr() == ('', '')


def test_render_mocked(capsys, mocker, Popen, quiet):
    proc = Popen.return_value
    proc.returncode = 0
    proc.communicate.return_value = (b'stdout', b'stderr')

    assert render('dot', 'pdf', 'nonfilepath', quiet=quiet) == 'nonfilepath.pdf'

    Popen.assert_called_once_with(['dot', '-Tpdf', '-O', 'nonfilepath'],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  startupinfo=mocker.ANY)
    check_startupinfo(Popen)
    proc.communicate.assert_called_once_with(None)
    assert capsys.readouterr() == ('', '' if quiet else 'stderr')


@pytest.mark.usefixtures('empty_path')
def test_pipe_missing_executable():
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
    stderr = mocker.patch('sys.stderr', new_callable=mocker.NonCallableMock)
    proc = Popen.return_value
    proc.returncode = mocker.sentinel.returncode
    err = mocker.Mock()
    proc.communicate.return_value = (mocker.sentinel.out, err)

    with pytest.raises(subprocess.CalledProcessError) as e:
        pipe('dot', 'png', b'nongraph', quiet=quiet)

    assert e.value.returncode is mocker.sentinel.returncode
    assert e.value.stdout is mocker.sentinel.out
    assert e.value.stderr is err
    Popen.assert_called_once_with(['dot', '-Tpng'],
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  startupinfo=mocker.ANY)
    check_startupinfo(Popen)
    proc.communicate.assert_called_once_with(b'nongraph')
    if not quiet:
        if py2:
            stderr.write.assert_called_once_with(err)
        else:
            err.decode.assert_called_once_with(stderr.encoding)
            stderr.write.assert_called_once_with(err.decode.return_value)
        stderr.flush.assert_called_once_with()


def test_pipe_mocked(capsys, mocker, Popen, quiet):  # noqa: N803
    proc = Popen.return_value
    proc.returncode = 0
    proc.communicate.return_value = (mocker.sentinel.out, b'stderr')

    assert pipe('dot', 'png', b'nongraph', quiet=quiet) is mocker.sentinel.out

    Popen.assert_called_once_with(['dot', '-Tpng'],
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  startupinfo=mocker.ANY)
    check_startupinfo(Popen)
    proc.communicate.assert_called_once_with(b'nongraph')
    assert capsys.readouterr() == ('', '' if quiet else 'stderr')


@pytest.mark.usefixtures('empty_path')
def test_version_missing_executable():
    with pytest.raises(ExecutableNotFound, match=r'execute'):
        version()


@pytest.exe
def test_version(capsys):
    assert version() is not None
    assert capsys.readouterr() == ('', '')


def test_version_parsefail_mocked(mocker, Popen):
    proc = Popen.return_value
    proc.returncode = 0
    proc.communicate.return_value = (b'nonversioninfo', None)

    with pytest.raises(RuntimeError):
        version()

    Popen.assert_called_once_with(['dot', '-V'],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,
                                  startupinfo=mocker.ANY)
    check_startupinfo(Popen)
    proc.communicate.assert_called_once_with(None)


def test_version_mocked(mocker, Popen):
    proc = Popen.return_value
    proc.returncode = 0
    proc.communicate.return_value = (b'dot - graphviz version 1.2.3 (mocked)', None)

    assert version() == (1, 2, 3)

    Popen.assert_called_once_with(['dot', '-V'],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,
                                  startupinfo=mocker.ANY)
    check_startupinfo(Popen)
    proc.communicate.assert_called_once_with(None)


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

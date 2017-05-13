# test_backend.py

import subprocess

import pytest

from graphviz.backend import render, pipe, view, ExecutableNotFound, STARTUPINFO


def test_render_engine_unknown():
    with pytest.raises(ValueError) as e:
        render('', 'pdf', 'nonfilepath')
    e.match(r'engine')


def test_render_format_unknown():
    with pytest.raises(ValueError) as e:
        render('dot', '', 'nonfilepath')
    e.match(r'format')


def test_render_missingdot(empty_path):
    with pytest.raises(ExecutableNotFound) as e:
        render('dot', 'pdf', 'nonfilepath')
    e.match(r'execute')
    

@pytest.exe
def test_render_missingfile(engine='dot', format_='pdf'):
    with pytest.raises(subprocess.CalledProcessError) as e:
        render(engine, format_, '', quiet=True)
    assert e.value.returncode == 2


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


@pytest.exe
def test_render(tmpdir, engine='dot', format_='pdf', filename='hello.gv',
                data=b'digraph { hello -> world }'):
    source = tmpdir.join(filename)
    source.write(data)
    rendered = source.new(ext='%s.%s' % (source.ext, format_))

    assert render(engine, format_, str(source)) == str(rendered)
    assert rendered.size()


def test_pipe_missingdot(empty_path):
    with pytest.raises(ExecutableNotFound) as e:
        pipe('dot', 'pdf', b'nongraph')
    e.match(r'execute')


@pytest.exe
def test_pipe_invalid_data(engine='dot', format_='svg'):
    with pytest.raises(subprocess.CalledProcessError) as e:
        pipe(engine, format_, b'nongraph', quiet=True)
    assert e.value.returncode == 1


def test_pipe_mocked_fail(mocker, Popen, quiet):
    stderr = mocker.patch('sys.stderr')
    proc = Popen.return_value
    proc.returncode = mocker.sentinel.returncode
    proc.communicate.return_value = mocker.sentinel.outs, mocker.sentinel.errs

    with pytest.raises(subprocess.CalledProcessError) as e:
        pipe('dot', 'png', b'nongraph', quiet=quiet)
    assert e.value.returncode is mocker.sentinel.returncode

    Popen.assert_called_once_with(['dot', '-Tpng'],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, startupinfo=STARTUPINFO)
    proc.communicate.assert_called_once_with(b'nongraph')
    if not quiet:
        stderr.write.assert_called_once_with(mocker.sentinel.errs)
        stderr.flush.assert_called_once_with()


def test_pipe_mocked(mocker, Popen):
    proc = Popen.return_value
    proc.returncode = 0
    proc.communicate.return_value = mocker.sentinel.outs, mocker.sentinel.errs

    assert pipe('dot', 'png', b'nongraph') is mocker.sentinel.outs

    Popen.assert_called_once_with(['dot', '-Tpng'],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, startupinfo=STARTUPINFO)
    proc.communicate.assert_called_once_with(b'nongraph')


@pytest.exe
def test_pipe(svg_pattern, engine='dot', format_='svg', data=b'graph { spam }'):
    src = pipe(engine, format_, data).decode('ascii')
    assert svg_pattern.match(src)


def test_view(platform, Popen, startfile):
    if platform == 'nonplatform':
        with pytest.raises(RuntimeError) as e:
            view('nonfilepath')
        e.match(r'platform')
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

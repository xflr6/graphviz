# test_backend.py

import subprocess

import pytest


from graphviz.backend import render, pipe, view, ExecutableNotFound, STARTUPINFO


def test_render_engine_unknown():
    with pytest.raises(ValueError) as e:
        render('', 'pdf', '')
    e.match(r'engine')


def test_render_format_unknown():
    with pytest.raises(ValueError) as e:
        render('dot', '', '')
    e.match(r'format')


def test_render_missingdot(empty_path):
    with pytest.raises(ExecutableNotFound) as e:
        render('dot', 'pdf', '')
    e.match(r'execute')
    

def test_render_missingfile():
    with pytest.raises(subprocess.CalledProcessError) as e:
        render('dot', 'pdf', '')
    assert e.value.returncode == 2


def test_render_mocked(check_call):
    assert render('dot', 'pdf', '') == '.pdf'
    check_call.assert_called_once_with(['dot', '-Tpdf', '-O', ''],
                                       startupinfo=STARTUPINFO)


def test_render(check_call):
    pass  # TODO


def test_pipe_missingdot(empty_path):
    with pytest.raises(ExecutableNotFound) as e:
        pipe('dot', 'pdf', b'')
    e.match(r'execute')


def test_pipe_invalid_data():
    with pytest.raises(subprocess.CalledProcessError) as e:
        pipe('dot', 'svg', b'nongraph', quiet=True)
    assert e.value.returncode == 1


def test_pipe_mocked(Popen):
    pass  # TODO


def test_pipe(svg_pattern):
    src = pipe('dot', 'svg', b'graph { spam }').decode('ascii')
    assert svg_pattern.match(src)


def test_view(platform, Popen, startfile):
    if not platform:
        with pytest.raises(RuntimeError) as e:
            view('spam')
        e.match(r'platform')
    else:
        view('spam')
        if platform == 'darwin':
            Popen.assert_called_once_with(['open', 'spam'])
        elif platform in ('linux', 'freebsd'):
            Popen.assert_called_once_with(['xdg-open', 'spam'])
        elif platform == 'windows':
            startfile.assert_called_once_with('spam')
        else:
            raise RuntimeError

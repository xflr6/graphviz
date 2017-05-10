# test_backend.py

import subprocess

import pytest

from graphviz.backend import render, pipe, view


def test_render_engine_unknown():
    with pytest.raises(ValueError) as e:
        pipe('spam', 'pdf', b'')
    e.match(r'engine')


def test_render_format_unknown():
    with pytest.raises(ValueError) as e:
        pipe('dot', 'spam', b'')
    e.match(r'format')


def test_render_missingfile():
    with pytest.raises(subprocess.CalledProcessError) as e:
        render('dot', 'pdf', 'doesnotexist')
    assert e.value.returncode == 2


def test_pipe_invalid_data():
    with pytest.raises(subprocess.CalledProcessError) as e:
        pipe('dot', 'svg', b'spam', quiet=True)
    assert e.value.returncode == 1


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

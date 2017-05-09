# test_backend.py

import subprocess

import mock
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


@mock.patch('graphviz.backend.PLATFORM', 'spam')
def test_view_unsupported():
    with pytest.raises(RuntimeError) as e:
        view('spam')
    e.match(r'platform')


@mock.patch('graphviz.backend.PLATFORM', 'darwin')
@mock.patch('subprocess.Popen')
def test_view_darwin(Popen):
    view('spam')
    Popen.assert_called_once_with(['open', 'spam'])


@mock.patch('graphviz.backend.PLATFORM', 'linux')
@mock.patch('subprocess.Popen')
def test_view_linux(Popen):
    view('spam')
    Popen.assert_called_once_with(['xdg-open', 'spam'])


@mock.patch('graphviz.backend.PLATFORM', 'windows')
@mock.patch('os.startfile', create=True)
def test_view_windows(startfile):
    view('spam')
    startfile.assert_called_once_with('spam')

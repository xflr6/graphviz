# test_backend.py

import re
import subprocess

import pytest

from graphviz.backend import render, pipe


def test_render_filepath_missing():
    with pytest.raises(subprocess.CalledProcessError) as e:
        render('dot', 'pdf', 'doesnotexist')
    assert e.value.returncode == 2


def test_render_engine_unknown():
    with pytest.raises(ValueError) as e:
        pipe('spam', 'pdf', b'')
    e.match(r'engine')


def test_render_format_unknown():
    with pytest.raises(ValueError) as e:
        pipe('dot', 'spam', b'')
    e.match(r'format')


def test_pipe_invalid_dot():
    with pytest.raises(subprocess.CalledProcessError) as e:
        pipe('dot', 'svg', b'spam', quiet=True)
    assert e.value.returncode == 1


def test_pipe(pattern=r'(?s)^<\?xml .+</svg>\s*$'):
    src = pipe('dot', 'svg', b'graph { spam }').decode('ascii')
    assert re.match(pattern, src)

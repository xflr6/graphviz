# test_files.py

import os

import pytest

from graphviz.files import File, Source


@pytest.fixture(scope='session')
def file():
    return File('name', 'dir', 'PNG', 'NEATO', 'latin1')


@pytest.fixture
def file_noent():
    oldpath = os.environ.get('PATH')
    os.environ['PATH'] = ''
    file = File('spam.gv', 'test-output')
    file.source = 'spam'
    yield file
    if oldpath is None:
        del os.environ['PATH']
    else:
        os.environ['PATH'] = oldpath


def test_format(file):
    with pytest.raises(ValueError) as e:
        file.format = 'spam'
    e.match(r'format')


def test_engine(file):
    with pytest.raises(ValueError) as e:
        file.engine = 'spam'
    e.match(r'engine')


def test_encoding(file):
    with pytest.raises(LookupError) as e:
        file.encoding = 'spam'
    e.match(r'encoding')


def test_init(file):
    assert file.filename == 'name'
    assert file.directory == 'dir'
    assert file.format == 'png'
    assert file.engine == 'neato'
    assert file.encoding == 'latin1'


def test_pipe_noent(file_noent):
    with pytest.raises(RuntimeError) as e:
        file_noent.pipe()
    e.match(r'failed to execute')


def test_render_noent(file_noent):
    with pytest.raises(RuntimeError) as e:
        file_noent.render(directory=file_noent.directory)
    e.match(r'failed to execute')


def test_view_unknown(platform, Popen, startfile, file):
    if not platform:
        with pytest.raises(RuntimeError) as e:
            file._view('name', 'png')
        e.match(r'support')
    else:
        file._view('name', 'png')
        if platform == 'darwin':
            Popen.assert_called_once_with(['open', 'name'])
        elif platform in ('freebsd', 'linux'):
            Popen.assert_called_once_with(['xdg-open', 'name'])
        elif platform == 'windows':
            startfile.assert_called_once_with('name')
        else:
            raise RuntimeError


def test_source():
    source = 'graph { hello -> world }'
    s = Source(source)
    assert s.source == source

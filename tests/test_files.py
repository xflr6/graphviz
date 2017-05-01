# test_files.py

import os
import pytest

from graphviz.files import File, Source


@pytest.fixture(scope='session')
def file():
    f = File('name', 'dir', 'PNG', 'NEATO', 'latin1')
    assert f.filename == 'name'
    assert f.format == 'png'
    assert f.engine == 'neato'
    assert f.encoding == 'latin1'
    return f


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


def test_render_noent(file_noent):
    with pytest.raises(RuntimeError) as e:
        file_noent.render(directory=file_noent.directory)
    e.match(r'failed to execute')


def test_pipe_noent(file_noent):
    with pytest.raises(RuntimeError) as e:
        file_noent.pipe()
    e.match(r'failed to execute')


def test_source():
    source = 'graph { hello -> world }'
    s = Source(source)
    assert s.source == source

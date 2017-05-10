# test_files.py

import pytest

from graphviz.files import File, Source


@pytest.fixture(scope='module')
def source():
    return Source('graph { hello -> world }', 'hello.gv', 'test-output',
                  format='PNG', engine='NEATO', encoding='utf-8')


def test_format(source):
    with pytest.raises(ValueError) as e:
        source.format = ''
    e.match(r'format')


def test_engine(source):
    with pytest.raises(ValueError) as e:
        source.engine = ''
    e.match(r'engine')


def test_encoding(source):
    with pytest.raises(LookupError) as e:
        source.encoding = ''
    e.match(r'encoding')


def test_init(source):
    assert source.source == 'graph { hello -> world }'
    assert source.filename == 'hello.gv'
    assert source.directory == 'test-output'
    assert source.format == 'png'
    assert source.engine == 'neato'
    assert source.encoding == 'utf-8'


def test_init_filename():
    assert Source('').filename == 'Source.gv'
    assert type('Named', (Source,), {'name': 'name'})('').filename == 'name.gv'


def test_view(mocker, source):
    render = mocker.patch.object(source, 'render')
    kwargs = {'filename': 'filename', 'directory': 'directory', 'cleanup': True}
    source.view(**kwargs)
    render.assert_called_once_with(view=True, **kwargs)


def test__view(platform, Popen, startfile, source):
    if not platform:
        with pytest.raises(RuntimeError) as e:
            source._view('name', 'png')
        e.match(r'support')
    else:
        source._view('name', 'png')
        if platform == 'darwin':
            Popen.assert_called_once_with(['open', 'name'])
        elif platform in ('freebsd', 'linux'):
            Popen.assert_called_once_with(['xdg-open', 'name'])
        elif platform == 'windows':
            startfile.assert_called_once_with('name')
        else:
            raise RuntimeError

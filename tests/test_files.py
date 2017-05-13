# test_files.py

import pytest

from graphviz.files import File, Source

SOURCE = {
    'source': 'digraph { hello -> world }',
    'filename': 'hello.gv', 'directory': 'test-output',
    'format': 'PNG', 'engine': 'NEATO', 'encoding': 'utf-8',
}


@pytest.fixture(scope='module')
def source():
    return Source(**SOURCE)


def test_format(source):
    assert not SOURCE['format'].islower()

    assert source.format == SOURCE['format'].lower()
    with pytest.raises(ValueError) as e:
        source.format = ''
    e.match(r'format')


def test_engine(source):
    assert not SOURCE['engine'].islower()

    source.engine == SOURCE['engine'].lower()
    with pytest.raises(ValueError) as e:
        source.engine = ''
    e.match(r'engine')


def test_encoding(source):
    assert source.encoding == SOURCE['encoding']

    with pytest.raises(LookupError) as e:
        source.encoding = ''
    e.match(r'encoding')


def test_init(source):
    assert source.source == SOURCE['source']
    assert source.filename == SOURCE['filename']
    assert source.directory == SOURCE['directory']


def test_init_filename():
    assert Source('').filename == 'Source.gv'
    assert type('Named', (Source,), {'name': 'name'})('').filename == 'name.gv'


def test__repr_svg_(mocker, source):
    pipe = mocker.patch.object(source, 'pipe')

    result = source._repr_svg_()

    pipe.assert_called_once_with(format='svg')
    pipe.return_value.decode.assert_called_once_with(source.encoding)
    assert result is pipe.return_value.decode.return_value


def test_pipe_format(pipe, source, format_='svg'):
    assert source.format != format_

    result = source.pipe(format=format_)

    data = source.source.encode(source.encoding)
    pipe.assert_called_once_with(source.engine, format_, data)
    assert result is pipe.return_value


def test_pipe(pipe, source):
    result = source.pipe()

    data = source.source.encode(source.encoding)
    pipe.assert_called_once_with(source.engine, source.format, data)
    assert result is pipe.return_value


def test_filepath(source):
    assert source.filepath in ('test-output/hello.gv', 'test-output\\hello.gv')


def test_save(mocker, py2, filename='filename', directory='directory'):
    source = Source(**SOURCE)
    makedirs = mocker.patch('os.makedirs')
    open = mocker.patch('io.open')

    result = source.save(filename, directory)

    assert source.filename == filename and source.directory == directory
    if py2:
        makedirs.assert_called_once_with(source.directory, 0o777)
    else:
        makedirs.assert_called_once_with(source.directory, 0o777, exist_ok=True)
    open.assert_called_once_with(source.filepath, 'w', encoding=source.encoding)
    fd = open.return_value.__enter__.return_value
    assert len(fd.write.mock_calls) == 2
    fd.write.assert_has_calls([mocker.call(source.source), mocker.call(u'\n')])
    assert result == source.filepath
    

def test_render(mocker, render, source):
    save = mocker.patch.object(source, 'save')
    _view = mocker.patch.object(source, '_view')
    remove = mocker.patch('os.remove')

    result = source.render(cleanup=True, view=True)

    save.assert_called_once_with(None, None)
    render.assert_called_once_with(source.engine, source.format, save.return_value)
    remove.assert_called_once_with(save.return_value)
    _view.assert_called_once_with(result, source.format)
    assert result is render.return_value
    

def test_view(mocker, source):
    render = mocker.patch.object(source, 'render')
    kwargs = {'filename': 'filename', 'directory': 'directory', 'cleanup': True}

    source.view(**kwargs)

    render.assert_called_once_with(view=True, **kwargs)


def test__view(mocker, platform, source):
    if platform == 'nonplatform':
        with pytest.raises(RuntimeError) as e:
            source._view('name', 'png')
        e.match(r'support')
    else:
        _view_platform = mocker.patch.object(source, '_view_%s' % platform)

        source._view('name', 'png')

        _view_platform.assert_called_once_with('name')


def test_copy(source):
    assert source.copy() is not source
    assert source.copy() is not source.copy()
    assert source.copy().__class__ is source.__class__
    assert source.copy().__dict__ == source.__dict__

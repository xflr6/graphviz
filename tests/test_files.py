# test_files.py

import locale

import pytest

from graphviz.files import Source

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
    with pytest.raises(ValueError, match=r'format'):
        source.format = ''


def test_engine(source):
    assert not SOURCE['engine'].islower()

    assert source.engine == SOURCE['engine'].lower()
    with pytest.raises(ValueError, match=r'engine'):
        source.engine = ''


def test_encoding(source):
    assert source.encoding == SOURCE['encoding']

    with pytest.raises(LookupError, match=r'encoding'):
        source.encoding = ''


def test_encoding_none(source):
    source_copy = source.copy()
    source_copy.encoding = None
    assert source_copy.encoding == locale.getpreferredencoding()


def test_init(source):
    assert source.source == SOURCE['source']
    assert source.filename == SOURCE['filename']
    assert source.directory == SOURCE['directory']


def test_init_filename():
    assert Source('').filename == 'Source.gv'
    assert type('Named', (Source,), {'name': 'name'})('').filename == 'name.gv'


def test__repr_svg_(mocker, source):
    kwargs = {'return_value.decode.return_value': mocker.sentinel.decoded}
    pipe = mocker.patch.object(source, 'pipe', new_callable=mocker.Mock, **kwargs)

    assert source._repr_svg_() is mocker.sentinel.decoded

    pipe.assert_called_once_with(format='svg')
    pipe.return_value.decode.assert_called_once_with(source.encoding)


def test_pipe_format(pipe, source, format_='svg'):
    assert source.format != format_

    assert source.pipe(format=format_) is pipe.return_value

    data = source.source.encode(source.encoding)
    pipe.assert_called_once_with(source.engine, format_, data, None, None)


def test_pipe(pipe, source):
    assert source.pipe() is pipe.return_value

    data = source.source.encode(source.encoding)
    pipe.assert_called_once_with(source.engine, source.format, data, None, None)


def test_filepath(test_platform, source):
    if test_platform == 'windows':
        assert source.filepath == 'test-output\\hello.gv'
    else:
        assert source.filepath == 'test-output/hello.gv'


def test_save(mocker, py2, filename='filename', directory='directory'):
    source = Source(**SOURCE)
    makedirs = mocker.patch('os.makedirs', new_callable=mocker.Mock)
    open_ = mocker.patch('io.open', mocker.mock_open())

    assert source.save(filename, directory) == source.filepath

    assert source.filename == filename and source.directory == directory
    if py2:
        makedirs.assert_called_once_with(source.directory, 0o777)
    else:
        makedirs.assert_called_once_with(source.directory, 0o777, exist_ok=True)
    open_.assert_called_once_with(source.filepath, 'w', encoding=source.encoding)
    assert open_.return_value.write.call_args_list == [((source.source,),), ((u'\n',),)]


def test_render(mocker, render, source):
    save = mocker.patch.object(source, 'save', new_callable=mocker.Mock)
    _view = mocker.patch.object(source, '_view', new_callable=mocker.Mock)
    remove = mocker.patch('os.remove', new_callable=mocker.Mock)

    assert source.render(cleanup=True, view=True) is render.return_value

    save.assert_called_once_with(None, None)
    render.assert_called_once_with(source.engine, source.format, save.return_value, None, None)
    remove.assert_called_once_with(save.return_value)
    _view.assert_called_once_with(render.return_value, source.format)


def test_view(mocker, source):
    render = mocker.patch.object(source, 'render', new_callable=mocker.Mock)
    kwargs = {'filename': 'filename', 'directory': 'directory', 'cleanup': True}

    assert source.view(**kwargs) is render.return_value

    render.assert_called_once_with(view=True, **kwargs)


def test__view(mocker, platform, source):
    if platform == 'nonplatform':
        with pytest.raises(RuntimeError, match=r'support'):
            source._view('name', 'png')
    else:
        _view_platform = mocker.patch.object(source, '_view_%s' % platform,
                                             new_callable=mocker.Mock)

        assert source._view(mocker.sentinel.name, 'png') is None

        _view_platform.assert_called_once_with(mocker.sentinel.name)


def test_copy(source):
    assert source.copy() is not source
    assert source.copy() is not source.copy()
    assert source.copy().__class__ is source.__class__
    assert source.copy().__dict__ == source.__dict__


def test_from_file(tmpdir, filename='hello.gv', directory='source_hello',
                   data=u'digraph { hello -> world }', encoding='utf-8'):
    lpath = tmpdir.mkdir(directory)
    (lpath / filename).write_text(data, encoding=encoding)

    source = Source.from_file(filename, str(lpath))
    assert source.encoding == 'utf-8'

    source = Source.from_file(filename, str(lpath), encoding=None)
    assert source.encoding == locale.getpreferredencoding()

    source = Source.from_file(filename, str(lpath), encoding=encoding)
    assert source.source == data
    assert source.filename == filename
    assert source.directory == str(lpath)
    assert source.encoding == encoding

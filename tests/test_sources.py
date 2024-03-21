import locale

import pytest

import graphviz

SOURCE = {'source': 'digraph { hello -> world }\n',
          'filename': 'hello.gv', 'directory': 'test-output',
          'format': 'PNG', 'engine': 'NEATO', 'encoding': 'utf-8'}


@pytest.fixture(scope='module')
def source():
    return graphviz.Source(**SOURCE)


@pytest.mark.parametrize(
    'parameter', ['engine', 'format', 'encoding'])
def test_source_parameter(source, parameter):
    if parameter != 'encoding':
        assert not SOURCE[parameter].islower()
    assert getattr(source, parameter) == SOURCE[parameter].lower()


def test_init(source):
    assert source.source == SOURCE['source']
    assert source.filename == SOURCE['filename']
    assert source.directory == SOURCE['directory']


def test_init_filename():
    assert graphviz.Source('').filename == 'Source.gv'
    assert type('Subcls', (graphviz.Source,),
                {'name': 'name'})('').filename == 'Subcls.gv'


def test_filepath(platform, source):
    if platform == 'windows':
        assert source.filepath == 'test-output\\hello.gv'
    else:
        assert source.filepath == 'test-output/hello.gv'


def test_from_file(tmp_path, filename='hello.gv', directory='source_hello',
                   data='digraph { hello -> world }', encoding='utf-8'):
    lpath = tmp_path / directory
    lpath.mkdir()
    (lpath / filename).write_text(data, encoding=encoding)

    with pytest.deprecated_call():
        source = graphviz.Source.from_file(filename, str(lpath))
    assert source.encoding == 'utf-8'

    with pytest.deprecated_call():
        source = graphviz.Source.from_file(filename, str(lpath), encoding=None)
    assert source.encoding == locale.getpreferredencoding()

    renderer = 'xdot'
    formatter = 'core'
    with pytest.deprecated_call():
        source = graphviz.Source.from_file(filename, str(lpath),
                                           encoding=encoding,
                                           renderer=renderer,
                                           formatter=formatter)
    assert source.source == data + '\n'
    assert source.filename == filename
    assert source.directory == str(lpath)
    assert source.encoding == encoding
    assert source.renderer == renderer
    assert source.formatter == formatter


def test_source_iter(source):
    source_without_newline = graphviz.Source(source.source + source.source.rstrip())
    lines = list(source_without_newline)

    assert lines == list(source) * 2

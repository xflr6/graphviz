import locale
import re

import pytest


import graphviz

ALL_CLASSES = [graphviz.Graph, graphviz.Digraph, graphviz.Source]


@pytest.fixture(params=ALL_CLASSES)
def cls(request):
    return request.param


@pytest.fixture
def dot(cls):
    if cls.__name__ == 'Source':
        return cls('digraph { hello -> world }\n')
    return cls()


def test_copy(cls, dot):
    assert type(dot) is cls
    assert dot.copy() is not dot
    assert dot.copy() is not dot.copy()
    assert type(dot.copy()) is type(dot)
    assert dot.copy().__dict__ == dot.__dict__ == dot.copy().__dict__


def test_str(dot):
    assert str(dot) == dot.source


@pytest.mark.parametrize(
    'parameter, expected_exception, match',
    [('engine', ValueError, r'unknown engine'),
     ('format', ValueError, r'unknown format'),
     ('renderer', ValueError, r'unknown renderer'),
     ('formatter', ValueError, r'unknown formatter'),
     ('encoding', LookupError, r'encoding')])
def test_invalid_parameter_raises_valuerror(dot, parameter,
                                            expected_exception, match):
    with pytest.raises(expected_exception, match=match):
        setattr(dot, parameter, 'invalid_parameter')


def test_encoding_none(dot):
    dot_copy = dot.copy()
    dot_copy.encoding = None
    assert dot_copy.encoding == locale.getpreferredencoding()


@pytest.mark.exe
@pytest.mark.parametrize(
    'kwargs', [{'engine': 'spam'}])
def test_render_raises_before_save(tmp_path, cls, kwargs, filename='dot.gv'):
    args = ['graph { spam }'] if cls.__name__ == 'Source' else []
    dot = cls(*args, filename=filename, directory=tmp_path)
    expected_source = tmp_path / filename
    assert not expected_source.exists()

    with pytest.raises(ValueError, match=r''):
        dot.render(**kwargs)

    assert not expected_source.exists()

    pdf = dot.render(engine='dot')

    assert pdf == f'{expected_source}.pdf'
    assert expected_source.exists()
    assert expected_source.stat().st_size


@pytest.mark.parametrize(
    'kwargs',
    [{'engine': 'spam'}, {'format': 'spam'},
     {'renderer': 'spam'}, {'formatter': 'spam'}])
def test_render_raises_before_save_mocked(tmp_path, mock_render, cls, kwargs,
                                          filename='dot.gv'):
    args = [''] if cls.__name__ == 'Source' else []
    dot = cls(*args, filename=filename, directory=tmp_path)

    expected_source = tmp_path / filename
    assert not expected_source.exists()

    first_arg = next(iter(kwargs))
    with pytest.raises(ValueError, match=f'unknown {first_arg}'):
        dot.render(**kwargs)

    assert not expected_source.exists()


def test_format_renderer_formatter_mocked(mocker, mock_render,
                                          quiet, cls,
                                          filename='format.gv', format='jpg',
                                          renderer='cairo', formatter='core'):
    args = [''] if cls.__name__ == 'Source' else []
    dot = cls(*args, filename=filename, format=format,
              renderer=renderer, formatter=formatter)

    assert dot.format == format
    assert dot.renderer == renderer
    assert dot.formatter == formatter

    mock_save = mocker.patch.object(dot, 'save', autospec=True)

    assert dot.render(quiet=quiet) is mock_render.return_value

    mock_save.assert_called_once_with(None, None, skip_existing=None)
    mock_render.assert_called_once_with('dot', format, mock_save.return_value,
                                        renderer=renderer, formatter=formatter,
                                        quiet=quiet)


@pytest.mark.parametrize(
    'encoding', [None, 'ascii', 'utf-8'])
def test_pipe_mocked(mocker, mock_pipe_lines, mock_pipe_lines_string, quiet,
                     dot, encoding):
    input_encoding = 'utf-8'
    dot.encoding = input_encoding

    result = dot.pipe(encoding=encoding, quiet=quiet)

    expected_args = ['dot', 'pdf', mocker.ANY]
    expected_kwargs = {'quiet': quiet,
                       'renderer': None,
                       'formatter': None}

    if encoding == input_encoding:
        assert result is mock_pipe_lines_string.return_value
        mock_pipe_lines_string.assert_called_once_with(*expected_args,
                                                       encoding=encoding,
                                                       **expected_kwargs)
        return

    if encoding is None:
        assert result is mock_pipe_lines.return_value
    else:
        assert result is mock_pipe_lines.return_value.decode.return_value
        mock_pipe_lines.return_value.decode.assert_called_once_with(encoding)
    mock_pipe_lines.assert_called_once_with(*expected_args,
                                            input_encoding=input_encoding,
                                            **expected_kwargs)


def test_repr_svg_mocked(mocker, dot):
    mock_pipe = mocker.patch.object(dot, 'pipe', autospec=True)

    assert dot._repr_svg_() is mock_pipe.return_value

    mock_pipe.assert_called_once_with(format='svg', encoding=dot.encoding)


@pytest.mark.exe
def test_unflatten(cls, dot):
    result = dot.unflatten()
    assert isinstance(result, graphviz.Source)

    normalized = re.sub(r'\s+', ' ', result.source.strip())
    if cls.__name__ == 'Source':
        assert normalized == 'digraph { hello -> world; }'
    else:
        assert normalized.startswith('digraph {' if dot.directed else 'graph {')


def test_unflatten_mocked(sentinel, mock_unflatten, dot):
    kwargs = {'stagger': sentinel.stagger,
              'fanout': sentinel.fanout,
              'chain': sentinel.chain}
    result = dot.unflatten(**kwargs)

    assert result is not None
    assert isinstance(result, graphviz.Source)
    assert type(result) is graphviz.Source
    assert result.source is mock_unflatten.return_value

    assert result.filename == dot.filename
    assert result.directory == dot.directory
    assert result.engine == dot.engine
    assert result.format == dot.format
    assert result.renderer == dot.renderer
    assert result.formatter == dot.formatter
    assert result.encoding == dot.encoding
    assert result._loaded_from_path is None

    mock_unflatten.assert_called_once_with(dot.source,
                                           encoding=dot.encoding,
                                           **kwargs)


def test_view_mocked(mocker, dot):
    mock_render = mocker.patch.object(dot, 'render', autospec=True)
    kwargs = {'filename': 'filename', 'directory': 'directory',
              'cleanup': True, 'quiet': True, 'quiet_view': True}

    assert dot.view(**kwargs) is mock_render.return_value

    mock_render.assert_called_once_with(view=True, **kwargs)


def test__view_unknown_platform(unknown_platform, dot):
    with pytest.raises(RuntimeError, match=r'support'):
        dot._view('name', 'png', False)


def test__view_mocked(mocker, sentinel, mock_platform, dot):
    _view_platform = mocker.patch.object(dot, f'_view_{mock_platform}',
                                         autospec=True)

    kwargs = {'quiet': False}

    assert dot._view(sentinel.name, 'png', **kwargs) is None

    _view_platform.assert_called_once_with(sentinel.name, **kwargs)

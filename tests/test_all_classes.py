import locale
import pathlib
import re
import subprocess

import pytest

import graphviz

import _common

ALL_CLASSES = [graphviz.Graph, graphviz.Digraph, graphviz.Source]


@pytest.fixture(params=ALL_CLASSES)
def cls(request):
    return request.param


@pytest.fixture
def dot(cls):
    if cls.__name__ == 'Source':
        return cls('digraph { hello -> world }\n')
    return cls()


@pytest.fixture
def invalid_dot(cls):
    if cls.__name__ == 'Source':
        return cls('graph { spam -- \\ }')
    else:
        invalid_dot = cls()
        with pytest.warns(graphviz.DotSyntaxWarning, match=r'syntax error'):
            invalid_dot.edge('spam', '\\')
        return invalid_dot


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


def test_render_mocked(mocker, mock_render, dot):
    mock_save = mocker.patch.object(dot, 'save', autospec=True)
    mock_view = mocker.patch.object(dot, '_view', autospec=True)
    mock_remove = mocker.patch('os.remove', autospec=True)

    assert dot.render(cleanup=True, view=True) is mock_render.return_value

    mock_save.assert_called_once_with(None, None, skip_existing=None)
    mock_render.assert_called_once_with(dot.engine, dot.format,
                                        mock_save.return_value,
                                        renderer=None, formatter=None,
                                        neato_no_op=None,
                                        outfile=None,
                                        raise_if_result_exists=False,
                                        overwrite_filepath=False,
                                        quiet=False)
    mock_remove.assert_called_once_with(mock_save.return_value)
    mock_view.assert_called_once_with(mock_render.return_value,
                                      format=dot.format, quiet=False)


def test_render_outfile_mocked(mocker, mock_render, dot):
    mock_save = mocker.patch.object(dot, 'save', autospec=True)
    mock_view = mocker.patch.object(dot, '_view', autospec=True)
    mock_remove = mocker.patch('os.remove', autospec=True)

    outfile = 'spam.pdf'

    assert dot.render(outfile=outfile,
                      raise_if_result_exists=True,
                      overwrite_source=True,
                      cleanup=True, view=True) is mock_render.return_value

    expected_filename = pathlib.Path('spam.gv')

    mock_save.assert_called_once_with(expected_filename, None, skip_existing=None)
    mock_render.assert_called_once_with(dot.engine, dot.format,
                                        mock_save.return_value,
                                        renderer=None, formatter=None,
                                        neato_no_op=None,
                                        outfile=pathlib.Path(outfile),
                                        raise_if_result_exists=True,
                                        overwrite_filepath=True,
                                        quiet=False)
    mock_remove.assert_called_once_with(mock_save.return_value)
    mock_view.assert_called_once_with(mock_render.return_value,
                                      format=dot.format, quiet=False)


def test_format_renderer_formatter_mocked(mocker, mock_render,
                                          quiet, cls,
                                          filename='format.gv', format='jpg',
                                          renderer='cairo', formatter='core'):
    dot = cls(*[''] if cls.__name__ == 'Source' else [],
              filename=filename, format=format,
              renderer=renderer, formatter=formatter)

    assert dot.format == format
    assert dot.renderer == renderer
    assert dot.formatter == formatter

    mock_save = mocker.patch.object(dot, 'save', autospec=True)

    assert dot.render(quiet=quiet) is mock_render.return_value

    mock_save.assert_called_once_with(None, None, skip_existing=None)
    mock_render.assert_called_once_with('dot', format, mock_save.return_value,
                                        renderer=renderer, formatter=formatter,
                                        neato_no_op=None,
                                        outfile=None,
                                        raise_if_result_exists=False,
                                        overwrite_filepath=False,
                                        quiet=quiet)


@pytest.mark.parametrize(
    'neato_no_op', [None, False, True, 0, 1, 2])
def test_neato_no_op_mocked(mocker, mock_render,
                            quiet, cls, neato_no_op,
                            engine='neato',
                            filename='neato_no_op.gv', format='svg'):
    dot = cls(*[''] if cls.__name__ == 'Source' else [],
              engine=engine,
              filename=filename, format=format)

    mock_save = mocker.patch.object(dot, 'save', autospec=True)

    assert dot.render(neato_no_op=neato_no_op,
                      quiet=quiet) is mock_render.return_value

    mock_save.assert_called_once_with(None, None, skip_existing=None)
    mock_render.assert_called_once_with(engine, format, mock_save.return_value,
                                        renderer=None, formatter=None,
                                        neato_no_op=neato_no_op,
                                        outfile=None,
                                        raise_if_result_exists=False,
                                        overwrite_filepath=False,
                                        quiet=quiet)


def test_save_mocked(mocker, dot, filename='nonfilename', directory='nondirectory'):
    mock_makedirs = mocker.patch('os.makedirs', autospec=True)
    mock_open = mocker.patch('builtins.open', mocker.mock_open())

    with pytest.deprecated_call():
        assert dot.save(filename, directory) == dot.filepath

    assert dot.filename == filename
    assert dot.directory == directory
    mock_makedirs.assert_called_once_with(dot.directory, 0o777, exist_ok=True)
    mock_open.assert_called_once_with(dot.filepath, 'w',
                                      encoding=dot.encoding)
    expected_calls = ([mocker.call(dot.source)] if type(dot).__name__ == 'Source'
                      else [mocker.call(mocker.ANY), mocker.call('}\n')])
    assert mock_open.return_value.write.call_args_list == expected_calls


@pytest.mark.exe
def test_pipe(dot, encoding='utf-8'):
    svg = dot.pipe(format='svg', encoding=encoding)
    assert svg.startswith('<?xml ')


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
                       'formatter': None,
                       'neato_no_op': None}

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


def test_pipe_lines_mocked(mocker, mock_pipe_lines, dot, format_='svg'):
    assert dot.format != format_

    assert dot.pipe(format=format_) is mock_pipe_lines.return_value

    mock_pipe_lines.assert_called_once_with(dot.engine, format_, mocker.ANY,
                                            renderer=None, formatter=None,
                                            neato_no_op=None,
                                            input_encoding='utf-8',
                                            quiet=False)
    _, _, data = mock_pipe_lines.call_args.args
    expected_lines = dot.source.splitlines(keepends=True)
    assert list(data) == expected_lines


@pytest.mark.exe
def test_pipe_lines_called_process_error(invalid_dot, encoding='ascii',
                                         input_encoding='utf-8'):
    _test_pipe_lines_called_process_error(invalid_dot,
                                          format='svg',
                                          encoding=encoding,
                                          input_encoding=input_encoding,
                                          expected_syntax_error='syntax error')


def _test_pipe_lines_called_process_error(invalid_dot, *,
                                          format, encoding, input_encoding,
                                          expected_syntax_error):
    assert encoding != input_encoding

    invalid_dot.encoding = input_encoding

    with pytest.raises(graphviz.CalledProcessError,
                       match=expected_syntax_error) as info:
        invalid_dot.pipe(format=format, encoding=encoding)

    assert isinstance(info.value, subprocess.CalledProcessError)
    assert isinstance(info.value, graphviz.CalledProcessError)
    assert isinstance(info.value.stderr, str)
    assert expected_syntax_error in info.value.stderr


def test_pipe_lines_called_process_error_mocked(invalid_dot,
                                                mocker, mock_pipe_lines,
                                                encoding='ascii',
                                                input_encoding='utf-8'):
    format = 'svg'

    expected_syntax_error = 'syntax error'
    expected_syntax_error = f'fake {expected_syntax_error}'

    fake_error = [1, _common.INVALID_CMD,
                  b'', expected_syntax_error.encode(input_encoding)]
    fake_error = graphviz.CalledProcessError(*fake_error)
    mock_pipe_lines.side_effect = fake_error

    _test_pipe_lines_called_process_error(invalid_dot,
                                          format=format,
                                          encoding=encoding,
                                          input_encoding=input_encoding,
                                          expected_syntax_error=expected_syntax_error)

    mock_pipe_lines.assert_called_once_with(_common.EXPECTED_DEFAULT_ENGINE,
                                            format,
                                            mocker.ANY,
                                            input_encoding=input_encoding,
                                            quiet=False,
                                            renderer=None,
                                            formatter=None,
                                            neato_no_op=None)


def test_repr_mimebundle_image_svg_xml_mocked(mocker, dot):
    mock_pipe = mocker.patch.object(dot, 'pipe', autospec=True)

    assert dot._repr_mimebundle_({'image/svg+xml'}) == {'image/svg+xml': mock_pipe.return_value}

    mock_pipe.assert_called_once_with(format='svg', encoding=dot.encoding)


def test_repr_mimebundle_image_png_mocked(mocker, dot):
    mock_pipe = mocker.patch.object(dot, 'pipe', autospec=True)

    assert dot._repr_mimebundle_({'image/png'}) == {'image/png': mock_pipe.return_value}

    mock_pipe.assert_called_once_with(format='png')


def test_repr_mimebundle_image_jpeg_mocked(mocker, dot):
    mock_pipe = mocker.patch.object(dot, 'pipe', autospec=True)

    assert dot._repr_mimebundle_({'image/jpeg'}) == {'image/jpeg': mock_pipe.return_value}

    mock_pipe.assert_called_once_with(format='jpeg')


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
        dot._view('name', format='png', quiet=False)


def test__view_mocked(mocker, sentinel, mock_platform, dot):
    _view_platform = mocker.patch.object(dot, f'_view_{mock_platform}',
                                         autospec=True)

    kwargs = {'quiet': False}

    assert dot._view(sentinel.name, format='png', **kwargs) is None

    _view_platform.assert_called_once_with(sentinel.name, **kwargs)

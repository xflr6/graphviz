import pytest

import graphviz
from graphviz import jupyter_integration

EXPECTED_SVG_ENCODING = 'utf-8'


def test_get_jupyter_format_mimetype_invalid_raises_unknown():
    with pytest.raises(ValueError, match=r'unknown'):
        jupyter_integration.get_jupyter_format_mimetype('Brian!')


def test_get_jupyter_mimetype_format_normalizes():
    assert jupyter_integration.get_jupyter_mimetype_format(
        jupyter_integration.get_jupyter_format_mimetype('jpg')) == 'jpeg'


def test_get_jupyter_mimetype_format_raises_unsupported():
    with pytest.raises(ValueError,
                       match=r"unsupported .*\(must be one of .+'image/svg\+xml'"):
        jupyter_integration.get_jupyter_mimetype_format('A boy called Brian!')


@pytest.mark.exe
def test_repr_image_svg_xml_encoding(input_encoding='latin1'):
    assert input_encoding != EXPECTED_SVG_ENCODING
    dot = graphviz.Graph(comment='Mønti Pythøn ik den Hølie Grailen',
                         encoding=input_encoding)

    result = dot._repr_image_svg_xml()

    assert result.startswith('<?xml version="1.0" encoding="UTF-8" standalone="no"?>')


@pytest.mark.exe
@pytest.mark.parametrize('input_encoding', ['utf-8', 'ascii', 'latin1'])
def test_repr_image_svg_xml_encoding_mocked(mocker, mock_pipe_lines_string,
                                            mock_pipe_lines, input_encoding):
    dot = graphviz.Graph(encoding=input_encoding)

    result = dot._repr_image_svg_xml()

    if input_encoding == 'utf-8':
        assert result is mock_pipe_lines_string.return_value

        mock_pipe_lines_string.assert_called_once()
        mock_pipe_lines.assert_not_called()

        assert (mock_pipe_lines_string.call_args.kwargs['encoding']
                == EXPECTED_SVG_ENCODING)
    else:
        assert result is mock_pipe_lines.return_value.decode.return_value

        mock_pipe_lines.assert_called_once()
        mock_pipe_lines_string.assert_not_called()

        assert 'encoding' not in mock_pipe_lines.call_args.kwargs
        (mock_pipe_lines.return_value.decode
         .assert_called_once_with(EXPECTED_SVG_ENCODING))

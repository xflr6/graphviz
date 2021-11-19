import pytest

from graphviz import jupyter_integration


def test_get_jupyter_format_mimetype_invalid_raises_unknown():
    with pytest.raises(ValueError, match=r'unknown'):
        jupyter_integration.get_jupyter_format_mimetype('Brian!')


def test_get_jupyter_mimetype_format_normalizes():
    assert jupyter_integration.get_jupyter_mimetype_format(
        jupyter_integration.get_jupyter_format_mimetype('jpg')) == 'jpeg'


def test_get_jupyter_mimetype_format_raises_unsupported():
    with pytest.raises(ValueError, match='unsupported'):
        jupyter_integration.get_jupyter_mimetype_format('A boy called Brian!')

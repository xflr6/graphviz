import locale
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
    'attribute, match',
    [('engine', r'unknown engine'),
     ('format', r'unknown format'),
     ('renderer', r'unknown renderer'),
     ('formatter', r'unknown formatter')])
def test_invalid_parameter_raises_valuerror(dot, attribute, match):
    with pytest.raises(ValueError, match=match):
        setattr(dot, attribute, 'invalid_parameter')


def test_encoding_none(dot):
    dot_copy = dot.copy()
    dot_copy.encoding = None
    assert dot_copy.encoding == locale.getpreferredencoding()


def test_repr_svg_mocked(mocker, dot):
    mock_pipe = mocker.patch.object(dot, 'pipe', autospec=True)

    assert dot._repr_svg_() is mock_pipe.return_value

    mock_pipe.assert_called_once_with(format='svg', encoding=dot.encoding)

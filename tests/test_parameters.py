import pytest

import graphviz
from graphviz import parameters

VERIFY_FUNCS = [parameters.verify_engine,
                parameters.verify_format,
                parameters.verify_renderer,
                parameters.verify_formatter]


@pytest.mark.parametrize(
    'cls', [graphviz.Graph, graphviz.Digraph, graphviz.Source])
def test_parameters(cls, engine='patchwork', format='tiff',
                    renderer='map', formatter='core'):
    args = [''] if cls is graphviz.Source else []
    dot = cls(*args,
              engine=engine, format=format,
              renderer=renderer, formatter=formatter)

    assert isinstance(dot, cls)
    assert type(dot) is cls

    assert dot.engine == engine
    assert dot.format == format
    assert dot.renderer == renderer
    assert dot.formatter == formatter

    dot_copy = dot.copy()

    assert dot_copy is not dot
    assert isinstance(dot_copy, cls)
    assert type(dot_copy) is cls

    assert dot.engine == engine
    assert dot.format == format
    assert dot_copy.renderer == renderer
    assert dot_copy.formatter == formatter


@pytest.mark.parametrize(
    'verify_func', VERIFY_FUNCS)
def test_verify_parameter_raises_unknown(verify_func):
    with pytest.raises(ValueError, match=r'unknown .*\(must be .*one of'):
        verify_func('Brian!')


@pytest.mark.parametrize(
    'verify_func', VERIFY_FUNCS)
def test_verify_parameter_none_required_false_passes(verify_func):
    assert verify_func(None, required=False) is None


@pytest.mark.parametrize(
    'verify_func', VERIFY_FUNCS)
def test_verify_parameter_none_required_raises_missing(verify_func):
    with pytest.raises(ValueError, match=r'missing'):
        verify_func(None, required=True)

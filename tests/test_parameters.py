import pytest

import graphviz


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

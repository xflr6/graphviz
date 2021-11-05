import pytest

import graphviz


@pytest.fixture(params=[graphviz.Graph, graphviz.Digraph, graphviz.Source],
                scope='module')
def cls(request):
    return request.param


def test_renderer_formatter(cls, renderer='map', formatter='core'):
    args = [''] if cls is graphviz.Source else []
    dot = cls(*args, renderer=renderer, formatter=formatter)

    assert isinstance(dot, cls)
    assert type(dot) is cls

    assert dot.renderer == renderer
    assert dot.formatter == formatter

    dot_copy = dot.copy()

    assert dot_copy is not dot
    assert isinstance(dot_copy, cls)
    assert type(dot_copy) is cls

    assert dot_copy.renderer == renderer
    assert dot_copy.formatter == formatter

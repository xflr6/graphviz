#!/usr/bin/env python3

"""graphviz.(Di)graph instance transformation: LazyGraph and LazyDigraph."""

import functools
from unittest import mock

import graphviz

WRAPS = ['Graph', 'Digraph']

RENDERING_METHODS = ('pipe', 'save', 'render', 'view', 'unflatten')

INPUT_PROPERTIES = ('source',)

__all__ = ['LazyGraph', 'LazyDigraph']


def lazy_graph_cls(wrapped_cls_name: str):
    return functools.partial(create_lazy_graph_instance, wrapped_cls_name)


def create_lazy_graph_instance(cls_name: str,
                               *init_args,
                               **init_kwargs) -> mock.NonCallableMagicMock:
    cls = getattr(graphviz, cls_name)
    if cls not in (graphviz.Graph, graphviz.Digraph):
        raise ValueError(f'cls_name: {cls_name!r}')

    fake = mock.create_autospec(cls, instance=True, spec_set=True)

    fake.copy.side_effect = NotImplementedError  # TODO

    def make_real_inst(calls):
        dot = cls(*init_args, **init_kwargs)
        for method_name, args, kwargs in calls:
            method = getattr(dot, method_name)
            method(*args, **kwargs)  # ignore return value
        return dot

    def make_methodcaller(method_name):
        def call_method(*args, **kwargs):
            last_call = fake.mock_calls.pop()
            assert last_call == getattr(mock.call, method_name)(*args, **kwargs)

            dot = make_real_inst(fake.mock_calls)
            method = getattr(dot, method_name)
            return method(*args, **kwargs)

        return call_method

    for method_name in RENDERING_METHODS:
        getattr(fake, method_name).side_effect = make_methodcaller(method_name)

    def make_property(property_name):
        def property_func(*args):
            last_call = property_mock.mock_calls.pop()
            assert last_call == mock.call(*args)
            assert not property_mock.mock_calls

            dot = make_real_inst(fake.mock_calls)
            property_obj = getattr(dot.__class__, property_name)
            property_func = property_obj.fset if args else property_obj.fget
            return property_func(dot, *args)

        property_mock = mock.PropertyMock(side_effect=property_func)
        return property_mock

    for property_name in INPUT_PROPERTIES:
        setattr(type(fake), property_name, make_property(property_name))

    return fake


LazyGraph, LazyDigraph = map(lazy_graph_cls, WRAPS)


if __name__ == '__main__':
    dot = LazyDigraph(filename='round-table.gv', comment='The Round Table')

    dot.node('A', 'King Arthur')
    dot.node('B', 'Sir Bedevere the Wise')
    dot.node('L', 'Sir Lancelot the Brave')

    dot.edges(['AB', 'AL'])
    dot.edge('B', 'L', constraint='false')

    print(repr(dot), dot.mock_calls, dot.source, sep='\n')
    #dot.view()  # noqa: E265

    def transform(mock_calls):
        """Replace full name labels with first names."""
        for call in mock_calls:
            method_name, args, kwargs = call
            if method_name == 'node':
                name, label = args
                label = label.split()[1]
                yield mock.call.node(name, label, **kwargs)
            else:
                yield call

    dot.mock_calls = list(transform(dot.mock_calls))

    # reverse the Bedvedere -> Lancelot edge
    method_name, tail_head, edge_attrs = dot.mock_calls.pop()
    assert method_name == 'edge'
    dot.edge(*reversed(tail_head), **edge_attrs)

    print(repr(dot), dot.mock_calls, dot.source, sep='\n')
    #dot.view('round-table-transformed.gv')  # noqa: E265

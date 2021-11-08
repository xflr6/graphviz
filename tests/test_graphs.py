import itertools
import re

import pytest

import graphviz

BASE_GRAPHS = [graphviz.Graph, graphviz.Digraph]


@pytest.fixture(params=BASE_GRAPHS)
def cls(request):
    return request.param


@pytest.fixture(params=list(itertools.permutations(BASE_GRAPHS, 2)),
                ids=lambda c: f'{c[0].__name__}, {c[1].__name__}')
def classes(request):
    return request.param


def test_format_renderer_formatter_mocked(mocker, mock_render,
                                          quiet, cls,
                                          filename='format.gv', format='jpg',
                                          renderer='cairo', formatter='core'):

    dot = cls(filename=filename, format=format,
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
def test_pipe_mocked(mocker, mock_pipe_lines, mock_pipe_lines_string, quiet, cls, encoding):
    input_encoding = 'utf-8'
    dot = cls(encoding=input_encoding)

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


@pytest.mark.exe
def test_unflatten(cls):
    c = cls()
    result = c.unflatten()
    assert isinstance(result, graphviz.Source)

    normalized = re.sub(r'\s+', ' ', result.source.strip())
    assert normalized.startswith('digraph {' if c.directed else 'graph {')


def test_unflatten_mocked(sentinel, mock_unflatten, cls):
    dot = cls()
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


@pytest.mark.exe
@pytest.mark.parametrize(
    'kwargs', [{'engine': 'spam'}])
def test_render_raises_before_save(tmp_path, cls, kwargs, filename='dot.gv'):
    dot = cls(filename=filename, directory=tmp_path)
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
    dot = cls(filename=filename, directory=tmp_path)

    expected_source = tmp_path / filename
    assert not expected_source.exists()

    first_arg = next(iter(kwargs))
    with pytest.raises(ValueError, match=f'unknown {first_arg}'):
        dot.render(**kwargs)

    assert not expected_source.exists()


@pytest.mark.exe
@pytest.mark.parametrize(
    'cls, expected',
    [(graphviz.Graph, 'graph {\n\tC\n}\n'),
     (graphviz.Digraph, 'digraph {\n\tC\n}\n')],
    ids=lambda p: getattr(p, '__name__', '...'))
def test_subgraph_render(capsys, tmp_path, cls, expected):
    lpath = tmp_path / 's1.gv'
    rendered = lpath.with_suffix('.gv.pdf')

    dot = cls()
    dot.edge('A', 'B')

    with dot.subgraph() as s1:
        s1.node('C')
        result = s1.render(str(lpath))

    assert result == str(rendered)

    assert lpath.read_text(encoding='ascii') == expected

    assert rendered.stat().st_size
    assert capsys.readouterr() == ('', '')


@pytest.mark.parametrize(
    'keep_attrs', [False, True])
def test_clear(cls, keep_attrs):
    kwargs = {f'{a}_attr': {a: a} for a in ('graph', 'node', 'edge')}
    c = cls(**kwargs)
    assert all(getattr(c, k) == v for k, v in kwargs.items())
    c.node('spam')
    assert len(c.body) == 1
    body = c.body

    c.clear(keep_attrs)
    assert c.body == []
    assert c.body is body
    if keep_attrs:
        assert all(getattr(c, k) == v for k, v in kwargs.items())
    else:
        assert all(getattr(c, k) == {} for k in kwargs)


def test_iter_subgraph_strict(cls):
    with pytest.raises(ValueError, match=r'strict'):
        cls().subgraph(cls(strict=True))


@pytest.mark.parametrize(
    'cls, expected',
    [(graphviz.Graph, 'strict graph {\n}\n'),
     (graphviz.Digraph, 'strict digraph {\n}\n')],
    ids=lambda p: getattr(p, '__name__', '...'))
def test_iter_strict(cls, expected):
    assert cls(strict=True).source == expected


def test_attr_invalid_kw(cls):
    with pytest.raises(ValueError, match=r'attr'):
        cls().attr('spam')


@pytest.mark.parametrize(
    'cls, expected',
    [(graphviz.Graph, 'graph {\n\tspam=eggs\n}\n'),
     (graphviz.Digraph, 'digraph {\n\tspam=eggs\n}\n')],
    ids=lambda p: getattr(p, '__name__', '...'))
def test_attr_kw_none(cls, expected):
    dot = cls()
    dot.attr(spam='eggs')
    assert dot.source == expected


@pytest.mark.parametrize(
    'cls, expected',
    [(graphviz.Graph,
      'graph {\n\tA [label="%s"]\n\tB [label="%s"]\n}\n' % (r'\\', r'\"\\\"')),
     (graphviz.Digraph,
      'digraph {\n\tA [label="%s"]\n\tB [label="%s"]\n}\n' % (r'\\', r'\"\\\"'))],
    ids=lambda p: getattr(p, '__name__', '...'))
def test_escaped_quotes_and_escapes(cls, expected):
    dot = cls()
    dot.node('A', label='\\\\')
    dot.node('B', label=r'"\\"')
    assert dot.source == expected


@pytest.mark.parametrize(
    'cls, expected',
    [(graphviz.Graph, 'graph {\n\t// comment\n\tsubgraph name {\n\t}\n}\n'),
     (graphviz.Digraph, 'digraph {\n\t// comment\n\tsubgraph name {\n\t}\n}\n')],
    ids=lambda p: getattr(p, '__name__', '...'))
def test_subgraph_graph_none(cls, expected):
    dot = cls(directory='nondirectory', format='png',
              encoding='ascii', engine='neato')
    assert dot.strict is False

    with dot.subgraph(name='name', comment='comment') as child:
        assert child.directory == dot.directory
        assert child.format == dot.format
        assert child.engine == dot.engine
        assert child.encoding == dot.encoding
        assert child.strict is None

    assert dot.source == expected


def test_subgraph_graph_notsole(cls):
    with pytest.raises(ValueError, match=r'sole'):
        cls().subgraph(cls(), name='spam')


def test_subgraph_mixed(classes):
    cls1, cls2 = classes
    with pytest.raises(ValueError, match=r'kind'):
        cls1().subgraph(cls2())


@pytest.mark.parametrize(
    'cls, expected',
    [(graphviz.Graph, 'graph {\n\t{\n\t}\n}\n'),
     (graphviz.Digraph, 'digraph {\n\t{\n\t}\n}\n')],
    ids=lambda p: getattr(p, '__name__', '...'))
def test_subgraph_reflexive(cls, expected):  # guard against potential infinite loop
    dot = cls()
    dot.subgraph(dot)
    assert dot.source == expected


def test_subgraph():
    s1 = graphviz.Graph()
    s1.node('A')
    s1.node('B')
    s1.node('C')
    s1.edge('A', 'B', constraint='false')
    s1.edges(['AC', 'BC'])

    s2 = graphviz.Graph()
    s2.node('D')
    s2.node('E')
    s2.node('F')
    s2.edge('D', 'E', constraint='false')
    s2.edges(['DF', 'EF'])

    dot = graphviz.Graph()
    dot.subgraph(s1)
    dot.subgraph(s2)
    dot.attr('edge', style='dashed')
    dot.edges(['AD', 'BE', 'CF'])

    assert dot.source == '''graph {
\t{
\t\tA
\t\tB
\t\tC
\t\tA -- B [constraint=false]
\t\tA -- C
\t\tB -- C
\t}
\t{
\t\tD
\t\tE
\t\tF
\t\tD -- E [constraint=false]
\t\tD -- F
\t\tE -- F
\t}
\tedge [style=dashed]
\tA -- D
\tB -- E
\tC -- F
}
'''


def test_label_html():
    """http://www.graphviz.org/doc/info/shapes.html#html"""
    dot = graphviz.Digraph('structs', node_attr={'shape': 'plaintext'})
    dot.node('struct1', '''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
  <TR>
    <TD>left</TD>
    <TD PORT="f1">middle</TD>
    <TD PORT="f2">right</TD>
  </TR>
</TABLE>>''')
    dot.node('struct2', '''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
  <TR>
    <TD PORT="f0">one</TD>
    <TD>two</TD>
  </TR>
</TABLE>>''')
    dot.node('struct3', '''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
  <TR>
    <TD ROWSPAN="3">hello<BR/>world</TD>
    <TD COLSPAN="3">b</TD>
    <TD ROWSPAN="3">g</TD>
    <TD ROWSPAN="3">h</TD>
  </TR>
  <TR>
    <TD>c</TD>
    <TD PORT="here">d</TD>
    <TD>e</TD>
  </TR>
  <TR>
    <TD COLSPAN="3">f</TD>
  </TR>
</TABLE>>''')
    dot.edge('struct1:f1', 'struct2:f0')
    dot.edge('struct1:f2', 'struct3:here')
    assert dot.source == '''digraph structs {
\tnode [shape=plaintext]
\tstruct1 [label=<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
  <TR>
    <TD>left</TD>
    <TD PORT="f1">middle</TD>
    <TD PORT="f2">right</TD>
  </TR>
</TABLE>>]
\tstruct2 [label=<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
  <TR>
    <TD PORT="f0">one</TD>
    <TD>two</TD>
  </TR>
</TABLE>>]
\tstruct3 [label=<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
  <TR>
    <TD ROWSPAN="3">hello<BR/>world</TD>
    <TD COLSPAN="3">b</TD>
    <TD ROWSPAN="3">g</TD>
    <TD ROWSPAN="3">h</TD>
  </TR>
  <TR>
    <TD>c</TD>
    <TD PORT="here">d</TD>
    <TD>e</TD>
  </TR>
  <TR>
    <TD COLSPAN="3">f</TD>
  </TR>
</TABLE>>]
\tstruct1:f1 -> struct2:f0
\tstruct1:f2 -> struct3:here
}
'''

import pytest

from graphviz import Graph, set_default_engine, set_default_format

ENGINE = 'dot'

FORMAT = 'pdf'


def test_set_default_engine_invalid():
    with pytest.raises(ValueError, match=r'unknown engine'):
        set_default_engine('nonengine')


def test_set_default_engine(monkeypatch, *, engine='neato', explicit_engine='sfdp'):
    assert len({ENGINE, engine, explicit_engine}) == 3

    from graphviz.files import Base
    assert Base._engine == ENGINE
    # isolate the test
    monkeypatch.setattr('graphviz.files.Base._engine', ENGINE)
    assert Base._engine == ENGINE

    g1 = Graph()
    assert g1.engine == ENGINE

    g2 = Graph(engine=explicit_engine)
    assert g2.engine == explicit_engine

    old = set_default_engine(engine)
    assert old == ENGINE

    assert g1.engine == engine
    assert g2.engine == explicit_engine

    g3 = Graph()
    assert g3.engine == engine

    g4 = Graph(engine=explicit_engine)
    assert g4.engine == explicit_engine

    old = set_default_engine(ENGINE)
    assert old == engine

    assert g1.engine == ENGINE
    assert g2.engine == explicit_engine
    assert g3.engine == ENGINE
    assert g4.engine == explicit_engine


def test_set_default_format_invalid():
    with pytest.raises(ValueError, match=r'unknown format'):
        set_default_format('nonformat')


def test_set_default_format(monkeypatch, *, format='png', explicit_format='jpeg'):
    assert len({FORMAT, format, explicit_format}) == 3

    from graphviz.files import Base
    assert Base._format == FORMAT
    # isolate the test
    monkeypatch.setattr('graphviz.files.Base._format', FORMAT)
    assert Base._format == FORMAT

    g1 = Graph()
    assert g1.format == FORMAT

    g2 = Graph(format=explicit_format)
    assert g2.format == explicit_format

    old = set_default_format(format)
    assert old == FORMAT

    assert g1.format == format
    assert g2.format == explicit_format

    g3 = Graph()
    assert g3.format == format

    g4 = Graph(format=explicit_format)
    assert g4.format == explicit_format

    old = set_default_format(FORMAT)
    assert old == format

    assert g1.format == FORMAT
    assert g2.format == explicit_format
    assert g3.format == FORMAT
    assert g4.format == explicit_format

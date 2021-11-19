import pytest

import graphviz

DEFAULT_ENGINE = 'dot'

DEFAULT_FORMAT = 'pdf'

DEFAULT_JUPYTER_FORMAT = 'svg'

DEFAULT_JUPYTER_MIMETYPE = 'image/svg+xml'


def test_set_default_engine_invalid():
    with pytest.raises(ValueError, match=r'unknown engine'):
        graphviz.set_default_engine('nonengine')


def test_set_default_format_invalid():
    with pytest.raises(ValueError, match=r'unknown format'):
        graphviz.set_default_format('nonformat')


def test_set_default_engine(monkeypatch, *, engine='neato', explicit_engine='sfdp'):
    assert len({DEFAULT_ENGINE, engine, explicit_engine}) == 3

    from graphviz.parameters import Parameters
    assert Parameters._engine == DEFAULT_ENGINE

    # isolate the test
    monkeypatch.setattr('graphviz.parameters.Parameters._engine', DEFAULT_ENGINE)
    assert Parameters._engine == DEFAULT_ENGINE

    g1 = graphviz.Graph()
    assert g1.engine == DEFAULT_ENGINE

    g2 = graphviz.Graph(engine=explicit_engine)
    assert g2.engine == explicit_engine

    old = graphviz.set_default_engine(engine)
    assert old == DEFAULT_ENGINE

    assert g1.engine == engine
    assert g2.engine == explicit_engine

    g3 = graphviz.Graph()
    assert g3.engine == engine

    g4 = graphviz.Graph(engine=explicit_engine)
    assert g4.engine == explicit_engine

    old = graphviz.set_default_engine(DEFAULT_ENGINE)
    assert old == engine

    assert g1.engine == DEFAULT_ENGINE
    assert g2.engine == explicit_engine
    assert g3.engine == DEFAULT_ENGINE
    assert g4.engine == explicit_engine


def test_set_default_format(monkeypatch, *, format='png', explicit_format='jpeg'):
    assert len({DEFAULT_FORMAT, format, explicit_format}) == 3

    from graphviz.parameters import Parameters
    assert Parameters._format == DEFAULT_FORMAT

    # isolate the test
    monkeypatch.setattr('graphviz.parameters.Parameters._format', DEFAULT_FORMAT)
    assert Parameters._format == DEFAULT_FORMAT

    g1 = graphviz.Graph()
    assert g1.format == DEFAULT_FORMAT

    g2 = graphviz.Graph(format=explicit_format)
    assert g2.format == explicit_format

    old = graphviz.set_default_format(format)
    assert old == DEFAULT_FORMAT

    assert g1.format == format
    assert g2.format == explicit_format

    g3 = graphviz.Graph()
    assert g3.format == format

    g4 = graphviz.Graph(format=explicit_format)
    assert g4.format == explicit_format

    old = graphviz.set_default_format(DEFAULT_FORMAT)
    assert old == format

    assert g1.format == DEFAULT_FORMAT
    assert g2.format == explicit_format
    assert g3.format == DEFAULT_FORMAT
    assert g4.format == explicit_format


def test_set_jupyter_format(monkeypatch, *, jupyter_format='jpg',
                            expected_old_format='svg',
                            expected_normalized_format='jpeg',
                            expected_mimetype='image/jpeg'):
    assert len({DEFAULT_JUPYTER_MIMETYPE, jupyter_format}) == 2

    from graphviz import jupyter_integration
    assert (jupyter_integration.JupyterIntegration._jupyter_mimetype
            == DEFAULT_JUPYTER_MIMETYPE)

    # isolate the test
    monkeypatch.setattr('graphviz.jupyter_integration.JupyterIntegration._jupyter_mimetype',
                        DEFAULT_JUPYTER_MIMETYPE)
    assert (jupyter_integration.JupyterIntegration._jupyter_mimetype
            == DEFAULT_JUPYTER_MIMETYPE)

    g1 = graphviz.Graph()
    assert g1._jupyter_mimetype == DEFAULT_JUPYTER_MIMETYPE

    old = graphviz.set_jupyter_format(jupyter_format)
    assert old == jupyter_integration.DEFAULT_JUPYTER_FORMAT

    assert g1._jupyter_mimetype == expected_mimetype

    g2 = graphviz.Graph()
    assert g2._jupyter_mimetype == expected_mimetype

    old = graphviz.set_jupyter_format(DEFAULT_JUPYTER_FORMAT)
    assert old == expected_normalized_format

    assert g1._jupyter_mimetype == DEFAULT_JUPYTER_MIMETYPE
    assert g2._jupyter_mimetype == DEFAULT_JUPYTER_MIMETYPE

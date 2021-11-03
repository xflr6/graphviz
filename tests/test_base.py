import pytest

from graphviz.base import Base


@pytest.fixture(scope='module')
def base():
    return Base()


def test_base_iter_raises_notimplementederror(base):
    with pytest.raises(NotImplementedError, match=r'subclasses'):
        iter(base)


def test_base_source_raises_notimplementederror(base):
    with pytest.raises(NotImplementedError, match=r'subclasses'):
        base.source

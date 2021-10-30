import pytest

from graphviz.base import Base


def test_base_iter():
    base_inst = Base()
    with pytest.raises(NotImplementedError, match=r'subclasses'):
        iter(base_inst)

# test_lang.py

import pytest

from graphviz.lang import quote, attr_list, nohtml


def test_quote_quotes():
    assert quote('"spam"') == r'"\"spam\""'


def test_quote_keyword():
    assert quote('node') == '"node"'
    assert quote('EDGE') == '"EDGE"'
    assert quote('Graph') == '"Graph"'


def test_attr_list_pairs():
    assert attr_list(attributes=[('spam', 'eggs')]) == ' [spam=eggs]'


def test_attr_list_map():
    assert attr_list(attributes={'spam': 'eggs'}) == ' [spam=eggs]'


def test_nohtml(py2):
    assert nohtml('spam') == 'spam'
    assert isinstance(nohtml('spam'), str)
    assert nohtml(u'spam') == u'spam'
    assert isinstance(nohtml(u'spam'), unicode if py2 else str)


def test_nohtml_invalid(py2):
    match = r"required types.+'str'"
    if py2:
        match += r".+'unicode'"
    with pytest.raises(TypeError, match=match):
        nohtml(True)

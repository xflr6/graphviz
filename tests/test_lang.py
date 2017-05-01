# test_lang.py

from graphviz.lang import quote, attr_list


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

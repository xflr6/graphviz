# test_lang.py

import pytest

from graphviz.lang import quote, attr_list, nohtml


@pytest.mark.parametrize('identifier, expected', [
    ('"spam"', r'"\"spam\""'),
    ('node', '"node"'),
    ('EDGE', '"EDGE"'),
    ('Graph', '"Graph"'),
])
def test_quote(identifier, expected):
    assert quote(identifier) == expected


@pytest.mark.parametrize('attributes, expected', [
    ([('spam', 'eggs')], ' [spam=eggs]'),
    ({'spam': 'eggs'}, ' [spam=eggs]'),
])
def test_attr_list(attributes, expected):
    assert attr_list(attributes=attributes) == expected


@pytest.mark.parametrize('string', ['spam', u'spam'])
def test_nohtml(string):
    result = nohtml(string)
    assert result == string
    assert isinstance(result, type(string))


def test_nohtml_invalid(py2):
    match = r"required types.+'str'"
    if py2:
        match += r".+'unicode'"
    with pytest.raises(TypeError, match=match):
        nohtml(True)

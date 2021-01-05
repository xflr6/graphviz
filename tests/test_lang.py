# test_lang.py

import warnings

import pytest

from graphviz.lang import quote, attr_list, nohtml


@pytest.mark.parametrize('char', ['G', 'E', 'T', 'H', 'L', 'l'])
def test_deprecated_escape(recwarn, char):
    warnings.simplefilter('always')

    escape = eval(rf'"\{char}"')

    assert len(recwarn) == 1
    w = recwarn.pop(DeprecationWarning)
    assert str(w.message).startswith('invalid escape sequence')

    assert escape == f'\\{char}'
    assert quote(escape) == f'"\\{char}"'


@pytest.mark.parametrize('identifier, expected', [
    ('"spam"', r'"\"spam\""'),
    ('node', '"node"'),
    ('EDGE', '"EDGE"'),
    ('Graph', '"Graph"'),
    ('\\G \\N \\E \\T \\H \\L', '"\\G \\N \\E \\T \\H \\L"'),
    ('\\n \\l \\r', '"\\n \\l \\r"'),
    ('\r\n', '"\r\n"'),
    ('\\\\n', r'"\\n"'),
    ('\u0665.\u0660', '"\u0665.\u0660"'),
    ('\\"spam', r'"\"spam"'),
    ('\\\\"spam', r'"\\\"spam"'),
    ('\\\\\\"spam', r'"\\\"spam"'),
    ('\\\\\\\\"spam', r'"\\\\\"spam"'),
])
def test_quote(identifier, expected):
    assert quote(identifier) == expected


@pytest.mark.parametrize('attributes, expected', [
    ([('spam', 'eggs')], ' [spam=eggs]'),
    ({'spam': 'eggs'}, ' [spam=eggs]'),
])
def test_attr_list(attributes, expected):
    assert attr_list(attributes=attributes) == expected


def test_nohtml(string='spam'):
    result = nohtml(string)
    assert result == string
    assert isinstance(result, str)

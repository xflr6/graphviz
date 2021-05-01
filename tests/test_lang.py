# test_lang.py

import warnings

import pytest

from graphviz import lang


@pytest.mark.parametrize('char', ['G', 'E', 'T', 'H', 'L', 'l'])
def test_deprecated_escape(recwarn, char):
    warnings.simplefilter('always')

    escape = eval(rf'"\{char}"')

    assert len(recwarn) == 1
    w = recwarn.pop(DeprecationWarning)
    assert str(w.message).startswith('invalid escape sequence')

    assert escape == f'\\{char}'
    assert lang.quote(escape) == f'"\\{char}"'


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
    assert lang.quote(identifier) == expected


@pytest.mark.parametrize('attributes, expected', [
    ([('spam', 'eggs')], ' [spam=eggs]'),
    ({'spam': 'eggs'}, ' [spam=eggs]'),
])
def test_attr_list(attributes, expected):
    assert lang.attr_list(attributes=attributes) == expected


@pytest.mark.parametrize('string, expected, expected_quoted', [
    ('spam', 'spam', 'spam'),
    ('<>-*-<>', '<>-*-<>', '"<>-*-<>"'),
])
def test_nohtml(string, expected, expected_quoted):
    result = lang.nohtml(string)
    assert isinstance(result, str)
    assert isinstance(result, lang.NoHtml)
    assert result == expected

    quoted = lang.quote(result)
    assert isinstance(quoted, str)
    assert quoted == expected_quoted

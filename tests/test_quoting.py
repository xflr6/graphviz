import sys
import warnings

import pytest

import graphviz
from graphviz import quoting


@pytest.mark.parametrize(
    'char', ['G', 'E', 'T', 'H', 'L', 'l'])
def test_deprecated_escape(recwarn, char):
    warnings.simplefilter('always')

    escape = eval(rf'"\{char}"')

    assert len(recwarn) == 1
    w = recwarn.pop(DeprecationWarning if sys.version_info < (3, 12)
                    else SyntaxWarning)
    assert str(w.message).startswith('invalid escape sequence')

    assert escape == f'\\{char}'
    assert quoting.quote(escape) == f'"\\{char}"'


@pytest.mark.parametrize(
    'identifier, expected',
    [('"spam"', r'"\"spam\""'),
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
     ('\\\\\\\\"spam', r'"\\\\\"spam"')])
def test_quote(identifier, expected):
    assert quoting.quote(identifier) == expected


@pytest.mark.parametrize(
    'attributes, expected',
    [([('spam', 'eggs')], ' [spam=eggs]'),
     ({'spam': 'eggs'}, ' [spam=eggs]')])
def test_attr_list(attributes, expected):
    assert quoting.attr_list(attributes=attributes) == expected


@pytest.mark.parametrize(
    'string, expected, expected_quoted',
    [('spam', 'spam', 'spam'),
     ('<>-*-<>', '<>-*-<>', '"<>-*-<>"')])
def test_nohtml(string, expected, expected_quoted):
    result = graphviz.nohtml(string)
    assert isinstance(result, str)
    assert isinstance(result, quoting.NoHtml)
    assert result == expected

    quoted = quoting.quote(result)
    assert isinstance(quoted, str)
    assert quoted == expected_quoted

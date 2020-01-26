# test_lang.py

import sys
import warnings

import pytest

from graphviz.lang import quote, attr_list, nohtml


@pytest.mark.parametrize('char', ['G', 'E', 'T', 'H', 'L', 'l'])
def test_deprecated_escape(recwarn, char):
    warnings.simplefilter('always')

    escape = eval(r'"\%s"' % char)

    if sys.version_info < (3, 6):
        assert not recwarn
    else:
        assert len(recwarn) == 1
        w = recwarn.pop(DeprecationWarning)
        assert str(w.message).startswith('invalid escape sequence')

    assert escape == '\\%s' % char
    assert quote(escape) == '"\\%s"' % char


@pytest.mark.parametrize('identifier, expected', [
    ('"spam"', r'"\"spam\""'),
    ('node', '"node"'),
    ('EDGE', '"EDGE"'),
    ('Graph', '"Graph"'),
    ('\\G \\N \\E \\T \\H \\L', '"\\G \\N \\E \\T \\H \\L"'),
    ('\\n \\l \\r', '"\\n \\l \\r"'),
    ('\r\n', '"\r\n"'),
    ('\\\\n', r'"\\n"'),
    (u'\u0665.\u0660', u'"\u0665.\u0660"'),
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

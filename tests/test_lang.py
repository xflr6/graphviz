# test_lang.py

import unittest

from graphviz.lang import quote, attributes


class TestQuote(unittest.TestCase):

    def test_quote_quotes(self):
        self.assertEqual(quote('"spam"'), r'"\"spam\""')


class TestAttributes(unittest.TestCase):

    def test_attributes_pairs(self):
        self.assertEqual(attributes(attributes=[('spam', 'eggs')]),
            ' [spam=eggs]')

    def test_attributes_map(self):
        self.assertEqual(attributes(attributes={'spam': 'eggs'}),
            ' [spam=eggs]')

    def test_attributes_raw(self):
        self.assertEqual(attributes(raw='spam'),
            ' [spam]')

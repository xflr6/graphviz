# test_lang.py

import unittest

from graphviz.lang import quote, attr_list


class TestQuote(unittest.TestCase):

    def test_quote_quotes(self):
        self.assertEqual(quote('"spam"'), r'"\"spam\""')

    def test_quote_keyword(self):
        self.assertEqual(quote('node'), '"node"')
        self.assertEqual(quote('EDGE'), '"EDGE"')
        self.assertEqual(quote('Graph'), '"Graph"')


class TestAttributes(unittest.TestCase):

    def test_attributes_pairs(self):
        self.assertEqual(attr_list(attributes=[('spam', 'eggs')]),
            ' [spam=eggs]')

    def test_attributes_map(self):
        self.assertEqual(attr_list(attributes={'spam': 'eggs'}),
            ' [spam=eggs]')

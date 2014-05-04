# test_files.py

import unittest

from graphviz.files import File


class TestBase(unittest.TestCase):

    def setUp(self):
        self.file = File()

    def test_format(self):
        with self.assertRaises(ValueError):
            self.file.format = 'spam'

    def test_engine(self):
        with self.assertRaises(ValueError):
            self.file.engine = 'spam'

    def test_encoding(self):
        with self.assertRaises(LookupError):
            self.file.encoding = 'spam'


class TestFile(unittest.TestCase):

    def test_init(self):
        f = File('name', 'dir', 'PNG', 'NEATO', 'latin1')
        self.assertEqual(f.filename, 'name')
        self.assertEqual(f.format, 'png')
        self.assertEqual(f.engine, 'neato')
        self.assertEqual(f.encoding, 'latin1')

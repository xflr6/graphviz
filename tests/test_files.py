# test_files.py

import os
import unittest2 as unittest

from graphviz.files import File, Source


class TestBase(unittest.TestCase):

    def setUp(self):
        self.file = File()

    def test_format(self):
        with self.assertRaisesRegexp(ValueError, 'format'):
            self.file.format = 'spam'

    def test_engine(self):
        with self.assertRaisesRegexp(ValueError, 'engine'):
            self.file.engine = 'spam'

    def test_encoding(self):
        with self.assertRaisesRegexp(LookupError, 'encoding'):
            self.file.encoding = 'spam'


class TestFile(unittest.TestCase):

    def test_init(self):
        f = File('name', 'dir', 'PNG', 'NEATO', 'latin1')
        self.assertEqual(f.filename, 'name')
        self.assertEqual(f.format, 'png')
        self.assertEqual(f.engine, 'neato')
        self.assertEqual(f.encoding, 'latin1')


class TestNoent(unittest.TestCase):

    def setUp(self):
        self._oldpath = os.environ.get('PATH')
        os.environ['PATH'] = ''
        self.file = File('spam.gv', 'test-output')
        self.file.source = 'spam'

    def tearDown(self):
        if self._oldpath is None:
            del os.environ['PATH']
        else:
            os.environ['PATH'] = self._oldpath

    def test_pipe(self):
        with self.assertRaisesRegexp(RuntimeError, 'failed to execute'):
            self.file.pipe()

    def test_render(self):
        with self.assertRaisesRegexp(RuntimeError, 'failed to execute'):
            self.file.render()


class TestSource(unittest.TestCase):

    def test_init(self):
        source = 'graph { hello -> world }'
        s = Source(source)
        self.assertEqual(s.source, source)

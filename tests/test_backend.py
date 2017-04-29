# test_backend.py

import unittest
import subprocess

from graphviz.backend import render, pipe


class TestRender(unittest.TestCase):

    def test_render_engine_unknown(self):
        with self.assertRaisesRegexp(ValueError, r'engine'):
            render('spam', 'pdf', '')

    def test_render_format_unknown(self):
        with self.assertRaisesRegexp(ValueError, r'format'):
            render('dot', 'spam', '')

    def test_render_filepath_missing(self):
        with self.assertRaises(subprocess.CalledProcessError) as c:
            render('dot', 'pdf', 'doesnotexist')
        self.assertEqual(c.exception.returncode, 2)


class TestPipe(unittest.TestCase):

    def test_render_engine_unknown(self):
        with self.assertRaisesRegexp(ValueError, r'engine'):
            pipe('spam', 'pdf', b'')

    def test_render_format_unknown(self):
        with self.assertRaisesRegexp(ValueError, r'format'):
            pipe('dot', 'spam', b'')

    def test_pipe_invalid_dot(self):
        with self.assertRaises(subprocess.CalledProcessError) as c:
            pipe('dot', 'svg', b'spam', quiet=True)
        self.assertEqual(c.exception.returncode, 1)

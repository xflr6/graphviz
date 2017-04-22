# test_backend.py

import unittest
import subprocess

from graphviz.backend import render, pipe


class TestRender(unittest.TestCase):

    def test_render_missing_file(self):
        with self.assertRaises(subprocess.CalledProcessError) as c:
            render('dot', 'pdf', 'doesnotexist')
        self.assertEqual(c.exception.returncode, 2)


class TestPipe(unittest.TestCase):

    def test_pipe_invalid_dot(self):
        with self.assertRaises(subprocess.CalledProcessError) as c:
            pipe('dot', 'svg', 'spam', quiet=True)
        self.assertEqual(c.exception.returncode, 1)

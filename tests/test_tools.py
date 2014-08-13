# test_tools.py

import unittest
import os

from graphviz.tools import mkdirs


class TestMkdirs(unittest.TestCase):

    @staticmethod
    def _dirnames(path=os.curdir):
        return [name for name in os.listdir(path) if os.path.isdir(name)]

    def test_cwd(self):
        dirnames = self._dirnames()
        mkdirs('setup.py')
        self.assertEqual(self._dirnames(), dirnames)

    def test_file(self):
        with self.assertRaises(OSError):
            mkdirs('setup.py/spam')

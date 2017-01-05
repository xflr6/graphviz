# test_tools.py

import unittest2 as unittest
import os
import stat

from graphviz.tools import mkdirs


class TestMkdirs(unittest.TestCase):
    def setUp(self):
        if not os.path.exists('setup.py'):
            f = open('setup.py', 'w')
            f.close()

    def tearDown(self):
        info = os.stat('setup.py')
        if info.st_size == 0:
            os.unlink('setup.py')

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

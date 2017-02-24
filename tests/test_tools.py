# test_tools.py

import unittest
import os
import shutil
import tempfile
import functools

from graphviz.tools import mkdirs


def itertree(root):
    for path, dirs, files in os.walk(root):
        base = os.path.relpath(path, root)
        rel_path = functools.partial(os.path.join, base if base != '.' else '')
        for is_file, names in [(False, dirs), (True, files)]:
            for n in names:
                yield is_file, rel_path(n).replace('\\', '/')


class TestMkdirs(unittest.TestCase):

    def setUp(self):
        self.old_dir = os.getcwd()
        self.test_dir = tempfile.mkdtemp()
        assert not self._dentries()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.old_dir)
        shutil.rmtree(self.test_dir)

    def _dentries(self):
        return list(itertree(self.test_dir))

    def test_mkdirs(self):
        mkdirs('spam.eggs')
        self.assertEqual(self._dentries(), [])
        for _ in range(2):
            mkdirs('spam/eggs/spam.eggs')
            self.assertEqual(self._dentries(),
                             [(False, 'spam'), (False, 'spam/eggs')])

    def test_mkdirs_invalid(self):
        with open('spam.eggs', 'wb'):
            pass
        with self.assertRaises(OSError):
            mkdirs('spam.eggs/spam')

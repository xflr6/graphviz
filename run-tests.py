# run-tests.py

import doctest

import nose

doctest.testfile('README.rst', module_relative=False)

nose.main()

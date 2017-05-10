# conftest.py

import re

import mock
import pytest


@pytest.fixture(scope='session')
def svg_pattern():
    return re.compile(r'(?s)^<\?xml .+</svg>\s*$')


@pytest.fixture(params=['', 'darwin', 'freebsd', 'linux', 'windows'])
def platform(request):
    name = request.param
    with mock.patch('graphviz.backend.PLATFORM', name):
        yield name


@pytest.fixture
def Popen():
    with mock.patch('subprocess.Popen') as Popen:
        yield Popen


@pytest.fixture
def startfile():
    with mock.patch('os.startfile', create=True) as startfile:
        yield startfile

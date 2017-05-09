# conftest.py

import re

import mock
import pytest


@pytest.fixture(scope='session')
def svg_pattern():
    return re.compile(r'(?s)^<\?xml .+</svg>\s*$')


@pytest.fixture
def unknown_platform(name='spam'):
    with mock.patch('graphviz.backend.PLATFORM', name):
        yield name


@pytest.fixture
def darwin(name='darwin'):
    with mock.patch('graphviz.backend.PLATFORM', name):
        yield name


@pytest.fixture
def unixoid(name='linux'):
    with mock.patch('graphviz.backend.PLATFORM', name):
        yield name


@pytest.fixture
def windows(name='windows'):
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

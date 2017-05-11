# conftest.py

import re

import pytest


@pytest.fixture(scope='session')
def svg_pattern():
    return re.compile(r'(?s)^<\?xml .+</svg>\s*$')


@pytest.fixture(params=['', 'darwin', 'freebsd', 'linux', 'windows'])
def platform(monkeypatch, request):
    monkeypatch.setattr('graphviz.backend.PLATFORM', request.param)
    yield request.param


@pytest.fixture
def check_call(mocker):
    yield mocker.patch('subprocess.check_call')


@pytest.fixture
def Popen(mocker):
    yield mocker.patch('subprocess.Popen')


@pytest.fixture
def startfile(mocker):
    yield mocker.patch('os.startfile', create=True)


@pytest.fixture
def empty_path(monkeypatch):
    monkeypatch.setenv('PATH', '')


@pytest.fixture
def pipe(mocker):
    yield mocker.patch('graphviz.backend.pipe')


@pytest.fixture
def render(mocker):
    yield mocker.patch('graphviz.backend.render')

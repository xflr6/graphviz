# conftest.py

import sys
import platform as _platform

import pytest


def pytest_addoption(parser):
    parser.addoption('--skipexe', action='store_true',
                     help='skip tests that run Graphviz executables')


def pytest_configure(config):
    pytest.exe = pytest.mark.skipif(config.getoption('--skipexe'),
                                    reason='skipped by --skipexe option')


@pytest.fixture(scope='session')
def py2():
    return sys.version_info.major == 2


@pytest.fixture(scope='session')
def test_platform():
    return _platform.system().lower()


@pytest.fixture(params=['nonplatform', 'darwin', 'freebsd', 'linux', 'windows'],
                ids=lambda p: 'platform=%r' % p)
def platform(monkeypatch, request):
    monkeypatch.setattr('graphviz.backend.PLATFORM', request.param)
    yield request.param


@pytest.fixture
def Popen(mocker):  # noqa: N802
    yield mocker.patch('subprocess.Popen')


@pytest.fixture
def startfile(mocker):
    yield mocker.patch('os.startfile', create=True)


@pytest.fixture
def empty_path(monkeypatch):
    monkeypatch.setenv('PATH', '')


@pytest.fixture(params=[False, True], ids=lambda q: 'quiet=%r' % q)
def quiet(request):
    return request.param


@pytest.fixture
def pipe(mocker):
    yield mocker.patch('graphviz.backend.pipe')


@pytest.fixture
def render(mocker):
    yield mocker.patch('graphviz.backend.render')

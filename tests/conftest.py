# conftest.py

import sys
import platform as platform_

import pytest


def pytest_addoption(parser):
    parser.addoption('--skipexe', action='store_true',
                     help='skip tests that run Graphviz executables'
                          'or subprocesses')


def pytest_configure(config):
    pytest.exe = pytest.mark.skipif(config.getoption('--skipexe'),
                                    reason='skipped by --skipexe option')


@pytest.fixture(scope='session')
def py2():
    return sys.version_info.major == 2


@pytest.fixture(scope='session')
def filesdir(tmpdir_factory):
    LocalPath = tmpdir_factory.getbasetemp().__class__  # noqa: N806
    return LocalPath(__file__).new(basename='')


@pytest.fixture(scope='session')
def test_platform():
    return platform_.system().lower()


@pytest.fixture(params=['darwin', 'freebsd', 'linux', 'windows'],
                ids=lambda p: 'platform=%r' % p)
def platform(monkeypatch, request):
    monkeypatch.setattr('graphviz.backend.PLATFORM', request.param)
    yield request.param


@pytest.fixture
def unknown_platform(monkeypatch, name='nonplatform'):
    monkeypatch.setattr('graphviz.backend.PLATFORM', name)
    yield name


@pytest.fixture
def Popen(mocker):  # noqa: N802
    yield mocker.patch('subprocess.Popen', autospec=True)


@pytest.fixture
def startfile(mocker, test_platform):
    if test_platform == 'windows':
        kwargs = {'autospec': True}
    else:
        kwargs = {'create': True, 'new_callable': mocker.Mock}
    yield mocker.patch('os.startfile', **kwargs)


@pytest.fixture
def empty_path(monkeypatch):
    monkeypatch.setenv('PATH', '')


@pytest.fixture(params=[False, True], ids=lambda q: 'quiet=%r' % q)
def quiet(request):
    return request.param


@pytest.fixture
def pipe(mocker):
    yield mocker.patch('graphviz.backend.pipe', autospec=True)


@pytest.fixture
def render(mocker):
    yield mocker.patch('graphviz.backend.render', autospec=True)

"""pytest command line options and fixtures."""

import pathlib
import platform as platform_

import pytest

DIRECTORY = pathlib.Path(__file__).parent

SKIP_EXE = '--skip-exe'


def pytest_addoption(parser):
    parser.addoption(SKIP_EXE, action='store_true',
                     help='skip tests that run Graphviz executables'
                          ' or subprocesses')


def pytest_configure(config):
    config.addinivalue_line('markers',
                            f'exe: skip if {SKIP_EXE} is given')


def pytest_collection_modifyitems(config, items):
    if config.getoption(SKIP_EXE):
        for item in items:
            if 'exe' in item.keywords:
                marker = pytest.mark.skip(reason=f'skipped by {SKIP_EXE} flag')
                item.add_marker(marker)


@pytest.fixture(scope='session')
def files_path():
    return DIRECTORY / 'files'


@pytest.fixture(scope='session')
def platform():
    return platform_.system().lower()


@pytest.fixture(params=['darwin', 'freebsd', 'linux', 'windows'],
                ids=lambda p: f'platform={p!r}')
def mock_platform(monkeypatch, request):
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
def startfile(mocker, platform):
    if platform == 'windows':
        kwargs = {'autospec': True}
    else:
        kwargs = {'create': True, 'new_callable': mocker.Mock}
    yield mocker.patch('os.startfile', **kwargs)


@pytest.fixture
def empty_path(monkeypatch):
    monkeypatch.setenv('PATH', '')


@pytest.fixture(params=[False, True], ids=lambda q: f'quiet={q!r}')
def quiet(request):
    return request.param


@pytest.fixture
def pipe(mocker):
    yield mocker.patch('graphviz.backend.pipe', autospec=True)


@pytest.fixture
def render(mocker):
    yield mocker.patch('graphviz.backend.render', autospec=True)

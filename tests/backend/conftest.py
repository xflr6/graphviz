"""pytest fixtures for backend."""

import pytest


@pytest.fixture
def mock_run(mocker):
    yield mocker.patch('subprocess.run', autospec=True)


@pytest.fixture
def mock_popen(mocker):
    yield mocker.patch('subprocess.Popen', autospec=True)


@pytest.fixture
def mock_startfile(mocker, platform):
    if platform == 'windows':
        kwargs = {'autospec': True}
    else:
        kwargs = {'create': True, 'new_callable': mocker.Mock}
    yield mocker.patch('os.startfile', **kwargs)

"""pytest doctest command line options and fixtures."""

import pytest

SKIP_EXE = '--skip-exe'


def pytest_addoption(parser):  # pragma: no cover
    try:
        parser.addoption(SKIP_EXE, action='store_true',
                         help='Skip tests with pytest.mark.exe.'
                              ' Xfail tests with pytest.mark.exe(xfail=True).'
                              ' Skip doctests with doctest_mark_exe().'
                              ' Xfail doctests with doctest_mark_exe(xfail=True).'
                              ' exe marks tests requiring backend.DOT_BINARY.')
    except ValueError as e:  # pragma: no cover
        assert SKIP_EXE in str(e), f'fails because {SKIP_EXE!r} is already added'


@pytest.fixture(autouse=True)  # pragma: no cover
def doctests(pytestconfig, doctest_namespace):
    def doctest_mark_exe(**kwargs):
        return None

    if pytestconfig.getoption(SKIP_EXE):
        def doctest_mark_exe(*, xfail: bool = False, **kwargs):  # noqa: F811
            return pytest.xfail(**kwargs) if xfail else pytest.skip(**kwargs)

    doctest_namespace['doctest_mark_exe'] = doctest_mark_exe

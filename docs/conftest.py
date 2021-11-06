"""pytest command line options and fixtures."""

import pytest

SKIP_EXE = '--skip-exe'


@pytest.fixture(autouse=True)
def doctests(pytestconfig, doctest_namespace):
    def doctest_mark_exe(**kwargs):
        return None

    if pytestconfig.getoption(SKIP_EXE):
        def doctest_mark_exe(*, xfail: bool = False, **kwargs):  # noqa: F811
            return pytest.xfail(**kwargs) if xfail else pytest.skip(**kwargs)

    doctest_namespace['doctest_mark_exe'] = doctest_mark_exe

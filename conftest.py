"""pytest command line options and doctest flag definition/setup."""

import doctest
import unittest.mock

NO_EXE = doctest.register_optionflag('NO_EXE')

class NoExeChecker(doctest.OutputChecker):  # noqa: E302

    def check_output(self, want, got, optionflags, *args, **kwargs) -> bool:
        if optionflags & NO_EXE:
            return True
        return super().check_output(want, got, optionflags, *args, **kwargs)

unittest.mock.patch.object(doctest, 'OutputChecker', new=NoExeChecker).start()  # noqa: E305

import pytest  # noqa: E402

SKIP_EXE = '--skip-exe'

ONLY_EXE = '--only-exe'


def pytest_addoption(parser):
    parser.addoption(SKIP_EXE, action='store_true',
                     help='Skip tests with pytest.mark.exe.'
                          ' Xfail tests with pytest.mark.exe(xfail=True).'
                          ' Skip doctests with doctest_mark_exe().'
                          ' Xfail doctests with doctest_mark_exe(xfail=True).'
                          ' exe marks tests requiring backend.DOT_BINARY.')

    parser.addoption(ONLY_EXE, action='store_true',
                     help='Skip tests without pytest.mark.exe.'
                          ' Overrides --skip-exe.'
                          ' exe marks tests requiring backend.DOT_BINARY.')


@pytest.fixture(autouse=True)
def doctests(pytestconfig, doctest_namespace):
    def doctest_mark_exe(**kwargs):
        return None

    if pytestconfig.getoption(SKIP_EXE):
        def doctest_mark_exe(*, reason=SKIP_EXE, xfail: bool = False, **kwargs):  # noqa: F811
            return (pytest.xfail(reason=reason, **kwargs) if xfail
                    else pytest.skip(reason, **kwargs))

    doctest_namespace.update(doctest_mark_exe=doctest_mark_exe)

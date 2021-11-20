"""pytest command line options and doctest namespace."""

import doctest as _doctest
from unittest import mock as _mock

_NO_EXE = _doctest.register_optionflag('NO_EXE')

SKIP_EXE = '--skip-exe'

ONLY_EXE = '--only-exe'


class _NoExeChecker(_doctest.OutputChecker):

    def check_output(self, want, got, optionflags, *args, **kwargs) -> bool:
        if optionflags & _NO_EXE:
            return True
        return super().check_output(want, got, optionflags, *args, **kwargs)


_mock.patch.object(_doctest, 'OutputChecker', new=_NoExeChecker).start()
import pytest  # noqa: E402


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

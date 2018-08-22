# _compat.py - Python 2/3 compatibility

import os
import sys
import subprocess

PY2 = sys.version_info.major == 2


if PY2:
    string_classes = (str, unicode)  # needed individually for sublassing
    text_type = unicode

    def iteritems(d):
        return d.iteritems()

    def makedirs(name, mode=0o777, exist_ok=False):
        try:
            os.makedirs(name, mode)
        except OSError:
            if not exist_ok or not os.path.isdir(name):
                raise

    def stderr_write_bytes(data, flush=False):
        """Write data str to sys.stderr (flush if requested)."""
        sys.stderr.write(data)
        if flush:
            sys.stderr.flush()


else:
    string_classes = (str,)
    text_type = str

    def iteritems(d):
        return iter(d.items())

    def makedirs(name, mode=0o777, exist_ok=False):  # allow os.makedirs mocking
        return os.makedirs(name, mode, exist_ok=exist_ok)

    def stderr_write_bytes(data, flush=False):
        """Encode data str and write to sys.stderr (flush if requested)."""
        encoding = sys.stderr.encoding or sys.getdefaultencoding()
        sys.stderr.write(data.decode(encoding))
        if flush:
            sys.stderr.flush()


if sys.version_info < (3, 5):
    class CalledProcessError(subprocess.CalledProcessError):

        def __init__(self, returncode, cmd, output=None, stderr=None):
            super(CalledProcessError, self).__init__(returncode, cmd, output)
            self.stderr = stderr

        @property
        def stdout(self):
            return self.output

        @stdout.setter
        def stdout(self, value):  # pragma: no cover
            self.output = value


else:
    CalledProcessError = subprocess.CalledProcessError

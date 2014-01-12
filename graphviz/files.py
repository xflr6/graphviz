# files.py - save, compile, view

"""Save DOT code objects, compile with Graphviz dot, and open in viewer."""

import os
import subprocess

__all__ = ['File']


class File(object):

    _compile = 'dot -Tpdf -O %s'

    def save(self, filename=None, compile=False, view=False, directory=None):
        """Save the source to file."""
        if filename is None:
            filename = self.filename
        if directory is None:
            directory = self.directory
        for dname in [directory, os.path.dirname(filename)]:
            if dname and not os.path.exists(dname):
                os.mkdir(dname)
        if directory:
            filename = os.path.join(directory, filename)
        data = self.source
        with open(filename, 'wb') as fd:
            fd.write(data)
        self._saved = filename
        if compile or view:
            self.compile(view=view)

    def compile(self, view=False):
        """Compile the saved source file to PDF."""
        if not self._saved:
            self.save(compile=False, view=False)
        subprocess.call(self._compile % self._saved)
        if view:
            self.view()

    def view(self):
        """Open the compiled PDF from the saved source file in a viewer."""
        if not self._saved:
            self.save(compile=False, view=False)
        pdfpath = '%s.pdf' % self._saved
        if not os.path.exists(pdfpath):
            self.compile(view=False)
        subprocess.call(pdfpath, shell=True)

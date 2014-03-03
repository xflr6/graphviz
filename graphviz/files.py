# files.py - save, compile, view

"""Save DOT code objects, compile with Graphviz dot, and open in viewer."""

import os
import sys
import codecs
import subprocess

import tools

__all__ = ['File']

FORMATS = {'pdf', 'ps', 'svg', 'fig', 'pcl', 'png', 'gif', 'dia'}
ENGINES = {'dot', 'neato', 'twopi', 'circo', 'fdp', 'sfdp'}


class Base(object):

    _cmd = '%(engine)s -T%(format)s -O %(filepath)s'

    _format = 'pdf'
    _engine = 'dot'
    _encoding = 'utf8'

    _default_extension = 'gv'

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, format):
        if format not in FORMATS:
            raise ValueError('Unknown format: %r' % format)
        self._format = format

    @property
    def engine(self):
        return self._engine

    @engine.setter
    def engine(self, engine):
        if engine not in ENGINES:
            raise ValueError('Unknown engine: %r' % engine)
        self._engine = engine

    @property
    def encoding(self):
        return self._encoding

    @encoding.setter
    def encoding(self, encoding):
        if encoding is not None:
            codecs.lookup(encoding)
        self._encoding = encoding



class File(Base):

    directory = ''

    @property
    def filepath(self):
        return os.path.join(self.directory, self.filename)

    def __init__(self, filename=None, directory=None, format=None, engine=None, encoding=None):
        if filename is None:
            name = getattr(self, 'name', None) or self.__class__.__name__
            filename = '%s.%s' % (name, self._default_extension)
        self.filename = filename

        if directory is not None:
            self.directory = directory

        if format is not None:
            self.format = format

        if engine is not None:
            self.engine = engine

        if encoding is not None:
            self.encoding = encoding            


    def render(self, filename=None, directory=None, view=False, dry=False):
        """Save the source to file and render with Graphviz engine."""
        if filename is not None:
            self.filename = filename
        if directory is not None:
            self.directory = directory

        filepath = self.filepath
        tools.mkdirs(filepath)
        data = self.source
        if self._encoding is None:
            with open(filepath, 'wb') as fd:
                fd.write(data)
        else:
            with codecs.open(filepath, 'wb', self._encoding) as fd:
                fd.write(data)

        if dry:
            return

        params = {'engine': self._engine, 'format': self._format, 'filepath': filepath}
        cmd = self._cmd % params
        returncode = subprocess.Popen(cmd.split()).wait()

        rendered = '%s.%s' % (filepath, self._format)

        if view:
            self._view(rendered, self._format)

        return rendered

    def view(self):
        """Save the source to file, open the rendered result in a viewer."""
        rendered = self.render()
        self._view(rendered, self._format)

    def _view(self, filepath, format):
        methods = [
            '_view_%s_%s' % (format, sys.platform),
            '_view_%s' % format,
        ]
        for name in methods:
            method = getattr(self, name, None)
            if method is not None:
                break
        else:
            raise RuntimeError('%r has no built-in viewer support for %r '
                'on %r platform' % (self.__class__, format, sys.platform))

        return method(filepath)

    def _view_pdf_linux2(self, filepath):
        raise NotImplementedError

    def _view_pdf_win32(self, filepath):
        subprocess.Popen(filepath, shell=True)

    def _view_pdf_darwin(self, filepath):
        subprocess.Popen(filepath, shell=True)

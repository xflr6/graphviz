# files.py - save, render, view

"""Save DOT code objects, render with Graphviz dot, and open in viewer."""

import sys
import os
import io
import codecs
import subprocess

from ._compat import text_type

from .tools import mkdirs

__all__ = ['File']

FORMATS = {'pdf', 'ps', 'svg', 'fig', 'pcl', 'png', 'gif', 'dia'}

ENGINES = {'dot', 'neato', 'twopi', 'circo', 'fdp', 'sfdp'}

PLATFORM = sys.platform


class Base(object):

    _format = 'pdf'
    _engine = 'dot'
    _encoding = 'utf8'

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

    _default_extension = 'gv'

    @staticmethod
    def _cmd(engine, format, filepath):
        return [engine, '-T%s' % format, '-O', filepath]

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
        mkdirs(filepath)

        data = text_type(self.source)

        with io.open(filepath, 'w', encoding=self.encoding) as fd:
            fd.write(data)

        if dry:
            return

        cmd = self._cmd(self._engine, self._format, filepath)

        returncode = subprocess.Popen(cmd).wait()

        rendered = '%s.%s' % (filepath, self._format)

        if view:
            self._view(rendered, self._format)

        return rendered

    def view(self):
        """Save the source to file, open the rendered result in a viewer."""
        rendered = self.render()
        self._view(rendered, self._format)

    def _view(self, filepath, format):
        """Start the right viewer based on file format and platform."""
        methods = [
            '_view_%s_%s' % (format, PLATFORM),
            '_view_%s' % PLATFORM,
        ]
        for name in methods:
            method = getattr(self, name, None)
            if method is not None:
                break
        else:
            raise RuntimeError('%r has no built-in viewer support for %r '
                'on %r platform' % (self.__class__, format, PLATFORM))

        method(filepath)

    @staticmethod
    def _view_linux2(filepath):
        """Open filepath in the user's preferred application (linux)."""
        subprocess.Popen(['xdg-open', filepath], shell=True)

    @staticmethod
    def _view_win32(filepath):
        """Start filepath with its associated application (windows)."""
        os.startfile(filepath)

    @staticmethod
    def _view_darwin(filepath):
        """Open filepath with its default application (mac)."""
        subprocess.Popen(['open', filepath], shell=True)

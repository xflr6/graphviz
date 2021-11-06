"""Rendering format parameter handling."""

import typing

from ... import copying

__all__ = ['FORMATS', 'verify_format', 'Format']

FORMATS = {'bmp',  # http://www.graphviz.org/doc/info/output.html
           'canon', 'dot', 'gv', 'xdot', 'xdot1.2', 'xdot1.4',
           'cgimage',
           'cmap',
           'eps',
           'exr',
           'fig',
           'gd', 'gd2',
           'gif',
           'gtk',
           'ico',
           'imap', 'cmapx',
           'imap_np', 'cmapx_np',
           'ismap',
           'jp2',
           'jpg', 'jpeg', 'jpe',
           'json', 'json0', 'dot_json', 'xdot_json',  # Graphviz 2.40
           'pct', 'pict',
           'pdf',
           'pic',
           'plain', 'plain-ext',
           'png',
           'pov',
           'ps',
           'ps2',
           'psd',
           'sgi',
           'svg', 'svgz',
           'tga',
           'tif', 'tiff',
           'tk',
           'vml', 'vmlz',
           'vrml',
           'wbmp',
           'webp',
           'xlib',
           'x11'}

DEFAULT_FORMAT = 'pdf'


def verify_format(format: str) -> None:
    if format.lower() not in FORMATS:
        raise ValueError(f'unknown format: {format!r}')


class Format(copying.Copy):
    """Rendering format parameter with ``'pdf'`` default."""

    _format = DEFAULT_FORMAT

    _verify_format = staticmethod(verify_format)

    def __init__(self, format: typing.Optional[str] = None, **kwargs) -> None:
        super().__init__(**kwargs)

        if format is not None:
            self.format = format

    def _copy_kwargs(self, **kwargs):
        """Return the kwargs to create a copy of the instance."""
        if '_format' in self.__dict__:
            kwargs['format'] = self._format
        return super()._copy_kwargs(**kwargs)

    @property
    def format(self) -> str:
        """The output format used for rendering
            (``'pdf'``, ``'png'``, ...)."""
        return self._format

    @format.setter
    def format(self, format: str) -> None:
        format = format.lower()
        self._verify_format(format)
        self._format = format

import typing

from .. import copying

__all__ = ['FORMATS', 'Format']

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


class Format:
    """Graphiz default format."""

    _format = 'pdf'

    def __init__(self, format=None, **kwargs):
        super().__init__(**kwargs)

        if format is not None:
            self.format = format

    def _copy_kwargs(self, **kwargs):
        """Return the kwargs to create a copy of the instance."""
        attr_kw = [('_format', 'format')]
        ns = self.__dict__
        for attr, kw in attr_kw:
            assert kw not in kwargs
            if attr in ns:
                kwargs[kw] = ns[attr]
        return super()._copy_kwargs(**kwargs)

    @property
    def format(self) -> str:
        """The output format used for rendering
            (``'pdf'``, ``'png'``, ...)."""
        return self._format

    @format.setter
    def format(self, format: str) -> None:
        format = format.lower()
        if format not in FORMATS:
            raise ValueError(f'unknown format: {format!r}')
        self._format = format

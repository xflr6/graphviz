"""Display rendered graph as SVG in Jupyter Notebooks and QtConsole."""

from . import encoding
from . import rendering

__all__ = ['JupyterSvgIntegration']


class JupyterSvgIntegration(rendering.Pipe, encoding.Encoding):

    def _repr_svg_(self):
        return self.pipe(format='svg', encoding=self._encoding)

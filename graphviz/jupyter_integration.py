"""Display rendered graph as SVG in Jupyter Notebooks and QtConsole."""

from . import rendering

__all__ = ['JupyterSvgIntegration']


class JupyterSvgIntegration(rendering.Pipe):

    def _repr_svg_(self):
        return self.pipe(format='svg', encoding=self._encoding)

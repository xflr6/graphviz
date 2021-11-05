"""Display rendered graph as SVG in Jupyter Notebooks and QtConsole."""

from . import piping

__all__ = ['JupyterSvgIntegration']


class JupyterSvgIntegration(piping.Pipe):
    """Display rendered graph as SVG in Jupyter Notebooks and QtConsole."""

    def _repr_svg_(self):
        return self.pipe(format='svg', encoding=self._encoding)

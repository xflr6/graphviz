"""Display rendered graph as SVG in Jupyter Notebooks and QtConsole."""
import typing
from . import piping

__all__ = ['JUPYTER_REPRESENTATIONS',
           'verify_jupyter_representation',
           'JupyterIntegration']

JUPYTER_REPRESENTATIONS = {
    'image/svg+xml': '_repr_image_svg_xml',
    'image/png': '_repr_image_png',
    'image/jpeg': '_repr_image_jpeg',

    # The following does not work yet. Not clear why, because the documentation
    # has only few information about them.
    'application/json': None,  # ToDo: What does jupyter expect?
    'application/pdf': None,  # ToDo: Does Jupyter only accept file path?

    # No reasonable representation
    'text/plain': None,
    'text/latex': None,
    'text/html': None,
    'application/javascript': None,
    'text/markdown': None,
}

DEFAULT_JUPYTER_REPRESENTATION = 'image/svg+xml'

REQUIRED = True


def verify_jupyter_representation(jupyter_representation: str,
                                  *,
                                  required: bool = REQUIRED) -> None:
    if jupyter_representation is None:
        if required:
            raise ValueError('missing jupyter_representation')
    elif jupyter_representation not in JUPYTER_REPRESENTATIONS:
        raise ValueError(
            f'unknown jupyter_representation: {jupyter_representation!r}')


class JupyterIntegration(piping.Pipe):
    """Display rendered graph as SVG in Jupyter Notebooks and QtConsole."""

    _jupyter_representation = DEFAULT_JUPYTER_REPRESENTATION

    _verify_jupyter_representation = staticmethod(verify_jupyter_representation)

    @property
    def jupyter_representation(self) -> str:
        """The output format used for rendering
            (``'pdf'``, ``'png'``, ...)."""
        return self._jupyter_representation

    @jupyter_representation.setter
    def jupyter_representation(self, jupyter_representation: str) -> None:
        self._verify_jupyter_representation(jupyter_representation)
        self._jupyter_representation = jupyter_representation

    def _repr_mimebundle_(self,
                          include: typing.Optional[list] = None,
                          exclude: typing.Optional[list] = None,
                          **kwargs) -> dict:
        # The documentation of this function is in the following notebook:
        #     "examples/IPython Kernel/Custom Display Logic.ipynb"
        # https://nbviewer.org/github/ipython/ipython/blob/master/examples/IPython%20Kernel/Custom%20Display%20Logic.ipynb
        # from IPython git repository. At the moment the readthedocs
        # documentation of IPython only mention _repr_mimebundle_ but details
        # are missing.
        del kwargs
        reprs = set(include) if include else {self._jupyter_representation}
        reprs -= exclude or set()

        return {mime: getattr(self, method_name)()
                for mime, method_name in JUPYTER_REPRESENTATIONS.items()
                if method_name is not None and mime in reprs}

    def _repr_image_svg_xml(self):
        return self.pipe(format='svg', encoding=self._encoding)

    def _repr_image_png(self):
        return self.pipe(format='png')

    def _repr_image_jpeg(self):
        return self.pipe(format='jpeg')

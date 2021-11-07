"""Mixin classes used by Base subclasses to inherit backend functionality."""

from .. import parameters

from . import piping
from . import rendering
from . import unflattening
from . import viewing

__all__ = ['Render', 'Pipe', 'Unflatten', 'View']


class RenderParameters(parameters.Parameters):
    """Parameters for calling ``graphviz.render()`` and ``graphviz.pipe()``."""

    def _get_parameters(self, **kwargs):
        kwargs = super()._get_parameters(**kwargs)
        return [kwargs.pop('engine'), kwargs.pop('format')], kwargs


class Render(RenderParameters):

    _get_render_parameters = RenderParameters._get_parameters

    @property
    def _render(_):
        """Simplify ``._render()`` mocking."""
        return rendering.render


class Pipe(RenderParameters):

    _get_pipe_parameters = RenderParameters._get_parameters

    @property
    def _pipe_lines(_):
        """Simplify ``._pipe_lines()`` mocking."""
        return piping.pipe_lines

    @property
    def _pipe_lines_string(_):
        """Simplify ``._pipe_lines_string()`` mocking."""
        return piping.pipe_lines_string


class Unflatten:

    @property
    def _unflatten(_):
        """Simplify ``._unflatten mocking."""
        return unflattening.unflatten


class View:
    """Open filepath with its default viewing application
        (platform-specific)."""

    _view_darwin = staticmethod(viewing.view_darwin)

    _view_freebsd = staticmethod(viewing.view_unixoid)

    _view_linux = staticmethod(viewing.view_unixoid)

    _view_windows = staticmethod(viewing.view_windows)

"""Pipe source through the Graphviz *unflatten* preprocessor."""

import typing

from . import base
from . import backend
from . import encoding

__all__ = ['Unflatten']


class Unflatten(encoding.Encoding, base.Base, backend.Unflatten):
    """Pipe source through the Graphviz *unflatten* preprocessor."""

    def unflatten(self,
                  stagger: typing.Optional[int] = None,
                  fanout: bool = False,
                  chain: typing.Optional[int] = None):
        """Return a new :class:`.Source` instance with the source
            piped through the Graphviz *unflatten* preprocessor.

        Args:
            stagger: Stagger the minimum length
                of leaf edges between 1 and this small integer.
            fanout: Fanout nodes with indegree = outdegree = 1
                when staggering (requires ``stagger``).
            chain: Form disconnected nodes into chains
                of up to this many nodes.

        Returns:
            Source: Prepocessed DOT source code (improved layout aspect ratio).

        Raises:
            graphviz.RequiredArgumentError: If ``fanout`` is given
                but ``stagger`` is None.
            graphviz.ExecutableNotFound: If the Graphviz ``unflatten`` executable
                is not found.
            subprocess.CalledProcessError: If the returncode (exit status)
                of the unflattening 'unflatten' subprocess is non-zero.

        See also:
            https://www.graphviz.org/pdf/unflatten.1.pdf
        """
        from . import sources

        out = self._unflatten(self.source,
                              stagger=stagger, fanout=fanout, chain=chain,
                              encoding=self._encoding)

        kwargs = self._copy_kwargs()
        return sources.Source(out,
                              filename=kwargs.get('filename'),
                              directory=kwargs.get('directory'),
                              format=kwargs.get('format'),
                              engine=kwargs.get('engine'),
                              encoding=kwargs.get('encoding'),
                              renderer=kwargs.get('renderer'),
                              formatter=kwargs.get('formatter'),
                              loaded_from_path=None)

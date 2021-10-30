from . import base
from . import backend
from . import encoding

__all__ = ['Unflatten']


class Unflatten(encoding.Encoding, backend.Graphviz, base.Base):
    """Pipe source through the Graphviz *unflatten* preprocessor."""

    def unflatten(self, stagger=None, fanout=False, chain=None):
        """Return a new :class:`.Source` instance with the source
            piped through the Graphviz *unflatten* preprocessor.

        Args:
            stagger (int): Stagger the minimum length
                of leaf edges between 1 and this small integer.
            fanout (bool): Fanout nodes with indegree = outdegree = 1
                when staggering (requires ``stagger``).
            chain (int): Form disconnected nodes into chains
                of up to this many nodes.

        Returns:
            Source: Prepocessed DOT source code (improved layout aspect ratio).

        Raises:
            graphviz.RequiredArgumentError: If ``fanout`` is given
                but ``stagger`` is None.
            graphviz.ExecutableNotFound: If the Graphviz 'unflatten' executable
                is not found.
        subprocess.CalledProcessError: If the returncode (exit status)
            of the unflattening 'unflatten' subprocess is non-zero.

        See also:
            https://www.graphviz.org/pdf/unflatten.1.pdf
        """
        from . import sources

        out = backend.unflatten(self.source,
                                stagger=stagger, fanout=fanout, chain=chain,
                                encoding=self._encoding)
        return sources.Source(out,
                              filename=self.filename, directory=self.directory,
                              format=self._format, engine=self._engine,
                              encoding=self._encoding)

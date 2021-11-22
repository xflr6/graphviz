"""Common backend constants."""

__all__ = ['RequiredArgumentError']


class RequiredArgumentError(TypeError):
    """:class:`TypeError` raised if a required argument is missing."""

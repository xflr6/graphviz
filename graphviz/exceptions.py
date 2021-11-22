"""Commonly used exception classes."""

__all__ = ['RequiredArgumentError']


class RequiredArgumentError(TypeError):
    """:class:`TypeError` raised if a required argument is missing."""

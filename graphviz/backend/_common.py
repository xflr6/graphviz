"""Common backend constants."""

__all__ = ['RequiredArgumentError']


class RequiredArgumentError(Exception):
    """:class:`Exception` raised if a required argument is missing."""

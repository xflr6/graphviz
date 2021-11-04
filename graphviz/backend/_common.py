"""Common backend constants."""

__all__ = ['RequiredArgumentError']


class RequiredArgumentError(Exception):
    """Exception raised if a required argument is missing (i.e. ``None``)."""

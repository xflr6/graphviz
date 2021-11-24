"""Commonly used exception classes."""

__all__ = ['RequiredArgumentError', 'FileExistsError']


class RequiredArgumentError(TypeError):
    """:class:`TypeError` raised if a required argument is missing."""


class FileExistsError(FileExistsError):
    """:class:`FileNotFoundError` raised with ``raise_if_exists=True``."""

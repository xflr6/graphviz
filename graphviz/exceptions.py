"""Commonly used exception classes."""

__all__ = ['RequiredArgumentError', 'FileExistsError',
           'UnknownSuffixWarning', 'FormatSuffixMismatchWarning']


class RequiredArgumentError(TypeError):
    """:class:`TypeError` raised if a required argument is missing."""


class FileExistsError(FileExistsError):
    """:class:`FileNotFoundError` raised with ``raise_if_exists=True``."""


class UnknownSuffixWarning(UserWarning):
    """:class:`UserWarning` raised for unknown ``outfile`` suffix."""


class FormatSuffixMismatchWarning(UserWarning):
    """:class:`UserWarning` raised for ``format`` mismatch with ``outfile`` suffix."""

"""Commonly used exception classes."""

from .backend.execute import ExecutableNotFound, CalledProcessError

__all__ = ['RequiredArgumentError', 'FileExistsError',
           'UnknownSuffixWarning', 'FormatSuffixMismatchWarning',
           'ExecutableNotFound', 'CalledProcessError']


class RequiredArgumentError(TypeError):
    """:class:`TypeError` raised if a required argument is missing."""


class FileExistsError(FileExistsError):
    """:class:`FileNotFoundError` raised with ``raise_if_exists=True``."""


class UnknownSuffixWarning(RuntimeWarning):
    """:class:`RuntimeWarning` raised if the suffix of ``outfile`` is unknown
        and the given ``format`` is used instead."""


class FormatSuffixMismatchWarning(UserWarning):
    """:class:`UserWarning` raised if the suffix ``outfile``
        does not match the given ``format``."""

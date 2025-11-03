#!/usr/bin/env python3

"""Run code linting with https://flake8.pycqa.org."""

import pathlib
import sys

import flake8.main.cli


if __name__ == '__main__':
    print('run', [pathlib.Path(__file__).name] + sys.argv[1:])
    args = sys.argv[1:]

    # https://flake8.pycqa.org/en/latest/internal/cli.html#flake8.main.cli.main
    print(f'flake8.main.cli.main({args!r})')
    if (returncode := flake8.main.cli.main(args)):
        print('FAILED:', returncode)
        sys.exit(returncode)
    print('PASSED.')

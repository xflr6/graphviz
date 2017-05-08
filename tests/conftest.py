# conftest.py

import re

import pytest


@pytest.fixture(scope='session')
def svg_pattern():
    return re.compile(r'(?s)^<\?xml .+</svg>\s*$')

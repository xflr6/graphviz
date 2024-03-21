import pathlib
from setuptools import setup, find_packages

setup(
    name='graphviz',
    version='0.20.3',
    author='Sebastian Bank',
    author_email='sebastian.bank@uni-leipzig.de',
    description='Simple Python interface for Graphviz',
    keywords='graph visualization dot render',
    license='MIT',
    url='https://github.com/xflr6/graphviz',
    project_urls={
        'Documentation': 'https://graphviz.readthedocs.io',
        'Changelog': 'https://graphviz.readthedocs.io/en/latest/changelog.html',
        'Issue Tracker': 'https://github.com/xflr6/graphviz/issues',
        'CI': 'https://github.com/xflr6/graphviz/actions',
        'Coverage': 'https://codecov.io/gh/xflr6/graphviz',
    },
    packages=find_packages(),
    platforms='any',
    python_requires='>=3.8',
    extras_require={
        'dev': ['tox>=3', 'flake8', 'pep8-naming', 'wheel', 'twine'],
        'test': ['pytest>=7,<8.1',  # https://github.com/pytest-dev/pytest/issues/12123
                 'pytest-mock>=3',
                 'pytest-cov', 'coverage'],
        'docs': ['sphinx>=5,<7', 'sphinx-autodoc-typehints', 'sphinx-rtd-theme'],
    },
    long_description=pathlib.Path('README.rst').read_text(encoding='utf-8'),
    long_description_content_type='text/x-rst',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
)

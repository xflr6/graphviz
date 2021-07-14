import pathlib
from setuptools import setup, find_packages

setup(
    name='graphviz',
    version='0.17.1.dev0',
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
    python_requires='>=3.6',
    extras_require={
        'dev': ['tox>=3', 'flake8', 'pep8-naming', 'wheel', 'twine'],
        'test': ['mock>=3', 'pytest>=5.2', 'pytest-mock>=2', 'pytest-cov'],
        'docs': ['sphinx>=1.8', 'sphinx-autodoc-typehints', 'sphinx-rtd-theme'],
    },
    long_description=pathlib.Path('README.rst').read_text(encoding='utf-8'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
)

# setup.py

import io
from setuptools import setup, find_packages

setup(
    name='graphviz',
    version='0.10.1',
    author='Sebastian Bank',
    author_email='sebastian.bank@uni-leipzig.de',
    description='Simple Python interface for Graphviz',
    keywords='graph visualization dot render',
    license='MIT',
    url='https://github.com/xflr6/graphviz',
    packages=find_packages(),
    platforms='any',
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    extras_require={
        'dev': ['tox>=3.0', 'flake8', 'pep8-naming', 'wheel', 'twine'],
        'test': ['mock>=2', 'pytest>=3.4', 'pytest-mock>=1.8', 'pytest-cov'],
        'docs': ['sphinx>=1.7', 'sphinx-rtd-theme'],
    },
    long_description=io.open('README.rst', encoding='utf-8').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
)

# setup.py

from setuptools import setup, find_packages

setup(
    name='graphviz',
    version='0.4.8',
    author='Sebastian Bank',
    author_email='sebastian.bank@uni-leipzig.de',
    description='Simple Python interface for Graphviz',
    keywords='graph visualization dot render',
    license='MIT',
    url='http://github.com/xflr6/graphviz',
    packages=find_packages(),
    extras_require={
        'test': ['unittest2', 'nose', 'coverage', 'flake8', 'pep8-naming'],
        'dev': ['wheel'],
    },
    platforms='any',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

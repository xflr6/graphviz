# setup.py

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
setup(
    name='graphviz',
    version='0.2.1',
    author='Sebastian Bank',
    author_email='sebastian.bank@uni-leipzig.de',
    description='Simple Python interface for Graphviz',
    license='MIT',
    keywords='graph visualization dot render',
    url='http://github.com/xflr6/graphviz',
    packages=['graphviz'],
    platforms='any',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

import os
import sys
from setuptools import setup
from treelib import __version__

setup(
    name = "treelib",
    version = __version__,
    url = '',
    author = 'caesar0301',
    author_email = 'chenxm35@gmail.com',
    description = 'A Python 2/3 implementation of tree structure.',
    long_description='''This is a simple tree data structure implementation in python.''',
    license = "LICENSE",
    packages = ['treelib'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: Freely Distributable',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.2',
            'Topic :: Software Development :: Libraries :: Python Modules',
   ],
)

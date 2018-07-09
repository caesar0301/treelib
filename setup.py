from setuptools import setup

from treelib import __version__

setup(
    name="treelib",
    version=__version__,
    url='https://github.com/caesar0301/treelib',
    author='Xiaming Chen',
    author_email='chenxm35@gmail.com',
    description='A Python 2/3 implementation of tree structure.',
    long_description='''This is a simple tree data structure implementation in python.''',
    license="Apache License, Version 2.0",
    packages=['treelib'],
    keywords=['data structure', 'tree', 'tools'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
   ],
)

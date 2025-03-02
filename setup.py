from setuptools import setup

__version__ = "1.7.1"


setup(
    name="treelib",
    version=__version__,
    url="https://github.com/caesar0301/treelib",
    author="Xiaming Chen",
    author_email="chenxm35@gmail.com",
    description="A Python implementation of tree structure.",
    long_description="""This is a simple tree data structure implementation in python.""",
    license="Apache License, Version 2.0",
    packages=["treelib"],
    keywords=["data structure", "tree", "tools"],
    install_requires=["six"],
    include_package_data=True,
    package_data={"": ["py.typed"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)

#!/usr/bin/env python

"""
Example of treelib usage to generate recursive tree of directories.
It could be useful to implement Directory Tree data structure

2016 samuelsh
"""

import treelib
import random
import hashlib
from string import digits, letters
import sys


MAX_FILES_PER_DIR = 10


def range2(stop):
    if sys.version_info[0] < 3:
        return xrange(stop)  # noqa: F821
    else:
        return range(stop)


def get_random_string(length):
    return "".join(random.choice(digits + letters) for _ in range2(length))


def build_recursive_tree(tree, base, depth, width):
    """
    Args:
        tree: Tree
        base: Node
        depth: int
        width: int

    Returns:

    """
    if depth >= 0:
        depth -= 1
        for i in range2(width):
            directory = Directory()
            tree.create_node(
                "{0}".format(directory.name),
                "{0}".format(hashlib.md5(directory.name)),
                parent=base.identifier,
                data=directory,
            )  # node identifier is md5 hash of it's name
        dirs_nodes = tree.children(base.identifier)
        for dir in dirs_nodes:
            newbase = tree.get_node(dir.identifier)
            build_recursive_tree(tree, newbase, depth, width)
    else:
        return


class Directory(object):
    def __init__(self):
        self._name = get_random_string(64)
        self._files = [
            File() for _ in range2(MAX_FILES_PER_DIR)
        ]  # Each directory contains 1000 files

    @property
    def name(self):
        return self._name

    @property
    def files(self):
        return self._files


class File(object):
    def __init__(self):
        self._name = get_random_string(64)

    @property
    def name(self):
        return self._name


tree = treelib.Tree()
base = tree.create_node("Root", "root")
build_recursive_tree(tree, base, 2, 10)

tree.show()

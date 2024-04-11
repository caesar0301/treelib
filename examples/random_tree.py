#!/usr/bin/env python3

"""
Generate a tree randomly; Test the `apply` method;
"""

import random
from treelib import Tree


def _random(max_depth=5, min_width=1, max_width=2, offset=()):
    # generate a tree randomly
    tree = Tree()
    tree.create_node(identifier=offset)
    if max_depth == 0:
        return tree
    elif max_depth == 1:
        nb = random.randint(min_width, max_width)
        for i in range(nb):
            identifier = offset + (i,)
            tree.create_node(identifier=identifier, parent=offset)
    else:
        nb = random.randint(min_width, max_width)
        for i in range(nb):
            subtree = _random(max_depth=max_depth-1, max_width=max_width, offset=offset+(i,))
            tree.paste(offset, subtree)
    return tree


def _map(func, tree):
    # tree as a functor
    tree = tree._clone(with_tree=True)
    print(tree)
    for a in tree.all_nodes_itr():
        key(a)
    return tree


def key(node):
    node.tag = ''.join(map(str, node.identifier))


print(_map(key, _random()))

print(_random().apply(key))

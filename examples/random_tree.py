"""
Generate a tree randomly
"""

import random
from treelib import Tree

def _random(max_depth=5, min_width=1, max_width=2, offset=(0,)):
    # just have fun
    tree = Tree()
    root = tree.create_node(identifier=offset)
    if max_depth == 0:
        return tree
    elif max_depth ==1:
        nb = random.randint(min_width, max_width)
        for i in range(nb):
            tree.create_node(identifier=offset+(i,), parent=offset)
    else:
        nb = random.randint(min_width, max_width)
        for i in range(nb):
            subtree = _random(max_depth=max_depth-1, max_width=max_width, offset=offset+(i,))
            tree.paste(offset, subtree)
    return tree

print(_random())

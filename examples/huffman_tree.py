#!/usr/bin/env python


"""Huffman coding
"""

from toolz import concat
from treelib import Tree, Node

import numpy as np


def _get_symbols(tree):
    """Get `symbols` from the root of a tree or a node

    tree: Tree or Node
    """
    if isinstance(tree, Node):
        a = tree.data['symbols']
    else:
        a = tree.get_node(tree.root).data['symbols']
    if isinstance(a, str):
        return [a]
    else:
        return a


def _get_frequency(tree):
    """Get `frequency` from the root of a tree or a node

    tree: Tree or Node
    """
    if isinstance(tree, Node):
        a = tree.data['frequency']
    else:
        a = tree.get_node(tree.root).data['frequency']
    if isinstance(a, str):
        return [a]
    else:
        return a


def merge(trees, level=''):
    """merge the trees to one tree by add a root

    Args:
        trees (list): list of trees or nodes
        level (tuple, optional): the prefix for identifier

    Returns:
        Tree
    """

    data = list(concat(map(_get_symbols, trees)))
    freq = sum(map(_get_frequency, trees))
    t = Tree()
    root = Node(tag='', identifier=level, data={'symbols': data, 'frequency': freq, 'code': ''})
    t.add_node(root)
    t.root = level
    root.tag = f"{root.data['code']}:{{{','.join(root.data['symbols'])}}}/{root.data['frequency']}"
    for k, tree in enumerate(trees):
        if isinstance(tree, Node):
            tree.identifier = f'{k}' + tree.identifier
            tree.data['code'] = f'{k}' + tree.data['code']
            tree.tag = f"{tree.data['code']}:{{{','.join(tree.data['symbols'])}}}/{tree.data['frequency']}"
            t.add_node(tree, parent=level)
        else:
            for n in tree.all_nodes_itr():
                n.identifier = f'{k}' + n.identifier
                n.data['code'] = f'{k}' + n.data['code']
                n.tag = f"{n.data['code']}:{{{','.join(n.data['symbols'])}}}/{n.data['frequency']}"

            nodes = {n.identifier: n for k, n in tree._nodes.items()}
            tree._nodes = nodes
            tree.root = f'{k}' + tree.root
            for n in tree.all_nodes_itr():
                if n.is_root():
                    n.set_successors([f'{k}' + nid for nid in n._successors[tree.identifier]], tree.identifier)
                elif n.is_leaf():
                    n.set_predecessor(f'{k}' + n._predecessor[tree.identifier], tree.identifier)
                else:
                    n.set_predecessor(f'{k}' + n._predecessor[tree.identifier], tree.identifier)
                    n.set_successors([f'{k}' + nid for nid in n._successors[tree.identifier]], tree.identifier)

            t.paste(level, tree, deep=True)
    return t


def huffman_tree(trees, level='', n_branches=2):
    """Huffman coding

    Args:
        trees (list): list of trees or nodes
        level (tuple, optional): the prefix for identifier
        set n_branches=2 by default

    Returns:
        Tree: Huffman tree
    """
    if len(trees) == 2:
        return merge(trees, level=level)
    else:
        ks = np.argsort([_get_frequency(tree) for tree in trees])[:n_branches]
        t = merge([trees[k] for k in ks], level=level)
        t = huffman_tree([t] + [tree for i, tree in enumerate(trees) if i not in ks], level=level)
        t.tag = 'root'
        return t


d = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
nodes = [Node(identifier='', data={'symbols': s, 'frequency': f, 'code': ''}) for s, f in d.items()]
t = huffman_tree(nodes)

print(t)

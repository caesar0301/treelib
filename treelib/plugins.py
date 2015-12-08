#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This is a public location to maintain contributed
   utilities to extend the basic Tree class.
"""
from __future__ import unicode_literals
import codecs


def export_to_dot(tree, filename, shape='circle', graph='digraph'):
    """Exports the tree in the dot format of the graphviz software"""
        
    nodes, connections = [], []
    if tree.nodes:        
        
        for n in tree.expand_tree(mode=tree.WIDTH):
            nid = tree[n].identifier
            state = '"' + nid + '"' + ' [label="' + tree[n].tag + '", shape=' + shape + ']'
            nodes.append(state)

            for c in tree.children(nid):
                cid = c.identifier

                connections.append('"' + nid + '"' + ' -> ' + '"' + cid + '"')

    # write nodes and connections to dot format
    with codecs.open(filename, 'w', 'utf-8') as f:
        f.write(graph + ' tree {\n')
        for n in nodes:
            f.write('\t' + n + '\n')
        
        f.write('\n')
        for c in connections:
            f.write('\t' + c + '\n')

        f.write('}')

if __name__ == '__main__':
    pass

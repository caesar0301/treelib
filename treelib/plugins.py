#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2011
# Brett Alistair Kromkamp - brettkromkamp@gmail.com
# Copyright (C) 2012-2017
# Xiaming Chen - chenxm35@gmail.com
# and other contributors.
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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

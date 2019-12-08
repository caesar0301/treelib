#!/usr/bin/env python
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
"""
Node structure in treelib.

A :class:`Node` object contains basic properties such as node identifier,
node tag, parent node, children nodes etc., and some operations for a node.
"""
from __future__ import unicode_literals

import copy
import uuid
from collections import defaultdict
from warnings import warn

from .exceptions import NodePropertyError
from .misc import deprecated


class Node(object):
    """
    Nodes are elementary objects that are stored in the `_nodes` dictionary of a Tree.
    Use `data` attribute to store node-specific data.
    """

    #: Mode constants for routine `update_fpointer()`.
    (ADD, DELETE, INSERT, REPLACE) = list(range(4))

    def __init__(self, tag=None, identifier=None, expanded=True, data=None):
        """Create a new Node object to be placed inside a Tree object"""

        #: if given as a parameter, must be unique
        self._identifier = None
        self._set_identifier(identifier)

        #: None or something else
        #: if None, self._identifier will be set to the identifier's value.
        if tag is None:
            self._tag = self._identifier
        else:
            self._tag = tag

        #: boolean
        self.expanded = expanded

        #: identifier of the parent's node :
        self._predecessor = {}
        #: identifier(s) of the soons' node(s) :
        self._successors = defaultdict(list)

        #: User payload associated with this node.
        self.data = data

        # for retro-compatilibity on bpointer/fpointer
        self._initial_tree_id = None

    def __lt__(self, other):
        return self.tag < other.tag

    def set_initial_tree_id(self, tree_id):
        if self._initial_tree_id is None:
            self._initial_tree_id = tree_id

    def _set_identifier(self, nid):
        """Initialize self._set_identifier"""
        if nid is None:
            self._identifier = str(uuid.uuid1())
        else:
            self._identifier = nid

    @property
    @deprecated(alias='node.predecessor')
    def bpointer(self):
        """Use predecessor method, this property is deprecated and only kept for retro-compatilibity. Parents of
        a node are dependant on a given tree. This implementation keeps the previous behavior by keeping returning 
        bpointer of first declared tree.
        """
        if self._initial_tree_id not in self._predecessor.keys():
            return None
        return self._predecessor[self._initial_tree_id]

    @bpointer.setter
    @deprecated(alias='node.set_predecessor')
    def bpointer(self, value):
        self.set_predecessor(self._initial_tree_id, value)

    @deprecated(alias='node.set_predecessor')
    def update_bpointer(self, nid):
        self.set_predecessor(self._initial_tree_id, nid)

    @property
    @deprecated(alias='node.successors')
    def fpointer(self):
        """Use successors method, this property is deprecated and only kept for retro-compatilibity. Children of
        a node are dependant on a given tree. This implementation keeps the previous behavior by keeping returning
        fpointer of first declared tree.
        """
        if self._initial_tree_id not in self._successors:
            return []
        return self._successors[self._initial_tree_id]

    @fpointer.setter
    @deprecated(alias='node.update_successors')
    def fpointer(self, value):
        self.set_successors(value, tree_id=self._initial_tree_id)

    @deprecated(alias='node.update_successors')
    def update_fpointer(self, nid, mode=ADD, replace=None):
        """Deprecated"""
        self.update_successors(nid, mode, replace, self._initial_tree_id)

    def predecessor(self, tree_id):
        """
        The parent ID of a node in a given tree.
        """
        return self._predecessor[tree_id]

    def set_predecessor(self, tree_id, nid):
        """Set the value of `_predecessor`."""
        self._predecessor[tree_id] = nid

    def successors(self, tree_id):
        """
        With a getting operator, a list of IDs of node's children is obtained. With
        a setting operator, the value can be list, set, or dict. For list or set,
        it is converted to a list type by the package; for dict, the keys are
        treated as the node IDs.
        """
        return self._successors[tree_id]

    def set_successors(self, value, tree_id=None):
        """Set the value of `_successors`."""
        if value is None:
            self._successors[tree_id] = list()
        elif isinstance(value, list):
            self._successors[tree_id] = value
        elif isinstance(value, dict):
            self._successors[tree_id] = list(value.keys())
        elif isinstance(value, set):
            self._successors[tree_id] = list(value)
        else:  # TODO: add deprecated routine
            pass

    def update_successors(self, nid, mode=ADD, replace=None, tid=None):
        """
        Update the children list with different modes: addition (Node.ADD or
        Node.INSERT) and deletion (Node.DELETE).
        """
        if nid is None:
            return

        if mode is self.ADD:
            self.successors(tid).append(nid)

        elif mode is self.DELETE:
            if nid in self.successors(tid):
                self.successors(tid).remove(nid)
            else:
                warn('Nid %s wasn\'t present in fpointer' % nid)

        elif mode is self.INSERT:  # deprecate to ADD mode
            warn("WARNING: INSERT is deprecated to ADD mode")
            self.update_successors(nid, tid=tid)

        elif mode is self.REPLACE:
            if replace is None:
                raise NodePropertyError(
                    'Argument "repalce" should be provided when mode is {}'.format(mode)
                )

            ind = self.successors(tid).index(nid)
            self.successors(tid)[ind] = replace

    @property
    def identifier(self):
        """
        The unique ID of a node within the scope of a tree. This attribute can be
        accessed and modified with ``.`` and ``=`` operator respectively.
        """
        return self._identifier

    def clone_pointers(self, former_tree_id, new_tree_id):
        former_bpointer = self.predecessor(former_tree_id)
        self.set_predecessor(new_tree_id, former_bpointer)
        former_fpointer = self.successors(former_tree_id)
        # fpointer is a list and would be copied by reference without deepcopy
        self.set_successors(copy.deepcopy(former_fpointer), tree_id=new_tree_id)

    def reset_pointers(self, tree_id):
        self.set_predecessor(tree_id, None)
        self.set_successors([], tree_id=tree_id)

    @identifier.setter
    def identifier(self, value):
        """Set the value of `_identifier`."""
        if value is None:
            print("WARNING: node ID can not be None")
        else:
            self._set_identifier(value)

    def is_leaf(self, tree_id=None):
        """Return true if current node has no children."""
        if tree_id is None:
            # for retro-compatilibity
            if self._initial_tree_id not in self._successors.keys():
                return True
            else:
                tree_id = self._initial_tree_id

        if len(self.successors(tree_id)) == 0:
            return True
        else:
            return False

    def is_root(self, tree_id=None):
        """Return true if self has no parent, i.e. as root."""
        if tree_id is None:
            # for retro-compatilibity
            if self._initial_tree_id not in self._predecessor.keys():
                return True
            else:
                tree_id = self._initial_tree_id

        return self.predecessor(tree_id) is None

    @property
    def tag(self):
        """
        The readable node name for human. This attribute can be accessed and
        modified with ``.`` and ``=`` operator respectively.
        """
        return self._tag

    @tag.setter
    def tag(self, value):
        """Set the value of `_tag`."""
        self._tag = value if value is not None else None

    def __repr__(self):
        name = self.__class__.__name__
        kwargs = [
            "tag={0}".format(self.tag),
            "identifier={0}".format(self.identifier),
            "data={0}".format(self.data),
        ]
        return "%s(%s)" % (name, ", ".join(kwargs))

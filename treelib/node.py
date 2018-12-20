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
import uuid

from .exceptions import NodePropertyError


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
        self._bpointer = None
        #: identifier(s) of the soons' node(s) :
        self._fpointer = list()

        #: User payload associated with this node.
        self.data = data

    def __lt__(self, other):
        return self.tag < other.tag

    def _set_identifier(self, nid):
        """Initialize self._set_identifier"""
        if nid is None:
            self._identifier = str(uuid.uuid1())
        else:
            self._identifier = nid

    @property
    def bpointer(self):
        """
        The parent ID of a node. This attribute can be
        accessed and modified with ``.`` and ``=`` operator respectively.
        """
        return self._bpointer

    @bpointer.setter
    def bpointer(self, nid):
        """Set the value of `_bpointer`."""
        if nid is not None:
            self._bpointer = nid
        else:
            # print("WARNING: the bpointer of node %s " \
            #      "is set to None" % self._identifier)
            self._bpointer = None

    @property
    def fpointer(self):
        """
        With a getting operator, a list of IDs of node's children is obtained. With
        a setting operator, the value can be list, set, or dict. For list or set,
        it is converted to a list type by the package; for dict, the keys are
        treated as the node IDs.
        """
        return self._fpointer

    @fpointer.setter
    def fpointer(self, value):
        """Set the value of `_fpointer`."""
        if value is None:
            self._fpointer = list()
        elif isinstance(value, list):
            self._fpointer = value
        elif isinstance(value, dict):
            self._fpointer = list(value.keys())
        elif isinstance(value, set):
            self._fpointer = list(value)
        else:  # TODO: add deprecated routine
            pass

    @property
    def identifier(self):
        """
        The unique ID of a node within the scope of a tree. This attribute can be
        accessed and modified with ``.`` and ``=`` operator respectively.
        """
        return self._identifier

    @identifier.setter
    def identifier(self, value):
        """Set the value of `_identifier`."""
        if value is None:
            print("WARNING: node ID can not be None")
        else:
            self._set_identifier(value)

    def is_leaf(self):
        """Return true if current node has no children."""
        if len(self.fpointer) == 0:
            return True
        else:
            return False

    def is_root(self):
        """Return true if self has no parent, i.e. as root."""
        return self._bpointer is None

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

    def update_bpointer(self, nid):
        """Set the parent (indicated by the ``nid`` parameter) of a node."""
        self.bpointer = nid

    def update_fpointer(self, nid, mode=ADD, replace=None):
        """
        Update the children list with different modes: addition (Node.ADD or
        Node.INSERT) and deletion (Node.DELETE).
        """
        if nid is None:
            return

        if mode is self.ADD:
            self._fpointer.append(nid)

        elif mode is self.DELETE:
            if nid in self._fpointer:
                self._fpointer.remove(nid)

        elif mode is self.INSERT:  # deprecate to ADD mode
            print("WARNING: INSERT is deprecated to ADD mode")
            self.update_fpointer(nid)

        elif mode is self.REPLACE:
            if replace is None:
                raise NodePropertyError(
                    'Argument "repalce" should be provided when mode is {}'.format(mode)
                )

            ind = self._fpointer.index(nid)
            self._fpointer[ind] = replace

    def __repr__(self):
        name = self.__class__.__name__
        kwargs = [
            "tag={0}".format(self.tag),
            "identifier={0}".format(self.identifier),
            "data={0}".format(self.data),
        ]
        return "%s(%s)" % (name, ", ".join(kwargs))

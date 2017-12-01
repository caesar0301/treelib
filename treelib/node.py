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
"""treelib - Simple to use for you.
   Python 2/3 Tree Implementation
"""

import uuid


class Node(object):
    """
    Nodes are elementary objects which are stored a `_nodes` dictionary of a Tree.
    Use `data` attribute to store node-specific data.
    """

    #: ADD, DELETE, INSERT constants :
    (ADD, DELETE, INSERT) = list(range(3))

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

        #: None or whatever given as a parameter
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
        """Return the value of `_bpointer`."""
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
        """Return the value of `_fpointer`."""
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
        """Return the value of `_identifier`."""
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
        """Return the value of `_tag`."""
        return self._tag

    @tag.setter
    def tag(self, value):
        """Set the value of `_tag`."""
        self._tag = value if value is not None else None

    def update_bpointer(self, nid):
        """Update parent node."""
        self.bpointer = nid

    def update_fpointer(self, nid, mode=ADD):
        """Update all children nodes."""
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

    def __repr__(self):
        name = self.__class__.__name__
        kwargs = [
            "tag={}".format(self.tag),
            "identifier={}".format(self.identifier),
            "data={}".format(self.data),
        ]
        return "%s(%s)" % (name, ", ".join(kwargs))

#!/usr/bin/env python
"""treelib - Simple to use for you.

   Python 2/3 Tree Implementation
"""

import uuid


class Node(object):
    """
    A Node object is stored inside the _nodes dictionary of a Tree object.
    Use Node objects to store data inside the data attribute.
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
        """return the value of _bpointer; see below for the setter"""
        return self._bpointer

    @bpointer.setter
    def bpointer(self, nid):
        """set the value of _bpointer; see above for the getter"""
        if nid is not None:
            self._bpointer = nid
        else:
            # print("WARNNING: the bpointer of node %s " \
            #      "is set to None" % self._identifier)
            self._bpointer = None

    @property
    def fpointer(self):
        """return the value of _fpointer; see below for the setter"""
        return self._fpointer

    @fpointer.setter
    def fpointer(self, value):
        """set the value of _fpointer; see above for the getter"""
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
        """return the value of _identifier; see below for the setter"""
        return self._identifier

    @identifier.setter
    def identifier(self, value):
        """set the value of _identifier; see above for the getter"""
        if value is None:
            print("WARNNING: node ID can not be None")
        else:
            self._set_identifier(value)

    def is_leaf(self):
        """return True if the the current node has no son"""
        if len(self.fpointer) == 0:
            return True
        else:
            return False

    def is_root(self):
        """return True if self has no parent, i.e. if self is root"""
        return self._bpointer is None

    @property
    def tag(self):
        """return the value if _tag; see below for the setter"""
        return self._tag

    @tag.setter
    def tag(self, value):
        """set the value if _tag; see above for the getter"""
        self._tag = value if value is not None else None

    def update_bpointer(self, nid):
        """set bpointer"""
        self.bpointer = nid

    def update_fpointer(self, nid, mode=ADD):
        """set _fpointer recursively"""
        if nid is None:
            return

        if mode is self.ADD:
            self._fpointer.append(nid)
        elif mode is self.DELETE:
            if nid in self._fpointer:
                self._fpointer.remove(nid)
        elif mode is self.INSERT:  # deprecate to ADD mode
            print("WARNNING: INSERT is deprecated to ADD mode")
            self.update_fpointer(nid)

if __name__ == '__main__':
    pass

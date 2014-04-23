#!/usr/bin/env python
"""

  treelib - Simple to use for you.
  Python 2/3 Tree Implementation

        node.py

        o       NodeIDTypeException class
        o       Node class
"""

import uuid


class NodeIDTypeException(Exception):
    """
        NodeIDTypeException class

        error class
    """
    pass


class Node(object):
    """
        Node class

        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        CLASS ATTRIBUTES :

        o ADD
        o DELETE
        o INSERT

        ATTRIBUTES :

        o _identifier
        o _tag
        o expanded
        o _bpointer
        o _fpointer
        o data

        METHODS :

        o __init__(self, tag=None, identifier=None, expanded=True, data=None)
        o __lt__(self, other)
        o _set_identifier(self, nid)
        o @property bpointer(self)
        o @bpointer.setter bpointer(self, nid)
        o @property fpointer(self)
        o @fpointer.setter fpointer(self, value)
        o @property identifier(self)
        o @identifier.setter identifier(self, value)
        o is_leaf(self)
        o @property tag(self)
        o @tag.setter tag(self, value)
        o update_bpointer(self, nid)
        o update_fpointer(self, nid, mode=ADD)
    """

    # ADD, DELETE, INSERT constants :
    (ADD, DELETE, INSERT) = list(range(3))

    def __init__(self, tag=None, identifier=None, expanded=True, data=None):
        """
                Node.__init__()

                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                PARAMETERS

                o node
                o tag           : None or something else
                                  if None, self._identifier will be set to the
                                  identifier's value.
                o identifier
                o expanded      : bool
                o data
        """
        self._identifier = None
        self._set_identifier(identifier)

        if tag is None:
            self._tag = self._identifier
        else:
            self._tag = tag

        self.expanded = expanded
        self._bpointer = None
        self._fpointer = list()
        self.data = data

    def __lt__(self, other):
        """
                Node.lt()

               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
               RETURN VALUE : a boolean
        """
        return self.tag < other.tag

    def _set_identifier(self, nid):
        """
                Node._set_identifier()

                Initialize self._set_identifier
        """
        if nid is None:
            self._identifier = str(uuid.uuid1())
        else:
            self._identifier = nid

    @property
    def bpointer(self):
        """
                Node.bpointer()
        """
        return self._bpointer

    @bpointer.setter
    def bpointer(self, nid):
        """
                Node.bpointer()
        """
        if nid is not None:
            self._bpointer = nid
        else:
            # print("WARNNING: the bpointer of node %s " \
            #      "is set to None" % self._identifier)
            self._bpointer = None

    @property
    def fpointer(self):
        """
                Node.fpointer()
        """
        return self._fpointer

    @fpointer.setter
    def fpointer(self, value):
        """
                Node.fpointer()
        """
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
                Node.identifier()

                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                RETURN VALUE : self._identifier
        """
        return self._identifier

    @identifier.setter
    def identifier(self, value):
        """
                Node.identifier()

                Initialize self._set_identifier
        """
        if value is None:
            print("WARNNING: node ID can not be None")
        else:
            self._set_identifier(value)

    def is_leaf(self):
        """
                Node.is_leaf()

                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                RETURN VALUE : a boolean
        """
        if len(self.fpointer) == 0:
            return True
        else:
            return False

    @property
    def tag(self):
        """
                Node.tag()

                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                RETURN VALUE: self._tag
        """
        return self._tag

    @tag.setter
    def tag(self, value):
        """
                Node.tag()

                Initialize self._tag
        """
        self._tag = value if value is not None else None

    def update_bpointer(self, nid):
        """
                Node.update_bpointer()
        """
        self.bpointer = nid

    def update_fpointer(self, nid, mode=ADD):
        """
                Node.update_fpointer()
        """
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

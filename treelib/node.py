import uuid


class NodeIDTypeException(Exception):
    pass

class Node(object):

    (ADD, DELETE, INSERT) = list(range(3))


    def __init__(self, tag=None, identifier=None, expanded=True, data=None):
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


    def _set_identifier(self, nid):
        if nid is None:
            self._identifier = str(uuid.uuid1())
        else:
            self._identifier = nid


    @property
    def tag(self):
        return self._tag


    @tag.setter
    def tag(self, value):
        self._tag = value if value is not None else None


    @property
    def identifier(self):
        return self._identifier


    @identifier.setter
    def identifier(self, value):
        if value is None:
            print("WARNNING: node ID can not be None")
        else:
            self._set_identifier(value)


    @property
    def bpointer(self):
        return self._bpointer


    @bpointer.setter
    def bpointer(self, nid):
        if nid is not None:
            self._bpointer = nid
        else:
            #print("WARNNING: the bpointer of node %s is set to None" % self._identifier)
            self._bpointer = None


    @property
    def fpointer(self):
        return self._fpointer


    @fpointer.setter
    def fpointer(self, value):
        if value is None:
            self._fpointer = list()
        elif isinstance(value, list):
            self._fpointer = value
        elif isinstance(value, dict):
            self._fpointer = list(value.keys())
        elif isinstance(value, set):
            self._fpointer = list(value)
        else: #TODO: add deprecated routine
            pass


    def update_bpointer(self, nid):
        self.bpointer = nid


    def update_fpointer(self, nid, mode=ADD):
        if nid is None:
            return
        if mode is self.ADD:
            self._fpointer.append(nid)
        elif mode is self.DELETE:
            if nid in self._fpointer:
                self._fpointer.remove(nid)
        elif mode is self.INSERT: # deprecate to ADD mode
            print("WARNNING: INSERT is deprecated to ADD mode")
            self.update_fpointer(nid)


    def is_leaf(self):
        if len(self.fpointer) == 0:
            return True
        else:
            return False

    def __lt__(self, other):
        return(self.tag < other.tag)


if __name__ == '__main__':
    pass
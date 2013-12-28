import uuid


class NodeIDTypeException(Exception):
    pass

class Node(object):

    (ADD, DELETE, INSERT) = list(range(3))


    def __init__(self, tag=None, identifier=None, expanded=True):
        self._identifier = None
        self._set_identifier(identifier)
        if tag is None:
            self._tag = str(self._identifier)
        else:
            self._tag = str(tag)
        self.expanded = expanded
        self._bpointer = None
        self._fpointer = list()


    def _set_identifier(self, identifier):
        if identifier is None:
            self._identifier = str(uuid.uuid1())
        else:
            self._identifier = self.sanitize_id(identifier)


    @classmethod
    def sanitize_id(cls, identifier):
        if isinstance(identifier, str):
            #return identifier.strip().replace(" ", "_")
            return identifier
        elif isinstance(identifier, int):
            return identifier
        else:
            raise NodeIDTypeException("Only string and integer types are supported currently")


    @property
    def tag(self):
        return self._tag


    @tag.setter
    def tag(self, value):
        self._tag = str(value) if value is not None else None


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
    def bpointer(self, identifier):
        if identifier is not None:
            self._bpointer = self.sanitize_id(identifier)
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


    def update_bpointer(self, identifier):
        self.bpointer = identifier


    def update_fpointer(self, identifier, mode=ADD):
        if identifier is None:
            return
        if mode is self.ADD:
            self._fpointer.append(self.sanitize_id(identifier))
        elif mode is self.DELETE:
            if identifier in self._fpointer:
                self._fpointer.remove(self.sanitize_id(identifier))
        elif mode is self.INSERT: # deprecate to ADD mode
            print("WARNNING: INSERT is deprecated to ADD mode")
            self.update_fpointer(identifier)


    def is_leaf(self):
        if len(self.fpointer) == 0:
            return True
        else:
            return False

    def __lt__(self, other):
        return(self.tag < other.tag)


if __name__ == '__main__':
    new_node = Node()
    print(new_node.tag)
    new_node.tag = "new node"
    print(new_node.tag)

    print(new_node.identifier)
    new_node.identifier = "my first node"
    print(new_node.identifier)

    print(new_node.bpointer)
    new_node.bpointer = "bpointer node"
    print(new_node.bpointer)
    new_node.update_bpointer(None)

    print(new_node.fpointer)
    new_node.update_fpointer("123", mode=Node.ADD)
    new_node.update_fpointer("124", mode=Node.DELETE)
    new_node.update_fpointer("124", mode=Node.INSERT)
    new_node.fpointer = {1:1,2:2}
    print(new_node.fpointer)

import uuid


(_ADD, _DELETE, _INSERT) = range(3)


class Node(object):
    def __init__(self, tag=None, identifier=None, expanded=True):
        self.tag = tag
        self._identifier = self.set_identifier(identifier)
        self.expanded = expanded
        self._bpointer = None
        self._fpointer = []


    def sanitize_id(self, identifier):
        return identifier.strip().replace(" ", "_")


    def set_identifier(self, identifier):
        if identifier is None:
            return str(uuid.uuid1())
        else:
            return self.sanitize_id(str(identifier))


    @property
    def identifier(self):
        return self._identifier


    @property
    def bpointer(self):
        return self._bpointer


    @bpointer.setter
    def bpointer(self, value):
        if value is not None:
            self._bpointer = self.sanitize_id(value)


    @property
    def fpointer(self):
        return self._fpointer


    @fpointer.setter
    def fpointer(self, value):
        if value is not None and isinstance(value, list):
            self._fpointer = value


    def update_fpointer(self, identifier, mode=_ADD):
        if mode is _ADD:
            self._fpointer.append(self.sanitize_id(identifier))
        elif mode is _DELETE:
            self._fpointer.remove(self.sanitize_id(identifier))
        elif mode is _INSERT:
            self._fpointer = [self.sanitize_id(identifier)]

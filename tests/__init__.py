
from treelib import Node, Tree


class CustomNode(Node):
    pass


class CustomTree(Tree):
    node_class = CustomNode

    def __init__(self, identifier, cool_stuff, **kwargs):
        self.cool_stuff = cool_stuff
        super(CustomTree, self).__init__(identifier=identifier, **kwargs)

    def _serialize_tree_metadata(self, **kwargs):
        d = super(CustomTree, self)._serialize_tree_metadata(**kwargs)
        d['stored_cool_stuff'] = self.cool_stuff
        return d

    @classmethod
    def _deserialize_tree_metadata(cls, d, **kwargs):
        dmodified = d.copy()
        dmodified['cool_stuff'] = dmodified.pop('stored_cool_stuff')
        return super(CustomTree, cls)._deserialize_tree_metadata(dmodified, **kwargs)

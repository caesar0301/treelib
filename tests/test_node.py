import unittest

from collections import defaultdict
from treelib import Node


class NodeCase(unittest.TestCase):
    def setUp(self):
        self.node1 = Node("Test One", "identifier 1")
        self.node2 = Node("Test Two", "identifier 2")

    def test_initialization(self):
        self.assertEqual(self.node1.tag, "Test One")
        self.assertEqual(self.node1.identifier, "identifier 1")
        # retro-compatibility
        self.assertEqual(self.node1.bpointer, None)
        self.assertEqual(self.node1.fpointer, [])

        self.assertEqual(self.node1.expanded, True)
        self.assertEqual(self.node1._predecessor, {})
        self.assertEqual(self.node1._successors, defaultdict(list))
        self.assertEqual(self.node1.data, None)

    def test_set_tag(self):
        self.node1.tag = "Test 1"
        self.assertEqual(self.node1.tag, "Test 1")
        self.node1.tag = "Test One"

    def test_object_as_node_tag(self):
        node = Node(tag=(0, 1))
        self.assertEqual(node.tag, (0, 1))
        self.assertTrue(node.__repr__().startswith('Node'))

    def test_set_identifier(self):
        self.node1.identifier = "ID1"
        self.assertEqual(self.node1.identifier, "ID1")
        self.node1.identifier = "identifier 1"

    def test_set_fpointer(self):
        # retro-compatibility
        self.node1.update_fpointer("identifier 2")
        self.assertEqual(self.node1.fpointer, ['identifier 2'])
        self.node1.fpointer = []
        self.assertEqual(self.node1.fpointer, [])

    def test_update_successors(self):
        self.node1.update_successors("identifier 2", tree_id="tree 1")
        self.assertEqual(self.node1.successors("tree 1"), ['identifier 2'])
        self.assertEqual(self.node1._successors["tree 1"], ['identifier 2'])
        self.node1.set_successors([], tree_id="tree 1")
        self.assertEqual(self.node1._successors["tree 1"], [])

    def test_set_bpointer(self):
        # retro-compatibility
        self.node2.update_bpointer("identifier 1")
        self.assertEqual(self.node2.bpointer, 'identifier 1')
        self.node2.bpointer = None
        self.assertEqual(self.node2.bpointer, None)

    def test_set_predecessor(self):
        self.node2.set_predecessor("identifier 1", "tree 1")
        self.assertEqual(self.node2.predecessor("tree 1"), 'identifier 1')
        self.assertEqual(self.node2._predecessor["tree 1"], 'identifier 1')
        self.node2.set_predecessor(None, "tree 1")
        self.assertEqual(self.node2.predecessor("tree 1"), None)

    def test_set_is_leaf(self):
        self.node1.update_fpointer("identifier 2")
        self.node2.update_bpointer("identifier 1")
        self.assertEqual(self.node1.is_leaf(), False)
        self.assertEqual(self.node2.is_leaf(), True)

    def test_tree_wise_is_leaf(self):
        self.node1.update_successors("identifier 2", tree_id="tree 1")
        self.node2.set_predecessor("identifier 1", "tree 1")
        self.assertEqual(self.node1.is_leaf("tree 1"), False)
        self.assertEqual(self.node2.is_leaf("tree 1"), True)

    def test_data(self):

        class Flower(object):
            def __init__(self, color):
                self.color = color

            def __str__(self):
                return "%s" % self.color

        self.node1.data = Flower("red")
        self.assertEqual(self.node1.data.color, "red")

    def test_simple_node_serialization(self):
        # serialization
        n = Node(identifier='id', tag='some_tag', expanded=True, data=2)
        self.assertEqual(
            n.serialize(),
            {'identifier': 'id', 'tag': 'some_tag', 'expanded': True, 'data':None}
        )
        # deserialization
        sn = Node.deserialize({'identifier': 'id', 'tag': 'some_tag', 'expanded': True, 'data': None})
        self.assertIsInstance(sn, Node)
        self.assertEqual(sn.tag, 'some_tag')
        self.assertEqual(sn.identifier, 'id')
        self.assertEqual(sn.expanded, True)
        # no data serialization was provided in this class
        self.assertEqual(sn.data, None)

    def test_custom_node_serialization(self):
        class Flower(object):
            def __init__(self, color):
                self.color = color

        class CustomNode(Node):
            def _serialize_data(self, **kwargs):
                return {'flower_color': self.data.color}

            @classmethod
            def _deserialize_data(cls, d, **kwargs):
                return Flower(color=d['flower_color'])

        # serialization
        cn = CustomNode(tag='blue_flower', identifier='id2', data=Flower(color='blue'))

        self.assertEqual(
            cn.serialize(),
            {
                'identifier': 'id2',
                'tag': 'blue_flower',
                'expanded': True,
                'data': {'flower_color': 'blue'}
            }
        )
        # deserialization
        csn = CustomNode.deserialize({
            'identifier': 'id2',
            'tag': 'blue_flower',
            'expanded': True,
            'data': {'flower_color': 'blue'}
        })

        self.assertIsInstance(csn, CustomNode)
        self.assertEqual(csn.tag, 'blue_flower')
        self.assertEqual(csn.identifier, 'id2')
        self.assertEqual(csn.expanded, True)
        self.assertIsInstance(csn.data, Flower)
        self.assertEqual(csn.data.color, 'blue')

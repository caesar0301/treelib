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
        self.assertEqual(self.node1._bpointer, {})
        self.assertEqual(self.node1._fpointer, defaultdict(list))
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

    def test_set_fpointer_in_tree(self):
        self.node1.update_fpointer_in_tree("tree 1", "identifier 2")
        self.assertEqual(self.node1.fpointer_in_tree("tree 1"), ['identifier 2'])
        self.assertEqual(self.node1._fpointer["tree 1"], ['identifier 2'])
        self.node1.set_fpointer_in_tree("tree 1", [])
        self.assertEqual(self.node1._fpointer["tree 1"], [])

    def test_set_bpointer(self):
        # retro-compatibility
        self.node2.update_bpointer("identifier 1")
        self.assertEqual(self.node2.bpointer, 'identifier 1')
        self.node2.bpointer = None
        self.assertEqual(self.node2.bpointer, None)

    def test_set_bpointer_in_tree(self):
        self.node2.update_bpointer_in_tree("tree 1", "identifier 1")
        self.assertEqual(self.node2.bpointer_in_tree("tree 1"), 'identifier 1')
        self.assertEqual(self.node2._bpointer["tree 1"], 'identifier 1')
        self.node2.update_bpointer_in_tree("tree 1", None)
        self.assertEqual(self.node2.bpointer_in_tree("tree 1"), None)

    def test_set_is_leaf(self):
        self.node1.update_fpointer("identifier 2")
        self.node2.update_bpointer("identifier 1")
        self.assertEqual(self.node1.is_leaf(), False)
        self.assertEqual(self.node2.is_leaf(), True)

    def test_set_is_leaf_in_tree(self):
        self.node1.update_fpointer_in_tree("tree 1", "identifier 2")
        self.node2.update_bpointer_in_tree("tree 1", "identifier 1")
        self.assertEqual(self.node1.is_leaf_in_tree("tree 1"), False)
        self.assertEqual(self.node2.is_leaf_in_tree("tree 1"), True)

    def test_data(self):

        class Flower(object):
            def __init__(self, color):
                self.color = color

            def __str__(self):
                return "%s" % self.color

        self.node1.data = Flower("red")
        self.assertEqual(self.node1.data.color, "red")

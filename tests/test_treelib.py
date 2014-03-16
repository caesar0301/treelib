#!/usr/bin/env python
import unittest
from treelib import Tree, Node
from treelib.tree import NodeIDAbsentError

class NodeCase(unittest.TestCase):
    def setUp(self):
        self.node1 = Node("Test One", "identifier 1")
        self.node2 = Node("Test Two", "identifier 2")

    def test_initialization(self):
        self.assertEqual(self.node1.tag, "Test One")
        self.assertEqual(self.node1.identifier, "identifier 1")
        self.assertEqual(self.node1.expanded, True)
        self.assertEqual(self.node1.bpointer, None)
        self.assertEqual(self.node1.fpointer, [])

    def test_set_tag(self):
        self.node1.tag = "Test 1"
        self.assertEqual(self.node1.tag, "Test 1")
        self.node1.tag = "Test One"

    def test_set_identifier(self):
        self.node1.identifier = "ID1"
        self.assertEqual(self.node1.identifier, "ID1")
        self.node1.identifier = "identifier 1"

    def test_set_fpointer(self):
        self.node1.update_fpointer("identifier 2")
        self.assertEqual(self.node1.fpointer, ['identifier 2'])
        self.node1.fpointer = []

    def test_set_bpointer(self):
        self.node2.update_bpointer("identifier 1")
        self.assertEqual(self.node2.bpointer, 'identifier 1')
        self.node2.bpointer = None

    def test_set_is_leaf(self):
        self.node1.update_fpointer("identifier 2")
        self.node2.update_bpointer("identifier 1")
        self.assertEqual(self.node1.is_leaf(), False)
        self.assertEqual(self.node2.is_leaf(), True)

    def tearDown(self):
        pass


class TreeCase(unittest.TestCase):
    def setUp(self):
        tree = Tree()
        tree.create_node("Harry", "harry")
        tree.create_node("Jane", "jane", parent="harry")
        tree.create_node("Bill", "bill", parent="harry")
        tree.create_node("Diane", "diane", parent="jane")
        tree.create_node("George", "george", parent="bill")
        self.tree = tree
        self.copytree = Tree(self.tree, True)

    def test_tree(self):
        self.assertEqual(isinstance(self.tree, Tree), True)
        self.assertEqual(isinstance(self.copytree, Tree), True)

    def test_nodes(self):
        self.assertEqual(len(self.tree.nodes), 5)
        self.assertEqual(len(self.tree.all_nodes()), 5)
        self.assertEqual(self.tree.size(), 5)

    def test_getitem(self):
        """Nodes can be accessed via getitem."""
        for node_id in self.tree.nodes:
            try:
                self.tree[node_id]
            except KeyError:
                self.fail('Node access should be possible via getitem.')
        try:
            self.tree['root']
        except KeyError:
            pass
        else:
            self.fail('There should be no default fallback value for getitem.')

    def test_parent(self):
        for nid in self.tree.nodes:
            if nid == self.tree.root:
                self.assertEqual(self.tree.parent(nid), None)
            else:
                self.assertEqual(self.tree.parent(nid) in self.tree.all_nodes(), True)

    def test_remove_node(self):
        self.tree.create_node("Jill", "jill", parent = "george")
        self.tree.create_node("Mark", "mark", parent = "jill")
        self.assertEqual(self.tree.remove_node("jill"), 2)
        self.assertEqual(self.tree.get_node("jill") is None, True)
        self.assertEqual(self.tree.get_node("mark") is None, True)

    def test_depth(self):
        # Try getting the level of this tree
        self.assertEqual(self.tree.depth(), 2)
        self.tree.create_node("Jill", "jill", parent = "george")
        self.assertEqual(self.tree.depth(), 3)
        self.tree.create_node("Mark", "mark", parent = "jill")
        self.assertEqual(self.tree.depth(), 4)

        # Try getting the level of the node
        """
        self.tree.show()
        Harry
        |___ Bill
        |    |___ George
        |         |___ Jill
        |              |___ Mark
        |___ Jane
        |    |___ Diane
        """
        self.assertEqual(self.tree.depth(self.tree.get_node("mark")), 4)
        self.assertEqual(self.tree.depth(self.tree.get_node("jill")), 3)
        self.assertEqual(self.tree.depth(self.tree.get_node("george")), 2)
        self.assertEqual(self.tree.depth(self.tree.get_node("jane")), 1)
        self.assertEqual(self.tree.depth(self.tree.get_node("bill")), 1)
        self.assertEqual(self.tree.depth(self.tree.get_node("harry")), 0)

        # Try getting Exception
        self.assertRaises(OSError, self.tree.depth, "raise OSError")
        node = Node("Test One", "identifier 1")
        self.assertRaises(NodeIDAbsentError, self.tree.depth, node)

        # Reset the test case
        self.tree.remove_node("jill")

    def tearDown(self):
        pass


def suite():
    suites = [NodeCase, TreeCase]
    suite = unittest.TestSuite()
    for s in suites:
        suite.addTest(unittest.makeSuite(s))
    return suite



if __name__ == '__main__':
    unittest.main(defaultTest='suite')

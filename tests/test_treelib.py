import unittest
from treelib import Tree, Node

class NodeCase(unittest.TestCase):
	def setUp(self):
		self.node1 = Node("Test One", "ide ntifier 1 ")

	def test_initialization(self):
		self.assertEqual(self.node1.tag, "Test One")
		self.assertEqual(self.node1.identifier, "ide_ntifier_1")
		self.assertEqual(self.node1.expanded, True)

	def test_set_fpointer(self):
		self.node1.update_fpointer(" identi fier 2")
		self.assertEqual(self.node1.fpointer, ['identi_fier_2'])

	def test_set_bpointer(self):
		self.node1.bpointer = " identi fier  1"
		self.assertEqual(self.node1.bpointer, 'identi_fier__1')

	def test_set_data(self):
		self.node1.data = {1:'hello', "two":'world'}
		self.assertEqual(self.node1.data, {1:'hello', "two":'world'})

	def tearDown(self):
		pass


class TreeCase(unittest.TestCase):
    def setUp(self):
        tree = Tree()
        tree.create_node("Harry", "harry")
        tree.create_node("Jane", "jane", parent="harry")
        tree.create_node("Bill", "bill", parent="harry")
        tree.create_node("Diane", "diane", parent="jane")
        tree.create_node("George", "george", parent="diane")
        tree.create_node("Mary", "mary", parent="diane")
        tree.create_node("Jill", "jill", parent="george")
        tree.create_node("Mark", "mark", parent="jane")
        self.tree = tree

    def test_tree(self):
        self.assertIsInstance(self.tree, Tree)

    def test_getitem(self):
        """Nodes can be accessed via getitem."""
        tree = Tree()
        tree.create_node("Harry", "harry")
        tree.create_node("Jane", "jane", parent="harry")

        for node_id in tree.nodes:
            try:
                tree[node_id]
            except KeyError:
                self.fail('Node access should be possible via getitem.')

        try:
            tree['root']
        except KeyError:
            pass
        else:
            self.fail('There should be no default fallback value for getitem.')

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

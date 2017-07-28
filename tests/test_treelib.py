#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import os
import codecs
try:
    from StringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO
import unittest
from treelib import Tree, Node
from treelib.tree import NodeIDAbsentError, LoopError

def encode(value):
    if sys.version_info[0] == 2:
        # Python2.x :
        return value.encode('utf-8')
    else:
        # Python3.x :
        return value


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
        self.assertEqual(self.node1.data, None)

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

    def test_data(self):
        class Flower(object):
            def __init__(self, color):
                self.color = color
            def __str__(self):
                return "%s" % self.color
        self.node1.data = Flower("red")
        self.assertEqual(self.node1.data.color, "red")

    def tearDown(self):
        pass


class TreeCase(unittest.TestCase):
    def setUp(self):
        tree = Tree()
        tree.create_node("Hárry", "hárry")
        tree.create_node("Jane", "jane", parent="hárry")
        tree.create_node("Bill", "bill", parent="hárry")
        tree.create_node("Diane", "diane", parent="jane")
        tree.create_node("George", "george", parent="bill")
        """
        Hárry
        ├── Bill
        │   └── George
        └── Jane
            └── Diane
        """
        self.tree = tree
        self.copytree = Tree(self.tree, True)

    def test_tree(self):
        self.assertEqual(isinstance(self.tree, Tree), True)
        self.assertEqual(isinstance(self.copytree, Tree), True)

    def test_is_root(self):
        self.assertTrue(self.tree._nodes['hárry'].is_root())
        self.assertFalse(self.tree._nodes['jane'].is_root())

    def test_paths_to_leaves(self):
        paths = self.tree.paths_to_leaves()
        self.assertEqual( len(paths), 2 )
        self.assertTrue( ['hárry', 'jane', 'diane'] in paths )
        self.assertTrue( ['hárry', 'bill', 'george'] in paths )

    def test_nodes(self):
        self.assertEqual(len(self.tree.nodes), 5)
        self.assertEqual(len(self.tree.all_nodes()), 5)
        self.assertEqual(self.tree.size(), 5)
        self.assertEqual(self.tree.get_node("jane").tag, "Jane")
        self.assertEqual(self.tree.contains("jane"), True)
        self.assertEqual("jane" in self.tree, True)
        self.assertEqual(self.tree.contains("alien"), False)
        self.tree.create_node("Alien","alien", parent="jane");
        self.assertEqual(self.tree.contains("alien"), True)
        self.tree.remove_node("alien")

    def test_getitem(self):
        """Nodes can be accessed via getitem."""
        for node_id in self.tree.nodes:
            try:
                self.tree[node_id]
            except NodeIDAbsentError:
                self.fail('Node access should be possible via getitem.')
        try:
            self.tree['root']
        except NodeIDAbsentError:
            pass
        else:
            self.fail('There should be no default fallback value for getitem.')

    def test_parent(self):
        for nid in self.tree.nodes:
            if nid == self.tree.root:
                self.assertEqual(self.tree.parent(nid), None)
            else:
                self.assertEqual(self.tree.parent(nid) in \
                                 self.tree.all_nodes(), True)

    def test_children(self):
        for nid in self.tree.nodes:
            children = self.tree.is_branch(nid)
            for child in children:
                self.assertEqual(self.tree[child] in self.tree.all_nodes(),
                                 True)
            children = self.tree.children(nid)
            for child in children:
                self.assertEqual(child in self.tree.all_nodes(), True)
        try:
            self.tree.is_branch("alien")
        except NodeIDAbsentError:
            pass
        else:
            self.fail("The absent node should be declaimed.")

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
        Hárry
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
        self.assertEqual(self.tree.depth("jane"), 1)
        self.assertEqual(self.tree.depth("bill"), 1)
        self.assertEqual(self.tree.depth("hárry"), 0)

        # Try getting Exception
        node = Node("Test One", "identifier 1")
        self.assertRaises(NodeIDAbsentError, self.tree.depth, node)

        # Reset the test case
        self.tree.remove_node("jill")

    def test_leaves(self):
        leaves = self.tree.leaves()
        for nid in self.tree.expand_tree():
            self.assertEqual((self.tree[nid].is_leaf()) == (self.tree[nid] \
                                                            in leaves), True)
        leaves = self.tree.leaves(nid='jane')
        for nid in self.tree.expand_tree(nid='jane'):
            self.assertEqual(self.tree[nid].is_leaf() == (self.tree[nid] in leaves), True)

    def test_link_past_node(self):
        self.tree.create_node("Jill", "jill", parent="hárry")
        self.tree.create_node("Mark", "mark", parent="jill")
        self.assertEqual("mark" not in self.tree.is_branch("hárry"), True)
        self.tree.link_past_node("jill")
        self.assertEqual("mark" in self.tree.is_branch("hárry"), True)

    def test_expand_tree(self):
        ## default config
        nodes = [nid for nid in self.tree.expand_tree()]
        # self.assertEqual(nodes, [u'h\xe1rry', u'bill', u'george', u'jane', u'diane'])
        self.assertEqual(len(nodes), 5)

        ## expanding from specific node
        nodes = [nid for nid in self.tree.expand_tree(nid="bill")]
        self.assertEqual(len(nodes), 2)

        ## changing into width mode
        nodes = [nid for nid in self.tree.expand_tree(mode=Tree.WIDTH)]
        # self.assertEqual(nodes, [u'h\xe1rry', u'bill', u'jane', u'george', u'diane'])
        self.assertEqual(len(nodes), 5)

        ## expanding by filters
        nodes = [nid for nid in self.tree.expand_tree(filter = lambda x: x.tag == "Bill")]
        self.assertEqual(len(nodes), 0)
        nodes = [nid for nid in self.tree.expand_tree(filter = lambda x: x.tag != "Bill")]
        # self.assertEqual(nodes, [u'h\xe1rry', u'jane', u'diane'])
        self.assertEqual(len(nodes), 3)

    def test_move_node(self):
        diane_parent = self.tree.parent("diane")
        self.tree.move_node("diane", "bill")
        self.assertEqual("diane" in self.tree.is_branch("bill"), True)
        self.tree.move_node("diane", diane_parent.identifier)

    def test_paste_tree(self):
        new_tree = Tree()
        new_tree.create_node("Jill", "jill")
        new_tree.create_node("Mark", "mark", parent="jill")
        self.tree.paste("jane", new_tree)
        self.assertEqual("jill" in self.tree.is_branch("jane"), True)
        self.tree.remove_node("jill")

    def test_rsearch(self):
        for nid in ["hárry", "jane", "diane"]:
            self.assertEqual(nid in self.tree.rsearch("diane"), True)

    def test_subtree(self):
        subtree_copy = Tree(self.tree.subtree("jane"), deep=True)
        self.assertEqual(subtree_copy.parent("jane") is None, True)
        subtree_copy["jane"].tag = "Sweeti"
        self.assertEqual(self.tree["jane"].tag == "Jane", True)
        self.assertEqual(subtree_copy.level("diane"), 1)
        self.assertEqual(subtree_copy.level("jane"), 0)
        self.assertEqual(self.tree.level("jane"), 1)

    def test_remove_subtree(self):
        subtree_shallow = self.tree.remove_subtree("jane")
        self.assertEqual("jane" not in self.tree.is_branch("hárry"), True)
        self.tree.paste("hárry", subtree_shallow)

    def test_to_json(self):
        self.assertEqual.__self__.maxDiff = None
        self.tree.to_json()
        self.tree.to_json(True)

    def test_siblings(self):
        self.assertEqual(len(self.tree.siblings("hárry")) == 0, True)
        self.assertEqual(self.tree.siblings("jane")[0].identifier == "bill",
                         True)

    def test_tree_data(self):
        class Flower(object):
            def __init__(self, color):
                self.color = color
        self.tree.create_node("Jill", "jill", parent="jane",
                              data=Flower("white"))
        self.assertEqual(self.tree["jill"].data.color, "white")
        self.tree.remove_node("jill")

    def test_show_data_property(self):
        new_tree = Tree()

        sys.stdout = open(os.devnull, "w")  # stops from printing to console

        try:
            new_tree.show()

            class Flower(object):
                def __init__(self, color):
                    self.color = color
            new_tree.create_node("Jill", "jill", data=Flower("white"))
            new_tree.show(data_property="color")
        finally:
            sys.stdout.close()
            sys.stdout = sys.__stdout__  # stops from printing to console

    def test_level(self):
        self.assertEqual(self.tree.level('hárry'),  0)
        depth = self.tree.depth()
        self.assertEqual(self.tree.level('diane'),  depth)
        self.assertEqual(self.tree.level('diane',
                                         lambda x: x.identifier!='jane'),
                         depth-1)

    def test_size(self):
        self.assertEqual(self.tree.size(level=2), 2)
        self.assertEqual(self.tree.size(level=1), 2)
        self.assertEqual(self.tree.size(level=0), 1)

    def test_print_backend(self):
        expected_result = """\
Hárry
├── Bill
│   └── George
└── Jane
    └── Diane
"""

        assert str(self.tree) == encode(expected_result)

    def test_show(self):
        if sys.version_info[0] < 3:
            reload(sys)
            sys.setdefaultencoding('utf-8')
        sys.stdout = open(os.devnull, "w")  # stops from printing to console

        try:
            self.tree.show()
        finally:
            sys.stdout.close()
            sys.stdout = sys.__stdout__  # stops from printing to console

    def tearDown(self):
        self.tree = None
        self.copytree = None

    def test_all_nodes_itr(self):
        """
        tests: Tree.all_nodes_iter
        Added by: William Rusnack
        """
        new_tree = Tree()
        self.assertEqual(len(new_tree.all_nodes_itr()), 0)
        nodes = []
        nodes.append(new_tree.create_node('root_node'))
        nodes.append(new_tree.create_node('second', parent=new_tree.root))
        for nd in new_tree.all_nodes_itr():
            self.assertTrue(nd in nodes)

    def test_filter_nodes(self):
        """
        tests: Tree.filter_nodes
        Added by: William Rusnack
        """
        new_tree = Tree()

        self.assertEqual(tuple(new_tree.filter_nodes(lambda n: True)), ())

        nodes = []
        nodes.append(new_tree.create_node('root_node'))
        nodes.append(new_tree.create_node('second', parent=new_tree.root))

        self.assertEqual(tuple(new_tree.filter_nodes(lambda n: False)), ())
        self.assertEqual(tuple(new_tree.filter_nodes(lambda n: n.is_root())), (nodes[0],))
        self.assertEqual(tuple(new_tree.filter_nodes(lambda n: not n.is_root())), (nodes[1],))
        self.assertTrue(set(new_tree.filter_nodes(lambda n: True)), set(nodes))

    def test_loop(self):
        tree = Tree()
        tree.create_node('a', 'a')
        tree.create_node('b', 'b', parent='a')
        tree.create_node('c', 'c', parent='b')
        tree.create_node('d', 'd', parent='c')
        try:
            tree.move_node('b', 'd')
        except LoopError:
            pass

def suite():
    suites = [NodeCase, TreeCase]
    suite = unittest.TestSuite()
    for s in suites:
        suite.addTest(unittest.makeSuite(s))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')

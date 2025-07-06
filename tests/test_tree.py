#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os
import sys
import unittest

from treelib import Node, Tree
from treelib.exceptions import (
    DuplicatedNodeIdError,
    LinkPastRootNodeError,
    MultipleRootError,
)
from treelib.tree import LoopError, NodeIDAbsentError


def encode(value):
    if sys.version_info[0] == 2:
        # Python2.x :
        return value.encode("utf-8")
    else:
        # Python3.x :
        return value


class TreeCase(unittest.TestCase):
    def setUp(self):
        tree = Tree(identifier="tree 1")
        tree.create_node("Hárry", "hárry")
        tree.create_node("Jane", "jane", parent="hárry")
        tree.create_node("Bill", "bill", parent="hárry")
        tree.create_node("Diane", "diane", parent="jane")
        tree.create_node("George", "george", parent="bill")
        # Hárry
        #   |-- Jane
        #       |-- Diane
        #   |-- Bill
        #       |-- George
        self.tree = tree
        self.copytree = Tree(self.tree, deep=True)
        self.input_dict = {
            "Bill": "Harry",
            "Jane": "Harry",
            "Harry": None,
            "Diane": "Jane",
            "Mark": "Jane",
            "Mary": "Harry",
        }

    @staticmethod
    def get_t1():
        """
        root
        ├── A
        │   └── A1
        └── B
        """
        t = Tree(identifier="t1")
        t.create_node(tag="root", identifier="r")
        t.create_node(tag="A", identifier="a", parent="r")
        t.create_node(tag="B", identifier="b", parent="r")
        t.create_node(tag="A1", identifier="a1", parent="a")
        return t

    @staticmethod
    def get_t2():
        """
        root2
        ├── C
        └── D
            └── D1
        """
        t = Tree(identifier="t2")
        t.create_node(tag="root2", identifier="r2")
        t.create_node(tag="C", identifier="c", parent="r2")
        t.create_node(tag="D", identifier="d", parent="r2")
        t.create_node(tag="D1", identifier="d1", parent="d")
        return t

    def test_tree(self):
        self.assertEqual(isinstance(self.tree, Tree), True)
        self.assertEqual(isinstance(self.copytree, Tree), True)

    def test_is_root(self):
        # retro-compatibility
        self.assertTrue(self.tree._nodes["hárry"].is_root())
        self.assertFalse(self.tree._nodes["jane"].is_root())

    def test_tree_wise_is_root(self):
        subtree = self.tree.subtree("jane", identifier="subtree 2")
        # harry is root of tree 1 but not present in subtree 2
        self.assertTrue(self.tree._nodes["hárry"].is_root("tree 1"))
        self.assertNotIn("hárry", subtree._nodes)
        # jane is not root of tree 1 but is root of subtree 2
        self.assertFalse(self.tree._nodes["jane"].is_root("tree 1"))
        self.assertTrue(subtree._nodes["jane"].is_root("subtree 2"))

    def test_paths_to_leaves(self):
        paths = self.tree.paths_to_leaves()
        self.assertEqual(len(paths), 2)
        self.assertTrue(["hárry", "jane", "diane"] in paths)
        self.assertTrue(["hárry", "bill", "george"] in paths)

    def test_nodes(self):
        self.assertEqual(len(self.tree.nodes), 5)
        self.assertEqual(len(self.tree.all_nodes()), 5)
        self.assertEqual(self.tree.size(), 5)
        self.assertEqual(self.tree.get_node("jane").tag, "Jane")
        self.assertEqual(self.tree.contains("jane"), True)
        self.assertEqual("jane" in self.tree, True)
        self.assertEqual(self.tree.contains("alien"), False)
        self.tree.create_node("Alien", "alien", parent="jane")
        self.assertEqual(self.tree.contains("alien"), True)
        self.tree.remove_node("alien")

    def test_getitem(self):
        """Nodes can be accessed via getitem."""
        for node_id in self.tree.nodes:
            try:
                self.tree[node_id]
            except NodeIDAbsentError:
                self.fail("Node access should be possible via getitem.")
        try:
            self.tree["root"]
        except NodeIDAbsentError:
            pass
        else:
            self.fail("There should be no default fallback value for getitem.")

    def test_parent(self):
        for nid in self.tree.nodes:
            if nid == self.tree.root:
                self.assertEqual(self.tree.parent(nid), None)
            else:
                self.assertEqual(self.tree.parent(nid) in self.tree.all_nodes(), True)

    def test_ancestor(self):
        for nid in self.tree.nodes:
            if nid == self.tree.root:
                self.assertEqual(self.tree.ancestor(nid), None)
            else:
                for level in range(self.tree.level(nid) - 1, 0, -1):
                    self.assertEqual(
                        self.tree.ancestor(nid, level=level) in self.tree.all_nodes(),
                        True,
                    )

    def test_children(self):
        for nid in self.tree.nodes:
            children = self.tree.is_branch(nid)
            for child in children:
                self.assertEqual(self.tree[child] in self.tree.all_nodes(), True)
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
        self.tree.create_node("Jill", "jill", parent="george")
        self.tree.create_node("Mark", "mark", parent="jill")
        self.assertEqual(self.tree.remove_node("jill"), 2)
        self.assertEqual(self.tree.get_node("jill") is None, True)
        self.assertEqual(self.tree.get_node("mark") is None, True)

    def test_tree_wise_depth(self):
        # Try getting the level of this tree
        self.assertEqual(self.tree.depth(), 2)
        self.tree.create_node("Jill", "jill", parent="george")
        self.assertEqual(self.tree.depth(), 3)
        self.tree.create_node("Mark", "mark", parent="jill")
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
        # retro-compatibility
        leaves = self.tree.leaves()
        for nid in self.tree.expand_tree():
            self.assertEqual((self.tree[nid].is_leaf()) == (self.tree[nid] in leaves), True)
        leaves = self.tree.leaves(nid="jane")
        for nid in self.tree.expand_tree(nid="jane"):
            self.assertEqual(self.tree[nid].is_leaf() == (self.tree[nid] in leaves), True)

    def test_tree_wise_leaves(self):
        leaves = self.tree.leaves()
        for nid in self.tree.expand_tree():
            self.assertEqual((self.tree[nid].is_leaf("tree 1")) == (self.tree[nid] in leaves), True)
        leaves = self.tree.leaves(nid="jane")
        for nid in self.tree.expand_tree(nid="jane"):
            self.assertEqual(self.tree[nid].is_leaf("tree 1") == (self.tree[nid] in leaves), True)

    def test_link_past_node(self):
        self.tree.create_node("Jill", "jill", parent="hárry")
        self.tree.create_node("Mark", "mark", parent="jill")
        self.assertEqual("mark" not in self.tree.is_branch("hárry"), True)
        self.tree.link_past_node("jill")
        self.assertEqual("mark" in self.tree.is_branch("hárry"), True)

    def test_expand_tree(self):
        # default config
        # Hárry
        #   |-- Jane
        #       |-- Diane
        #   |-- Bill
        #       |-- George
        # Traverse in depth first mode preserving insertion order
        nodes = [nid for nid in self.tree.expand_tree(sorting=False)]
        self.assertEqual(nodes, ["hárry", "jane", "diane", "bill", "george"])
        self.assertEqual(len(nodes), 5)

        # By default traverse depth first and sort child nodes by node tag
        nodes = [nid for nid in self.tree.expand_tree()]
        self.assertEqual(nodes, ["hárry", "bill", "george", "jane", "diane"])
        self.assertEqual(len(nodes), 5)

        # expanding from specific node
        nodes = [nid for nid in self.tree.expand_tree(nid="bill")]
        self.assertEqual(nodes, ["bill", "george"])
        self.assertEqual(len(nodes), 2)

        # changing into width mode preserving insertion order
        nodes = [nid for nid in self.tree.expand_tree(mode=Tree.WIDTH, sorting=False)]
        self.assertEqual(nodes, ["hárry", "jane", "bill", "diane", "george"])
        self.assertEqual(len(nodes), 5)

        # Breadth first mode, child nodes sorting by tag
        nodes = [nid for nid in self.tree.expand_tree(mode=Tree.WIDTH)]
        self.assertEqual(nodes, ["hárry", "bill", "jane", "george", "diane"])
        self.assertEqual(len(nodes), 5)

        # expanding by filters
        # Stops at root
        nodes = [nid for nid in self.tree.expand_tree(filter=lambda x: x.tag == "Bill")]
        self.assertEqual(len(nodes), 0)
        nodes = [nid for nid in self.tree.expand_tree(filter=lambda x: x.tag != "Bill")]
        self.assertEqual(nodes, ["hárry", "jane", "diane"])
        self.assertEqual(len(nodes), 3)

        # Test with filter - find nodes that are not leaves
        filtered = list(self.tree.expand_tree(filter=lambda node: not node.is_leaf(self.tree.identifier)))
        # Should find parent nodes with children
        self.assertGreater(len(filtered), 0)

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
        self.tree.show()
        self.assertEqual(
            self.tree._reader,
            """Hárry
├── Bill
│   └── George
└── Jane
    ├── Diane
    └── Jill
        └── Mark
""",
        )
        self.tree.remove_node("jill")
        self.assertNotIn("jill", self.tree.nodes.keys())
        self.assertNotIn("mark", self.tree.nodes.keys())
        self.tree.show()
        self.assertEqual(
            self.tree._reader,
            """Hárry
├── Bill
│   └── George
└── Jane
    └── Diane
""",
        )

    def test_merge(self):
        # merge on empty initial tree
        t1 = Tree(identifier="t1")
        t2 = self.get_t2()
        t1.merge(nid=None, new_tree=t2)

        self.assertEqual(t1.identifier, "t1")
        self.assertEqual(t1.root, "r2")
        self.assertEqual(set(t1._nodes.keys()), {"r2", "c", "d", "d1"})
        self.assertEqual(
            t1.show(stdout=False),
            """root2
├── C
└── D
    └── D1
""",
        )

        # merge empty new_tree (on root)
        t1 = self.get_t1()
        t2 = Tree(identifier="t2")
        t1.merge(nid="r", new_tree=t2)

        self.assertEqual(t1.identifier, "t1")
        self.assertEqual(t1.root, "r")
        self.assertEqual(set(t1._nodes.keys()), {"r", "a", "a1", "b"})
        self.assertEqual(
            t1.show(stdout=False),
            """root
├── A
│   └── A1
└── B
""",
        )

        # merge at root
        t1 = self.get_t1()
        t2 = self.get_t2()
        t1.merge(nid="r", new_tree=t2)

        self.assertEqual(t1.identifier, "t1")
        self.assertEqual(t1.root, "r")
        self.assertNotIn("r2", t1._nodes.keys())
        self.assertEqual(set(t1._nodes.keys()), {"r", "a", "a1", "b", "c", "d", "d1"})
        self.assertEqual(
            t1.show(stdout=False),
            """root
├── A
│   └── A1
├── B
├── C
└── D
    └── D1
""",
        )

        # merge on node
        t1 = self.get_t1()
        t2 = self.get_t2()
        t1.merge(nid="b", new_tree=t2)
        self.assertEqual(t1.identifier, "t1")
        self.assertEqual(t1.root, "r")
        self.assertNotIn("r2", t1._nodes.keys())
        self.assertEqual(set(t1._nodes.keys()), {"r", "a", "a1", "b", "c", "d", "d1"})
        self.assertEqual(
            t1.show(stdout=False),
            """root
├── A
│   └── A1
└── B
    ├── C
    └── D
        └── D1
""",
        )

    def test_paste(self):
        # paste under root
        t1 = self.get_t1()
        t2 = self.get_t2()
        t1.paste(nid="r", new_tree=t2)
        self.assertEqual(t1.identifier, "t1")
        self.assertEqual(t1.root, "r")
        self.assertEqual(t1.parent("r2").identifier, "r")
        self.assertEqual(set(t1._nodes.keys()), {"r", "r2", "a", "a1", "b", "c", "d", "d1"})
        self.assertEqual(
            t1.show(stdout=False),
            """root
├── A
│   └── A1
├── B
└── root2
    ├── C
    └── D
        └── D1
""",
        )

        # paste under non-existing node
        t1 = self.get_t1()
        t2 = self.get_t2()
        with self.assertRaises(NodeIDAbsentError) as e:
            t1.paste(nid="not_existing", new_tree=t2)
        self.assertEqual(e.exception.args[0], "Node 'not_existing' is not in the tree")

        # paste under None nid
        t1 = self.get_t1()
        t2 = self.get_t2()
        with self.assertRaises(ValueError) as e:
            t1.paste(nid=None, new_tree=t2)
        self.assertEqual(e.exception.args[0], 'Must define "nid" under which new tree is pasted.')

        # paste under node
        t1 = self.get_t1()
        t2 = self.get_t2()
        t1.paste(nid="b", new_tree=t2)
        self.assertEqual(t1.identifier, "t1")
        self.assertEqual(t1.root, "r")
        self.assertEqual(t1.parent("b").identifier, "r")
        self.assertEqual(set(t1._nodes.keys()), {"r", "a", "a1", "b", "c", "d", "d1", "r2"})
        self.assertEqual(
            t1.show(stdout=False),
            """root
├── A
│   └── A1
└── B
    └── root2
        ├── C
        └── D
            └── D1
""",
        )
        # paste empty new_tree (under root)
        t1 = self.get_t1()
        t2 = Tree(identifier="t2")
        t1.paste(nid="r", new_tree=t2)

        self.assertEqual(t1.identifier, "t1")
        self.assertEqual(t1.root, "r")
        self.assertEqual(set(t1._nodes.keys()), {"r", "a", "a1", "b"})
        self.assertEqual(
            t1.show(stdout=False),
            """root
├── A
│   └── A1
└── B
""",
        )

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

    def test_remove_subtree_whole_tree(self):
        self.tree.remove_subtree("hárry")
        self.assertIsNone(self.tree.root)
        self.assertEqual(len(self.tree.nodes.keys()), 0)

    def test_to_json(self):
        self.assertEqual.__self__.maxDiff = None
        self.tree.to_json()
        self.tree.to_json(True)

    def test_siblings(self):
        self.assertEqual(len(self.tree.siblings("hárry")) == 0, True)
        self.assertEqual(self.tree.siblings("jane")[0].identifier == "bill", True)

    def test_tree_data(self):
        class Flower(object):
            def __init__(self, color):
                self.color = color

        self.tree.create_node("Jill", "jill", parent="jane", data=Flower("white"))
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
        self.assertEqual(self.tree.level("hárry"), 0)
        depth = self.tree.depth()
        self.assertEqual(self.tree.level("diane"), depth)
        self.assertEqual(self.tree.level("diane", lambda x: x.identifier != "jane"), depth - 1)

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
            reload(sys)  # noqa: F821
            sys.setdefaultencoding("utf-8")
        sys.stdout = open(os.devnull, "w")  # stops from printing to console

        try:
            self.tree.show()
        finally:
            sys.stdout.close()
            sys.stdout = sys.__stdout__  # stops from printing to console

    def tearDown(self):
        self.tree = None
        self.copytree = None

    def test_show_without_sorting(self):
        t = Tree()
        t.create_node("Students", "Students", parent=None)
        Node(tag="Students", identifier="Students", data=None)
        t.create_node("Ben", "Ben", parent="Students")
        Node(tag="Ben", identifier="Ben", data=None)
        t.create_node("Annie", "Annie", parent="Students")
        Node(tag="Annie", identifier="Annie", data=None)
        t.show()
        self.assertEqual(
            t.show(sorting=False, stdout=False),
            """Students
├── Ben
└── Annie
""",
        )

    def test_all_nodes_itr(self):
        """
        tests: Tree.all_nodes_iter
        Added by: William Rusnack
        """
        new_tree = Tree()
        self.assertEqual(len(new_tree.all_nodes_itr()), 0)
        nodes = list()
        nodes.append(new_tree.create_node("root_node"))
        nodes.append(new_tree.create_node("second", parent=new_tree.root))
        for nd in new_tree.all_nodes_itr():
            self.assertTrue(nd in nodes)

    def test_filter_nodes(self):
        """
        tests: Tree.filter_nodes
        Added by: William Rusnack
        """
        new_tree = Tree(identifier="tree 1")

        self.assertEqual(tuple(new_tree.filter_nodes(lambda n: True)), ())

        nodes = list()
        nodes.append(new_tree.create_node("root_node"))
        nodes.append(new_tree.create_node("second", parent=new_tree.root))

        self.assertEqual(tuple(new_tree.filter_nodes(lambda n: False)), ())
        self.assertEqual(tuple(new_tree.filter_nodes(lambda n: n.is_root("tree 1"))), (nodes[0],))
        self.assertEqual(tuple(new_tree.filter_nodes(lambda n: not n.is_root("tree 1"))), (nodes[1],))
        self.assertTrue(set(new_tree.filter_nodes(lambda n: True)), set(nodes))

    def test_loop(self):
        tree = Tree()
        tree.create_node("a", "a")
        tree.create_node("b", "b", parent="a")
        tree.create_node("c", "c", parent="b")
        tree.create_node("d", "d", parent="c")
        try:
            tree.move_node("b", "d")
        except LoopError:
            pass

    def test_modify_node_identifier_directly_failed(self):
        tree = Tree()
        tree.create_node("Harry", "harry")
        tree.create_node("Jane", "jane", parent="harry")
        n = tree.get_node("jane")
        self.assertTrue(n.identifier == "jane")

        # Failed to modify
        n.identifier = "xyz"
        self.assertTrue(tree.get_node("xyz") is None)
        self.assertTrue(tree.get_node("jane").identifier == "xyz")

    def test_modify_node_identifier_recursively(self):
        tree = Tree()
        tree.create_node("Harry", "harry")
        tree.create_node("Jane", "jane", parent="harry")
        n = tree.get_node("jane")
        self.assertTrue(n.identifier == "jane")

        # Success to modify
        tree.update_node(n.identifier, identifier="xyz")
        self.assertTrue(tree.get_node("jane") is None)
        self.assertTrue(tree.get_node("xyz").identifier == "xyz")

    def test_modify_node_identifier_root(self):
        tree = Tree(identifier="tree 3")
        tree.create_node("Harry", "harry")
        tree.create_node("Jane", "jane", parent="harry")
        tree.update_node(tree["harry"].identifier, identifier="xyz", tag="XYZ")
        self.assertTrue(tree.root == "xyz")
        self.assertTrue(tree["xyz"].tag == "XYZ")
        self.assertEqual(tree.parent("jane").identifier, "xyz")

    def test_subclassing(self):
        class SubNode(Node):
            pass

        class SubTree(Tree):
            node_class = SubNode

        tree = SubTree()
        node = tree.create_node()
        self.assertTrue(isinstance(node, SubNode))

        tree = Tree(node_class=SubNode)
        node = tree.create_node()
        self.assertTrue(isinstance(node, SubNode))

    def test_shallow_copy_hermetic_pointers(self):
        # tree 1
        # Hárry
        #   └── Jane
        #       └── Diane
        #   └── Bill
        #       └── George
        tree2 = self.tree.subtree(nid="jane", identifier="tree 2")
        # tree 2
        # Jane
        #   └── Diane

        # check that in shallow copy, instances are the same
        self.assertIs(self.tree["jane"], tree2["jane"])
        self.assertEqual(self.tree["jane"]._predecessor, {"tree 1": "hárry", "tree 2": None})
        self.assertEqual(
            dict(self.tree["jane"]._successors),
            {"tree 1": ["diane"], "tree 2": ["diane"]},
        )

        # when creating new node on subtree, check that it has no impact on
        # initial tree
        tree2.create_node("Jill", "jill", parent="diane")
        self.assertIn("jill", tree2)
        self.assertIn("jill", tree2.is_branch("diane"))
        self.assertNotIn("jill", self.tree)
        self.assertNotIn("jill", self.tree.is_branch("diane"))

    def test_paste_duplicate_nodes(self):
        t1 = Tree()
        t1.create_node(identifier="A")
        t2 = Tree()
        t2.create_node(identifier="A")
        t2.create_node(identifier="B", parent="A")

        with self.assertRaises(ValueError) as e:
            t1.paste("A", t2)
        self.assertEqual(e.exception.args, ("Duplicated nodes ['A'] exists.",))

    def test_shallow_paste(self):
        t1 = Tree()
        n1 = t1.create_node(identifier="A")

        t2 = Tree()
        n2 = t2.create_node(identifier="B")

        t3 = Tree()
        n3 = t3.create_node(identifier="C")

        t1.paste(n1.identifier, t2)
        self.assertEqual(t1.to_dict(), {"A": {"id": "A", "children": [{"B": {"id": "B"}}]}})
        t1.paste(n1.identifier, t3)
        self.assertEqual(
            t1.to_dict(),
            {"A": {"id": "A", "children": [{"B": {"id": "B"}}, {"C": {"id": "C"}}]}},
        )

        self.assertEqual(t1.level(n1.identifier), 0)
        self.assertEqual(t1.level(n2.identifier), 1)
        self.assertEqual(t1.level(n3.identifier), 1)

    def test_root_removal(self):
        t = Tree()
        t.create_node(identifier="root-A")
        self.assertEqual(len(t.nodes.keys()), 1)
        self.assertEqual(t.root, "root-A")
        t.remove_node(identifier="root-A")
        self.assertEqual(len(t.nodes.keys()), 0)
        self.assertEqual(t.root, None)
        t.create_node(identifier="root-B")
        self.assertEqual(len(t.nodes.keys()), 1)
        self.assertEqual(t.root, "root-B")

    def test_from_map(self):
        tree = Tree.from_map(self.input_dict)
        self.assertTrue(tree.size() == 6)
        self.assertTrue(tree.root == [k for k, v in self.input_dict.items() if v is None][0])
        tree = Tree.from_map(self.input_dict, id_func=lambda x: x.upper())
        self.assertTrue(tree.size() == 6)

        def data_func(x):
            return x.upper()

        tree = Tree.from_map(self.input_dict, data_func=data_func)
        self.assertTrue(tree.size() == 6)
        self.assertTrue(
            tree.get_node(tree.root).data == data_func([k for k, v in self.input_dict.items() if v is None][0])
        )
        with self.assertRaises(ValueError):
            # invalid input payload without a root
            tree = Tree.from_map({"a": "b"})

        with self.assertRaises(ValueError):
            # invalid input payload without more than 1 root
            tree = Tree.from_map({"a": None, "b": None})

    def test_tree_initialization_comprehensive(self):
        """Test comprehensive tree initialization scenarios"""
        # Test empty tree
        empty_tree = Tree()
        self.assertIsNotNone(empty_tree.identifier)
        self.assertIsNone(empty_tree.root)
        self.assertEqual(len(empty_tree), 0)

        # Test tree with custom identifier
        custom_tree = Tree(identifier="custom_id")
        self.assertEqual(custom_tree.identifier, "custom_id")

        # Test tree with custom node class
        class CustomNode(Node):
            def __init__(self, tag=None, identifier=None, data=None):
                super().__init__(tag, identifier, data=data)
                self.custom_attr = "custom"

        custom_node_tree = Tree(node_class=CustomNode)
        node = custom_node_tree.create_node("test")
        self.assertIsInstance(node, CustomNode)
        self.assertEqual(node.custom_attr, "custom")

        # Test shallow copy
        shallow_copy = Tree(self.tree, deep=False)
        self.assertIsNot(shallow_copy, self.tree)
        self.assertEqual(shallow_copy.root, self.tree.root)
        self.assertIs(shallow_copy["hárry"], self.tree["hárry"])

        # Test deep copy
        deep_copy = Tree(self.tree, deep=True)
        self.assertIsNot(deep_copy, self.tree)
        self.assertEqual(deep_copy.root, self.tree.root)
        self.assertIsNot(deep_copy["hárry"], self.tree["hárry"])
        self.assertEqual(deep_copy["hárry"].tag, self.tree["hárry"].tag)

    def test_display_options_comprehensive(self):
        """Test comprehensive display options and formatting."""
        # Test different line types
        line_types = ["ascii", "ascii-ex", "ascii-exr", "ascii-em", "ascii-emv", "ascii-emh"]

        for line_type in line_types:
            output = self.tree.show(line_type=line_type, stdout=False)
            self.assertIn("Hárry", output)
            self.assertIsInstance(output, str)

        # Test with reversed sorting
        output_reversed = self.tree.show(reverse=True, stdout=False)
        self.assertIn("Hárry", output_reversed)

        # Test with custom key function
        output_key = self.tree.show(key=lambda x: len(x.tag), stdout=False)
        self.assertIn("Hárry", output_key)

        # Test without sorting
        output_no_sort = self.tree.show(sorting=False, stdout=False)
        self.assertIn("Hárry", output_no_sort)

        # Test starting from specific node
        output_subtree = self.tree.show(nid="jane", stdout=False)
        self.assertIn("Jane", output_subtree)
        self.assertNotIn("Bill", output_subtree)

    def test_tree_metrics_comprehensive(self):
        """Test comprehensive tree metrics and analysis."""
        # Test paths to leaves
        paths = self.tree.paths_to_leaves()
        self.assertEqual(len(paths), 2)  # Two leaf nodes

        # Verify each path starts with root
        for path in paths:
            self.assertEqual(path[0], "hárry")

        # Test size at different levels
        self.assertEqual(self.tree.size(level=0), 1)  # Root only
        self.assertEqual(self.tree.size(level=1), 2)  # Jane and Bill
        self.assertEqual(self.tree.size(level=2), 2)  # Diane and George

        # Test depth calculation
        self.assertEqual(self.tree.depth(), 2)

    def test_node_relationship_comprehensive(self):
        """Test comprehensive node relationship queries."""
        # Test siblings for all nodes
        harry_siblings = self.tree.siblings("hárry")
        self.assertEqual(len(harry_siblings), 0)  # Root has no siblings

        jane_siblings = self.tree.siblings("jane")
        self.assertEqual(len(jane_siblings), 1)
        self.assertEqual(jane_siblings[0].identifier, "bill")

        bill_siblings = self.tree.siblings("bill")
        self.assertEqual(len(bill_siblings), 1)
        self.assertEqual(bill_siblings[0].identifier, "jane")

        # Test ancestor relationships at different levels
        self.assertEqual(self.tree.ancestor("diane", level=0), self.tree["hárry"])
        self.assertEqual(self.tree.ancestor("diane", level=1), self.tree["jane"])
        self.assertEqual(self.tree.ancestor("diane"), "jane")  # Immediate parent

    def test_tree_modification_edge_cases(self):
        """Test edge cases in tree modification operations."""
        # Test moving node to itself (should change parent to itself)
        self.tree.move_node("jane", "jane")
        # Node should now be its own parent
        self.assertEqual(self.tree.parent("jane").identifier, "jane")

        # Test moving node to its descendant (should fail)
        with self.assertRaises(LoopError):
            self.tree.move_node("jane", "diane")

        # Test moving siblings (should work)
        single_tree = Tree()
        single_tree.create_node("Root", "root")
        single_tree.create_node("Child1", "child1", parent="root")
        single_tree.create_node("Child2", "child2", parent="root")

        # Move one child under another
        single_tree.move_node("child1", "child2")
        self.assertEqual(single_tree.parent("child1").identifier, "child2")

    def test_advanced_filtering_scenarios(self):
        """Test advanced filtering scenarios."""
        # Create tree with mixed data types
        data_tree = Tree()
        data_tree.create_node("Root", "root", data={"type": "root", "value": 0})
        data_tree.create_node("Branch1", "b1", parent="root", data={"type": "branch", "value": 1})
        data_tree.create_node("Branch2", "b2", parent="root", data={"type": "branch", "value": 2})
        data_tree.create_node("Leaf1", "l1", parent="b1", data={"type": "leaf", "value": 10})
        data_tree.create_node("Leaf2", "l2", parent="b2", data={"type": "leaf", "value": 20})

        # Filter by data type
        branches = list(data_tree.filter_nodes(lambda n: n.data and n.data.get("type") == "branch"))
        self.assertEqual(len(branches), 2)

        # Filter by data value
        high_value = list(data_tree.filter_nodes(lambda n: n.data and n.data.get("value", 0) > 5))
        self.assertEqual(len(high_value), 2)  # Leaf1 and Leaf2

        # Complex filter combining multiple conditions
        branch_with_high_value = list(
            data_tree.filter_nodes(lambda n: n.data and n.data.get("type") == "branch" and n.data.get("value", 0) > 1)
        )
        self.assertEqual(len(branch_with_high_value), 1)  # Only Branch2

    def test_tree_serialization_edge_cases(self):
        """Test edge cases in tree serialization."""
        # Test tree with None data
        none_tree = Tree()
        none_tree.create_node("Root", "root", data=None)
        none_tree.create_node("Child", "child", parent="root", data=None)

        # Should handle None data gracefully
        json_str = none_tree.to_json(with_data=True)
        self.assertIsInstance(json_str, str)

        dict_repr = none_tree.to_dict(with_data=True)
        self.assertIsInstance(dict_repr, dict)

        # Test tree with complex nested data
        complex_tree = Tree()
        complex_data = {
            "metadata": {
                "created": "2023-01-01",
                "tags": ["important", "test"],
                "properties": {"active": True, "score": 95.5},
            },
            "items": [1, 2, 3, {"nested": "value"}],
        }
        complex_tree.create_node("Complex", "complex", data=complex_data)

        # Should serialize complex data
        json_str = complex_tree.to_json(with_data=True)
        parsed = json.loads(json_str)
        self.assertIn("Complex", parsed)

    def test_unicode_and_encoding_comprehensive(self):
        """Test comprehensive Unicode and encoding scenarios."""
        # Test with various Unicode scripts
        unicode_tree = Tree()

        # Latin with diacritics
        unicode_tree.create_node("Café résumé", "cafe")

        # Cyrillic
        unicode_tree.create_node("Привет мир", "cyrillic", parent="cafe")

        # Chinese
        unicode_tree.create_node("你好世界", "chinese", parent="cyrillic")

        # Arabic
        unicode_tree.create_node("مرحبا بالعالم", "arabic", parent="chinese")

        # Emoji
        unicode_tree.create_node("Hello 🌍🚀✨", "emoji", parent="arabic")

        # Test that all operations work with Unicode
        self.assertEqual(len(unicode_tree), 5)
        self.assertTrue(unicode_tree.is_ancestor("cafe", "emoji"))

        # Test display with Unicode
        output = unicode_tree.show(stdout=False)
        self.assertIn("Café", output)
        self.assertIn("你好", output)

        # Test JSON serialization with Unicode
        json_str = unicode_tree.to_json()
        self.assertIsInstance(json_str, str)

    def test_memory_management_scenarios(self):
        """Test scenarios that could cause memory issues."""
        # Test with large amounts of data
        large_data_tree = Tree()
        large_data = {"data": "x" * 10000}  # 10KB of data per node

        large_data_tree.create_node("Root", "root", data=large_data)
        for i in range(10):
            large_data_tree.create_node(f"Child{i}", f"child{i}", parent="root", data=large_data)

        # Should handle large data without issues
        self.assertEqual(len(large_data_tree), 11)

        # Test subtree operations with large data
        subtree = large_data_tree.subtree("child0")
        self.assertEqual(len(subtree), 1)

        # Test removal
        removed = large_data_tree.remove_subtree("child1")
        self.assertEqual(len(removed), 1)

    def test_error_handling_comprehensive(self):
        """Test comprehensive error handling scenarios."""
        # Test operations on nodes that don't exist
        error_tree = Tree()
        error_tree.create_node("Root", "root")

        operations_that_should_fail = [
            (lambda: error_tree.parent("nonexistent"), NodeIDAbsentError),
            (lambda: error_tree.children("nonexistent"), NodeIDAbsentError),
            (lambda: error_tree.siblings("nonexistent"), NodeIDAbsentError),
            (lambda: error_tree.level("nonexistent"), NodeIDAbsentError),
            (lambda: error_tree.remove_node("nonexistent"), NodeIDAbsentError),
            (lambda: error_tree.move_node("nonexistent", "root"), NodeIDAbsentError),
            (lambda: error_tree.move_node("root", "nonexistent"), NodeIDAbsentError),
        ]

        for operation, expected_error in operations_that_should_fail:
            with self.assertRaises(expected_error):
                operation()

        # Test invalid parameter types
        with self.assertRaises(TypeError):
            error_tree.size(level="invalid")

        # Test adding invalid node types
        with self.assertRaises(OSError):
            error_tree.add_node("not_a_node")

    def test_special_methods_comprehensive(self):
        """Test __contains__, __len__, __str__, __getitem__ methods"""
        # Test __contains__
        self.assertTrue("hárry" in self.tree)
        self.assertFalse("nonexistent" in self.tree)

        # Test __len__
        self.assertEqual(len(self.tree), 5)

        # Test __str__ (string representation)
        str_repr = str(self.tree)
        self.assertIn("Hárry", str_repr)
        self.assertIn("Jane", str_repr)

        # Test __getitem__ success
        node = self.tree["hárry"]
        self.assertEqual(node.tag, "Hárry")

        # Test __getitem__ failure
        with self.assertRaises(NodeIDAbsentError):
            _ = self.tree["nonexistent"]

    def test_add_node_comprehensive(self):
        """Test add_node method with various scenarios"""
        tree = Tree()

        # Test adding root node
        root_node = Node("Root", "root")
        tree.add_node(root_node)
        self.assertEqual(tree.root, "root")
        self.assertIn("root", tree)

        # Test adding child node
        child_node = Node("Child", "child")
        tree.add_node(child_node, parent="root")
        self.assertEqual(tree.parent("child").identifier, "root")

        # Test adding node with Node object as parent
        grandchild_node = Node("Grandchild", "grandchild")
        tree.add_node(grandchild_node, parent=child_node)
        self.assertEqual(tree.parent("grandchild").identifier, "child")

        # Test duplicate node ID error
        with self.assertRaises(DuplicatedNodeIdError):
            duplicate_node = Node("Duplicate", "root")
            tree.add_node(duplicate_node)

        # Test multiple root error
        with self.assertRaises(MultipleRootError):
            another_root = Node("Another Root", "root2")
            tree.add_node(another_root)

        # Test parent not found error
        with self.assertRaises(NodeIDAbsentError):
            orphan_node = Node("Orphan", "orphan")
            tree.add_node(orphan_node, parent="nonexistent")

        # Test wrong node type error
        with self.assertRaises(OSError):
            tree.add_node("not_a_node")

    def test_create_node_comprehensive(self):
        """Test create_node method with various parameters"""
        tree = Tree()

        # Test creating root with all parameters
        root = tree.create_node(tag="Root", identifier="root", data={"key": "value"})
        self.assertEqual(root.tag, "Root")
        self.assertEqual(root.identifier, "root")
        self.assertEqual(root.data, {"key": "value"})

        # Test creating child with auto-generated ID
        child = tree.create_node(tag="Child", parent="root")
        self.assertIsNotNone(child.identifier)
        self.assertEqual(child.tag, "Child")
        self.assertEqual(tree.parent(child.identifier).identifier, "root")

        # Test creating node with minimal parameters on a new tree
        minimal_tree = Tree()
        minimal = minimal_tree.create_node()
        self.assertIsNotNone(minimal.identifier)
        self.assertIsNotNone(minimal.tag)

    def test_expand_tree_comprehensive(self):
        """Test expand_tree with all modes and parameters"""
        # Test DEPTH mode (default)
        depth_traversal = list(self.tree.expand_tree(mode=Tree.DEPTH))
        self.assertEqual(depth_traversal[0], "hárry")  # Root first

        # Test WIDTH mode
        width_traversal = list(self.tree.expand_tree(mode=Tree.WIDTH))
        self.assertEqual(width_traversal[0], "hárry")  # Root first

        # Test ZIGZAG mode
        zigzag_traversal = list(self.tree.expand_tree(mode=Tree.ZIGZAG))
        self.assertEqual(zigzag_traversal[0], "hárry")  # Root first

        # Test with filter
        filtered = list(self.tree.expand_tree(filter=lambda node: not node.is_leaf(self.tree.identifier)))
        # Should find parent nodes with children
        self.assertGreater(len(filtered), 0)

        # Test with key sorting
        sorted_traversal = list(self.tree.expand_tree(key=lambda node: node.tag, reverse=True))
        self.assertIn("hárry", sorted_traversal)

        # Test with specific starting node
        subtree_traversal = list(self.tree.expand_tree(nid="jane"))
        self.assertEqual(subtree_traversal[0], "jane")

        # Test without sorting
        unsorted = list(self.tree.expand_tree(sorting=False))
        self.assertEqual(unsorted[0], "hárry")

        # Test with nonexistent node
        with self.assertRaises(NodeIDAbsentError):
            list(self.tree.expand_tree(nid="nonexistent"))

        # Test invalid mode
        with self.assertRaises(ValueError):
            list(self.tree.expand_tree(mode=999))

    def test_tree_queries_comprehensive(self):
        """Test various tree query methods"""
        # Test contains
        self.assertTrue(self.tree.contains("hárry"))
        self.assertFalse(self.tree.contains("nonexistent"))

        # Test get_node
        node = self.tree.get_node("hárry")
        self.assertIsNotNone(node)
        self.assertEqual(node.tag, "Hárry")

        # Test get_node with None/nonexistent
        self.assertIsNone(self.tree.get_node(None))
        self.assertIsNone(self.tree.get_node("nonexistent"))

        # Test all_nodes vs all_nodes_itr
        all_nodes_list = self.tree.all_nodes()
        all_nodes_iter = list(self.tree.all_nodes_itr())
        self.assertEqual(len(all_nodes_list), len(all_nodes_iter))

        # Test size with level
        total_size = self.tree.size()
        self.assertEqual(total_size, 5)

        level_0_size = self.tree.size(level=0)
        self.assertEqual(level_0_size, 1)  # Only root

        # Test size with invalid level type
        with self.assertRaises(TypeError):
            self.tree.size(level="invalid")

    def test_tree_relationships_comprehensive(self):
        """Test relationship methods"""
        # Test is_ancestor
        self.assertTrue(self.tree.is_ancestor("hárry", "diane"))
        self.assertTrue(self.tree.is_ancestor("jane", "diane"))
        self.assertFalse(self.tree.is_ancestor("bill", "diane"))
        self.assertFalse(self.tree.is_ancestor("diane", "hárry"))

        # Test siblings
        siblings = self.tree.siblings("jane")
        sibling_ids = [s.identifier for s in siblings]
        self.assertIn("bill", sibling_ids)
        self.assertNotIn("jane", sibling_ids)

        # Test root siblings (should be empty)
        root_siblings = self.tree.siblings("hárry")
        self.assertEqual(len(root_siblings), 0)

        # Test is_branch with None (should raise error)
        with self.assertRaises(OSError):
            self.tree.is_branch(None)

    def test_tree_modification_comprehensive(self):
        """Test tree modification methods"""
        # Create test tree
        tree = Tree()
        tree.create_node("A", "a")
        tree.create_node("B", "b", parent="a")
        tree.create_node("C", "c", parent="a")
        tree.create_node("D", "d", parent="b")

        # Test link_past_node
        tree.link_past_node("b")
        self.assertNotIn("b", tree)
        self.assertEqual(tree.parent("d").identifier, "a")

        # Test link_past_node with root (should fail)
        with self.assertRaises(LinkPastRootNodeError):
            tree.link_past_node("a")

        # Test link_past_node with nonexistent node
        with self.assertRaises(NodeIDAbsentError):
            tree.link_past_node("nonexistent")

    def test_update_node_comprehensive(self):
        """Test update_node method"""
        tree = Tree()
        tree.create_node("Original", "orig", data="original_data")
        tree.create_node("Child", "child", parent="orig")

        # Test updating tag
        tree.update_node("orig", tag="Updated")
        self.assertEqual(tree["orig"].tag, "Updated")

        # Test updating data
        tree.update_node("orig", data="updated_data")
        self.assertEqual(tree["orig"].data, "updated_data")

        # Test updating identifier
        tree.update_node("orig", identifier="new_id")
        self.assertNotIn("orig", tree)
        self.assertIn("new_id", tree)
        self.assertEqual(tree.root, "new_id")
        self.assertEqual(tree.parent("child").identifier, "new_id")

    def test_output_methods_comprehensive(self):
        """Test various output methods"""
        # Test to_dict
        tree_dict = self.tree.to_dict()
        self.assertIn("Hárry", tree_dict)

        # Test to_dict with data
        tree_dict_with_data = self.tree.to_dict(with_data=True)
        self.assertIn("Hárry", tree_dict_with_data)

        # Test to_json
        json_str = self.tree.to_json()
        self.assertIsInstance(json_str, str)
        # Handle Unicode encoding in JSON - the 'á' character is encoded as
        # \\u00e1
        self.assertTrue("H\\u00e1rry" in json_str or "Hárry" in json_str)

        # Test show with different parameters
        output = self.tree.show(stdout=False)
        self.assertIn("Hárry", output)

        # Test show with different line types
        for line_type in [
            "ascii",
            "ascii-ex",
            "ascii-exr",
            "ascii-em",
            "ascii-emv",
            "ascii-emh",
        ]:
            output = self.tree.show(line_type=line_type, stdout=False)
            self.assertIn("Hárry", output)

    def test_error_handling_comprehensive(self):
        """Test comprehensive error handling"""
        empty_tree = Tree()

        # Test operations on empty tree
        with self.assertRaises(NodeIDAbsentError):
            empty_tree.parent("nonexistent")

        with self.assertRaises(NodeIDAbsentError):
            empty_tree.children("nonexistent")

        with self.assertRaises(NodeIDAbsentError):
            empty_tree.remove_node("nonexistent")

        # Test show on empty tree (should print message)
        import io
        import sys

        captured_output = io.StringIO()
        sys.stdout = captured_output
        empty_tree.show()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Tree is empty", output)

    def test_edge_cases_comprehensive(self):
        """Test edge cases and boundary conditions"""
        # Test single node tree
        single_tree = Tree()
        single_tree.create_node("Single", "single")

        self.assertEqual(len(single_tree), 1)
        self.assertEqual(single_tree.depth(), 0)
        self.assertEqual(len(single_tree.leaves()), 1)
        self.assertEqual(len(single_tree.paths_to_leaves()), 1)

        # Test operations on single node
        self.assertIsNone(single_tree.parent("single"))
        self.assertEqual(len(single_tree.children("single")), 0)
        self.assertEqual(len(single_tree.siblings("single")), 0)

        # Test removing single node
        single_tree.remove_node("single")
        self.assertIsNone(single_tree.root)
        self.assertEqual(len(single_tree), 0)

    def test_merge_comprehensive(self):
        """Test merge method with various scenarios"""
        # Test merging on empty tree
        empty_tree = Tree()
        merge_tree = self.get_t1()
        empty_tree.merge(None, merge_tree)
        self.assertEqual(empty_tree.root, "r")

        # Test merging with specified node
        tree1 = self.get_t1()
        tree2 = self.get_t2()
        original_size = len(tree1)
        tree1.merge("a", tree2)

        # Verify merge
        self.assertGreater(len(tree1), original_size)
        self.assertIn("c", tree1)  # From tree2
        self.assertIn("d", tree1)  # From tree2

        # Test merge with None nid on non-empty tree
        tree3 = self.get_t1()
        tree4 = self.get_t2()
        with self.assertRaises(ValueError):
            tree3.merge(None, tree4)

        # Test merge with empty source tree
        tree5 = Tree()
        tree6 = self.get_t1()
        original_len = len(tree6)
        tree6.merge("a", tree5)
        self.assertEqual(len(tree6), original_len)  # Should be unchanged

    def test_paste_comprehensive(self):
        """Test paste method thoroughly"""
        tree1 = Tree()
        tree1.create_node("Root", "root")

        tree2 = Tree()
        tree2.create_node("Subtree", "subtree")
        tree2.create_node("Child", "child", parent="subtree")

        # Test normal paste
        tree1.paste("root", tree2)
        self.assertIn("subtree", tree1)
        self.assertIn("child", tree1)
        self.assertEqual(tree1.parent("subtree").identifier, "root")

        # Test paste with None nid
        tree3 = Tree()
        tree3.create_node("Root", "root")
        tree4 = Tree()
        tree4.create_node("Sub", "sub")

        with self.assertRaises(ValueError):
            tree3.paste(None, tree4)

        # Test paste to nonexistent node
        with self.assertRaises(NodeIDAbsentError):
            tree3.paste("nonexistent", tree4)

        # Test paste empty tree
        empty_tree = Tree()
        tree5 = Tree()
        tree5.create_node("Root", "root")
        tree5.paste("root", empty_tree)  # Should do nothing
        self.assertEqual(len(tree5), 1)

    def test_subtree_and_remove_subtree_comprehensive(self):
        """Test subtree and remove_subtree methods"""
        # Test subtree creation
        jane_subtree = self.tree.subtree("jane")
        self.assertEqual(jane_subtree.root, "jane")
        self.assertIn("diane", jane_subtree)
        self.assertNotIn("bill", jane_subtree)

        # Test subtree with None (empty tree)
        empty_subtree = self.tree.subtree(None)
        self.assertEqual(len(empty_subtree), 0)
        self.assertIsNone(empty_subtree.root)

        # Test subtree with nonexistent node
        with self.assertRaises(NodeIDAbsentError):
            self.tree.subtree("nonexistent")

        # Test remove_subtree
        original_size = len(self.tree)
        removed_subtree = self.tree.remove_subtree("jane")

        self.assertLess(len(self.tree), original_size)
        self.assertNotIn("jane", self.tree)
        self.assertNotIn("diane", self.tree)
        self.assertEqual(removed_subtree.root, "jane")
        self.assertIn("diane", removed_subtree)

        # Test remove_subtree with None
        tree = Tree()
        empty_removed = tree.remove_subtree(None)
        self.assertEqual(len(empty_removed), 0)

    def test_save2file_and_to_graphviz(self):
        """Test file output methods"""
        import os
        import tempfile

        # Test save2file
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            self.tree.save2file(tmp_path)
            self.assertTrue(os.path.exists(tmp_path))

            # Verify file content
            with open(tmp_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn("Hárry", content)
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        # Test to_graphviz with file output
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".dot") as tmp:
            dot_path = tmp.name

        try:
            self.tree.to_graphviz(filename=dot_path)
            self.assertTrue(os.path.exists(dot_path))

            # Verify dot file content
            with open(dot_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn("digraph", content)
                self.assertIn("Hárry", content)
        finally:
            if os.path.exists(dot_path):
                os.unlink(dot_path)

        # Test to_graphviz with different parameters
        import io
        import sys

        # Capture stdout for graphviz without filename
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.tree.to_graphviz(shape="box", graph="graph")
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertIn("graph tree", output)
        self.assertIn("box", output)

    def test_tree_constants(self):
        """Test tree traversal constants"""
        self.assertEqual(Tree.ROOT, 0)
        self.assertEqual(Tree.DEPTH, 1)
        self.assertEqual(Tree.WIDTH, 2)
        self.assertEqual(Tree.ZIGZAG, 3)

    def test_performance_edge_cases(self):
        """Test performance and edge cases with larger trees"""
        # Create a deeper tree
        deep_tree = Tree()
        current_id = "root"
        deep_tree.create_node("Root", current_id)

        # Create a chain of 100 nodes
        for i in range(100):
            new_id = f"node_{i}"
            deep_tree.create_node(f"Node {i}", new_id, parent=current_id)
            current_id = new_id

        # Test operations on deep tree
        self.assertEqual(deep_tree.depth(), 100)
        self.assertEqual(len(deep_tree.leaves()), 1)

        # Test traversal
        all_nodes = list(deep_tree.expand_tree())
        self.assertEqual(len(all_nodes), 101)  # root + 100 nodes

        # Create a wide tree
        wide_tree = Tree()
        wide_tree.create_node("Root", "root")

        # Create 100 children of root
        for i in range(100):
            wide_tree.create_node(f"Child {i}", f"child_{i}", parent="root")

        # Test operations on wide tree
        self.assertEqual(wide_tree.depth(), 1)
        self.assertEqual(len(wide_tree.leaves()), 100)
        self.assertEqual(len(wide_tree.children("root")), 100)

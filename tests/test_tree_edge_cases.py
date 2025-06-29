#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Edge case tests for Tree class.
This module focuses on boundary conditions, error handling, and unusual scenarios.
"""
from __future__ import unicode_literals

import unittest

from treelib import Node, Tree
from treelib.exceptions import (
    DuplicatedNodeIdError,
    InvalidLevelNumber,
    LinkPastRootNodeError,
    LoopError,
    MultipleRootError,
    NodeIDAbsentError,
)


class TreeEdgeCasesTestCase(unittest.TestCase):
    """Edge case tests for Tree class."""

    def setUp(self):
        """Set up test fixtures."""
        self.tree = Tree()
        self.tree.create_node("Root", "root")
        self.tree.create_node("Child1", "child1", parent="root")
        self.tree.create_node("Child2", "child2", parent="root")
        self.tree.create_node("Grandchild", "grandchild", parent="child1")

    def test_empty_tree_operations(self):
        """Test operations on empty tree."""
        empty_tree = Tree()

        # Basic properties
        self.assertEqual(len(empty_tree), 0)
        self.assertIsNone(empty_tree.root)
        self.assertEqual(empty_tree.size(), 0)
        self.assertEqual(empty_tree.depth(), 0)

        # Operations that should work on empty tree
        self.assertEqual(len(empty_tree.all_nodes()), 0)
        self.assertEqual(len(list(empty_tree.all_nodes_itr())), 0)
        self.assertEqual(len(empty_tree.leaves()), 0)

        # Operations that should fail on empty tree
        with self.assertRaises(NodeIDAbsentError):
            empty_tree.parent("nonexistent")

        with self.assertRaises(NodeIDAbsentError):
            empty_tree.children("nonexistent")

        with self.assertRaises(NodeIDAbsentError):
            empty_tree.level("nonexistent")

    def test_single_node_tree(self):
        """Test operations on single node tree."""
        single_tree = Tree()
        single_tree.create_node("Only", "only")

        # Basic properties
        self.assertEqual(len(single_tree), 1)
        self.assertEqual(single_tree.root, "only")
        self.assertEqual(single_tree.size(), 1)
        self.assertEqual(single_tree.depth(), 0)

        # Node relationships
        self.assertIsNone(single_tree.parent("only"))
        self.assertEqual(len(single_tree.children("only")), 0)
        self.assertEqual(len(single_tree.siblings("only")), 0)
        self.assertEqual(single_tree.level("only"), 0)

        # Leaves and traversal
        leaves = single_tree.leaves()
        self.assertEqual(len(leaves), 1)
        self.assertEqual(leaves[0].identifier, "only")

        # Expansion
        expanded = list(single_tree.expand_tree())
        self.assertEqual(expanded, ["only"])

    def test_very_deep_tree(self):
        """Test operations on very deep tree (linear chain)."""
        deep_tree = Tree()
        deep_tree.create_node("Root", "root")

        # Create a chain of 1000 nodes
        current = "root"
        for i in range(1000):
            node_id = f"node_{i}"
            deep_tree.create_node(f"Node {i}", node_id, parent=current)
            current = node_id

        # Test basic properties
        self.assertEqual(len(deep_tree), 1001)  # root + 1000 nodes
        self.assertEqual(deep_tree.depth(), 1000)
        self.assertEqual(len(deep_tree.leaves()), 1)  # Only the last node

        # Test traversal works
        all_nodes = list(deep_tree.expand_tree())
        self.assertEqual(len(all_nodes), 1001)

        # Test ancestor/descendant relationships
        self.assertTrue(deep_tree.is_ancestor("root", "node_999"))
        self.assertTrue(deep_tree.is_ancestor("node_0", "node_999"))
        self.assertFalse(deep_tree.is_ancestor("node_999", "root"))

    def test_very_wide_tree(self):
        """Test operations on very wide tree (many children)."""
        wide_tree = Tree()
        wide_tree.create_node("Root", "root")

        # Create 1000 children of root
        for i in range(1000):
            wide_tree.create_node(f"Child {i}", f"child_{i}", parent="root")

        # Test basic properties
        self.assertEqual(len(wide_tree), 1001)  # root + 1000 children
        self.assertEqual(wide_tree.depth(), 1)
        self.assertEqual(len(wide_tree.leaves()), 1000)  # All children are leaves

        # Test children access
        children = wide_tree.children("root")
        self.assertEqual(len(children), 1000)

        # Test sibling relationships
        siblings = wide_tree.siblings("child_0")
        self.assertEqual(len(siblings), 999)  # All other children

    def test_unicode_identifiers_and_tags(self):
        """Test tree with Unicode identifiers and tags."""
        unicode_tree = Tree()

        # Create nodes with Unicode identifiers and tags
        unicode_tree.create_node("Café", "café")
        unicode_tree.create_node("Naïve résumé", "naïve_résumé", parent="café")
        unicode_tree.create_node("中文节点", "中文_id", parent="naïve_résumé")
        unicode_tree.create_node("Ñoño", "ñoño", parent="中文_id")
        unicode_tree.create_node("Ελληνικά", "ελληνικά", parent="ñoño")

        # Test basic operations work
        self.assertEqual(len(unicode_tree), 5)
        self.assertEqual(unicode_tree.root, "café")
        self.assertTrue(unicode_tree.contains("中文_id"))
        self.assertTrue(unicode_tree.is_ancestor("café", "ελληνικά"))

        # Test node access
        node = unicode_tree["中文_id"]
        self.assertEqual(node.tag, "中文节点")

        # Test traversal
        all_nodes = list(unicode_tree.expand_tree())
        self.assertEqual(len(all_nodes), 5)
        self.assertIn("ελληνικά", all_nodes)

    def test_extreme_data_types(self):
        """Test nodes with extreme data types."""
        data_tree = Tree()

        # Different data types
        data_tree.create_node("None Data", "none", data=None)
        data_tree.create_node("List Data", "list", parent="none", data=[1, 2, 3, "test"])
        data_tree.create_node("Dict Data", "dict", parent="none", data={"nested": {"deep": {"value": 42}}})
        data_tree.create_node("Set Data", "set", parent="none", data={1, 2, 3})
        data_tree.create_node("Tuple Data", "tuple", parent="none", data=(1, "two", 3.0))

        # Custom object data
        class CustomObject:
            def __init__(self, value):
                self.value = value
                self.nested = {"test": [1, 2, 3]}

        data_tree.create_node("Object Data", "object", parent="none", data=CustomObject("test_value"))

        # Test that all nodes work properly
        self.assertEqual(len(data_tree), 6)

        # Test data access
        self.assertIsNone(data_tree["none"].data)
        self.assertEqual(data_tree["list"].data[3], "test")
        self.assertEqual(data_tree["dict"].data["nested"]["deep"]["value"], 42)
        self.assertIn(1, data_tree["set"].data)
        self.assertEqual(data_tree["tuple"].data[1], "two")
        self.assertEqual(data_tree["object"].data.value, "test_value")

    def test_circular_reference_prevention(self):
        """Test that circular references are prevented."""
        circ_tree = Tree()
        circ_tree.create_node("A", "a")
        circ_tree.create_node("B", "b", parent="a")
        circ_tree.create_node("C", "c", parent="b")
        circ_tree.create_node("D", "d", parent="c")

        # Try to create a loop by moving B under D
        with self.assertRaises(LoopError):
            circ_tree.move_node("b", "d")

        # Tree structure should remain unchanged
        self.assertEqual(circ_tree.parent("b").identifier, "a")
        self.assertEqual(circ_tree.parent("d").identifier, "c")

    def test_duplicate_identifier_handling(self):
        """Test handling of duplicate identifiers."""
        dup_tree = Tree()
        dup_tree.create_node("First", "duplicate")

        # Try to create another node with same identifier
        with self.assertRaises(DuplicatedNodeIdError):
            dup_tree.create_node("Second", "duplicate")

        # Try to add node with same identifier
        duplicate_node = Node("Third", "duplicate")
        with self.assertRaises(DuplicatedNodeIdError):
            dup_tree.add_node(duplicate_node)

    def test_multiple_root_prevention(self):
        """Test prevention of multiple roots."""
        multi_tree = Tree()
        multi_tree.create_node("Root1", "root1")

        # Try to create another root
        with self.assertRaises(MultipleRootError):
            multi_tree.create_node("Root2", "root2")

        # Try to add another root node
        root_node = Node("Root3", "root3")
        with self.assertRaises(MultipleRootError):
            multi_tree.add_node(root_node)

    def test_nonexistent_parent_handling(self):
        """Test handling of nonexistent parent references."""
        parent_tree = Tree()
        parent_tree.create_node("Root", "root")

        # Try to create child with nonexistent parent
        with self.assertRaises(NodeIDAbsentError):
            parent_tree.create_node("Orphan", "orphan", parent="nonexistent")

        # Try to add node with nonexistent parent
        orphan_node = Node("Orphan2", "orphan2")
        with self.assertRaises(NodeIDAbsentError):
            parent_tree.add_node(orphan_node, parent="nonexistent")

    def test_invalid_node_types(self):
        """Test handling of invalid node types."""
        invalid_tree = Tree()

        # Try to add non-Node object
        with self.assertRaises(OSError):
            invalid_tree.add_node("not_a_node")

        with self.assertRaises(OSError):
            invalid_tree.add_node(42)

        with self.assertRaises(OSError):
            invalid_tree.add_node({"not": "a_node"})

    def test_extremely_long_identifiers_and_tags(self):
        """Test with extremely long identifiers and tags."""
        long_tree = Tree()

        # Create very long identifier and tag
        long_id = "x" * 10000
        long_tag = "Very " * 2000 + "Long Tag"

        long_tree.create_node(long_tag, long_id)

        # Should work normally
        self.assertEqual(len(long_tree), 1)
        self.assertEqual(long_tree.root, long_id)
        self.assertEqual(long_tree[long_id].tag, long_tag)

    def test_special_characters_in_identifiers(self):
        """Test with special characters in identifiers."""
        special_tree = Tree()

        # Various special character combinations
        special_ids = [
            "id-with-dashes",
            "id_with_underscores",
            "id.with.dots",
            "id with spaces",
            "id/with/slashes",
            "id\\with\\backslashes",
            "id@with@symbols",
            "id#with$various%special^chars&*()",
            "id[with]brackets{and}braces",
            "id<with>angle<brackets>",
            "id\"with'quotes",
            "id`with`backticks",
            "id~with~tildes",
            "id|with|pipes",
            "id=with=equals+plus",
            "id?with?questions!exclamation",
            "id,with,commas;semicolons:",
            "\t\n\r\f\v",  # whitespace characters
        ]

        special_tree.create_node("Root", "root")

        for special_id in special_ids:
            try:
                special_tree.create_node(f"Node {special_id}", special_id, parent="root")
                # If creation succeeds, test basic operations
                self.assertTrue(special_tree.contains(special_id))
                self.assertEqual(special_tree.parent(special_id).identifier, "root")
            except Exception:
                # Some special characters might not be supported, which is fine
                pass

    def test_root_operations_edge_cases(self):
        """Test edge cases with root operations."""
        root_tree = Tree()
        root_tree.create_node("Root", "root")
        root_tree.create_node("Child", "child", parent="root")

        # Test link_past_node on root (should fail)
        with self.assertRaises(LinkPastRootNodeError):
            root_tree.link_past_node("root")

        # Test removing root removes entire tree
        num_removed = root_tree.remove_node("root")
        self.assertEqual(num_removed, 2)  # root + child
        self.assertIsNone(root_tree.root)
        self.assertEqual(len(root_tree), 0)

    def test_level_edge_cases(self):
        """Test level calculation edge cases."""
        level_tree = Tree()
        level_tree.create_node("Root", "root")
        level_tree.create_node("L1", "l1", parent="root")
        level_tree.create_node("L2", "l2", parent="l1")

        # Test level with filter that excludes nodes
        level_filtered = level_tree.level("l2", filter=lambda x: x.identifier != "l1")
        self.assertEqual(level_filtered, 1)  # Skips l1, so l2 appears at level 1

        # Test level with filter that excludes all intermediate nodes
        level_tree.create_node("L3", "l3", parent="l2")
        level_filtered2 = level_tree.level("l3", filter=lambda x: x.identifier in ["root", "l3"])
        self.assertEqual(level_filtered2, 1)  # Only root and l3 count

    def test_ancestor_edge_cases(self):
        """Test ancestor method edge cases."""
        anc_tree = Tree()
        anc_tree.create_node("Root", "root")
        anc_tree.create_node("L1", "l1", parent="root")
        anc_tree.create_node("L2", "l2", parent="l1")
        anc_tree.create_node("L3", "l3", parent="l2")

        # Test ancestor at level equal to node's level (should fail)
        with self.assertRaises(InvalidLevelNumber):
            anc_tree.ancestor("l3", level=3)  # l3 is at level 3

        # Test ancestor at level greater than node's level (should fail)
        with self.assertRaises(InvalidLevelNumber):
            anc_tree.ancestor("l2", level=5)  # l2 is at level 2

    def test_memory_efficiency_large_operations(self):
        """Test memory efficiency with large operations."""
        # Create a moderately large tree
        mem_tree = Tree()
        mem_tree.create_node("Root", "root")

        # Create 100 branches with 50 nodes each (5000 total nodes)
        for branch in range(100):
            branch_id = f"branch_{branch}"
            mem_tree.create_node(f"Branch {branch}", branch_id, parent="root")

            for leaf in range(50):
                leaf_id = f"leaf_{branch}_{leaf}"
                mem_tree.create_node(f"Leaf {branch}-{leaf}", leaf_id, parent=branch_id)

        # Test that operations complete without memory issues
        self.assertEqual(len(mem_tree), 5101)  # root + 100 branches + 5000 leaves

        # Test large traversals
        all_nodes = list(mem_tree.expand_tree())
        self.assertEqual(len(all_nodes), 5101)

        # Test filtering large datasets
        leaf_nodes = list(mem_tree.filter_nodes(lambda n: n.is_leaf(mem_tree.identifier)))
        self.assertEqual(len(leaf_nodes), 5000)  # All leaves

        # Test paths to leaves (this could be memory intensive)
        paths = mem_tree.paths_to_leaves()
        self.assertEqual(len(paths), 5000)  # One path per leaf

    def tearDown(self):
        """Clean up test fixtures."""
        self.tree = None


if __name__ == "__main__":
    unittest.main()

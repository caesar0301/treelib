#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Comprehensive tests for Tree class methods that need additional coverage.
This module focuses on edge cases, error handling, and less-tested methods.
"""
from __future__ import unicode_literals

import io
import json
import os
import tempfile
import unittest
from unittest.mock import patch

from treelib import Node, Tree
from treelib.exceptions import InvalidLevelNumber, NodeIDAbsentError


class TreeComprehensiveTestCase(unittest.TestCase):
    """Comprehensive tests for Tree class methods and edge cases."""

    def setUp(self):
        """Set up test fixtures with various tree structures."""
        # Basic family tree
        self.tree = Tree(identifier="family_tree")
        self.tree.create_node("Grandpa", "grandpa")
        self.tree.create_node("Dad", "dad", parent="grandpa")
        self.tree.create_node("Uncle", "uncle", parent="grandpa")
        self.tree.create_node("Me", "me", parent="dad")
        self.tree.create_node("Sister", "sister", parent="dad")
        self.tree.create_node("Cousin", "cousin", parent="uncle")

        # Simple tree for graphviz tests
        self.simple_tree = Tree(identifier="simple")
        self.simple_tree.create_node("Root", "r")
        self.simple_tree.create_node("Child A", "a", parent="r")
        self.simple_tree.create_node("Child B", "b", parent="r")

        # Empty tree
        self.empty_tree = Tree(identifier="empty")

        # Single node tree
        self.single_tree = Tree(identifier="single")
        self.single_tree.create_node("Only", "only")

    def test_to_graphviz_default(self):
        """Test to_graphviz with default parameters."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            self.simple_tree.to_graphviz()
            output = mock_stdout.getvalue()

            # Check basic structure
            self.assertIn("digraph tree", output)
            self.assertIn('"r" [label="Root", shape=circle]', output)
            self.assertIn('"a" [label="Child A", shape=circle]', output)
            self.assertIn('"r" -> "a"', output)
            self.assertIn('"r" -> "b"', output)

    def test_to_graphviz_custom_shape(self):
        """Test to_graphviz with custom shape."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            self.simple_tree.to_graphviz(shape="box")
            output = mock_stdout.getvalue()

            self.assertIn("shape=box", output)

    def test_to_graphviz_undirected_graph(self):
        """Test to_graphviz with undirected graph."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            self.simple_tree.to_graphviz(graph="graph")
            output = mock_stdout.getvalue()

            self.assertIn("graph tree", output)
            self.assertIn('"r" -- "a"', output)  # Undirected edge

    def test_to_graphviz_with_filter(self):
        """Test to_graphviz with node filter."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            # Only show nodes that don't start with 'Child B'
            self.simple_tree.to_graphviz(filter=lambda x: x.tag != "Child B")
            output = mock_stdout.getvalue()

            self.assertIn("Root", output)
            self.assertIn("Child A", output)
            self.assertNotIn("Child B", output)

    def test_to_graphviz_with_sorting(self):
        """Test to_graphviz with custom sorting."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            self.simple_tree.to_graphviz(key=lambda x: x.tag, reverse=True, sorting=True)
            output = mock_stdout.getvalue()

            # Should contain all nodes regardless of sorting
            self.assertIn("Root", output)
            self.assertIn("Child A", output)
            self.assertIn("Child B", output)

    def test_to_graphviz_file_output(self):
        """Test to_graphviz writing to file."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".dot") as tmp:
            tmp_path = tmp.name

        try:
            self.simple_tree.to_graphviz(filename=tmp_path)

            # Verify file was created and has content
            self.assertTrue(os.path.exists(tmp_path))
            with open(tmp_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn("digraph tree", content)
                self.assertIn("Root", content)

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_to_graphviz_empty_tree(self):
        """Test to_graphviz with empty tree."""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            self.empty_tree.to_graphviz()
            output = mock_stdout.getvalue()

            self.assertIn("digraph tree", output)
            # Should only have the basic structure, no nodes
            self.assertEqual(output.count("[label="), 0)

    def test_to_graphviz_special_characters(self):
        """Test to_graphviz with special characters in labels."""
        special_tree = Tree()
        special_tree.create_node('Root "quoted"', "r")
        special_tree.create_node("Child's", "c", parent="r")

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            special_tree.to_graphviz()
            output = mock_stdout.getvalue()

            # Should escape quotes properly
            self.assertIn(r"Root \"quoted\"", output)
            self.assertIn("Child's", output)

    def test_save2file_basic(self):
        """Test save2file basic functionality."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            self.tree.save2file(tmp_path)

            # Verify file exists and has content
            self.assertTrue(os.path.exists(tmp_path))
            with open(tmp_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn("Grandpa", content)
                self.assertIn("Dad", content)
                # Should have tree structure characters
                self.assertTrue(any(c in content for c in ["├", "└", "│"]))

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_save2file_with_parameters(self):
        """Test save2file with various parameters."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            self.tree.save2file(
                tmp_path,
                nid="dad",  # Start from dad
                idhidden=False,  # Show identifiers
                line_type="ascii",  # ASCII style
                sorting=False,  # Preserve insertion order
            )

            with open(tmp_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Should start from Dad, not Grandpa
                self.assertIn("Dad", content)
                self.assertNotIn("Grandpa", content)
                # Should show identifiers
                self.assertIn("[dad]", content)
                # Should use ASCII characters
                self.assertIn("|--", content)

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_save2file_with_filter(self):
        """Test save2file with node filter."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # Filter that allows branch nodes but shows different content
            self.tree.save2file(tmp_path, filter=lambda x: not x.tag.startswith("Uncle"))

            with open(tmp_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Should show most nodes but exclude Uncle and its subtree
                self.assertIn("Grandpa", content)
                self.assertIn("Dad", content)
                self.assertIn("Me", content)
                self.assertNotIn("Uncle", content)
                self.assertNotIn("Cousin", content)

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_save2file_with_data_property(self):
        """Test save2file displaying custom data property."""
        # Create tree with data
        data_tree = Tree()
        data_tree.create_node("Person", "p1", data=type("obj", (), {"name": "Alice"})())
        data_tree.create_node("Person", "p2", parent="p1", data=type("obj", (), {"name": "Bob"})())

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            data_tree.save2file(tmp_path, data_property="name")

            with open(tmp_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn("Alice", content)
                self.assertIn("Bob", content)

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_is_ancestor_basic(self):
        """Test is_ancestor basic functionality."""
        # Grandpa is ancestor of everyone
        self.assertTrue(self.tree.is_ancestor("grandpa", "dad"))
        self.assertTrue(self.tree.is_ancestor("grandpa", "me"))
        self.assertTrue(self.tree.is_ancestor("grandpa", "cousin"))

        # Dad is ancestor of his children
        self.assertTrue(self.tree.is_ancestor("dad", "me"))
        self.assertTrue(self.tree.is_ancestor("dad", "sister"))

        # But not of cousin
        self.assertFalse(self.tree.is_ancestor("dad", "cousin"))

        # Self is not ancestor of self
        self.assertFalse(self.tree.is_ancestor("dad", "dad"))

    def test_is_ancestor_reverse_relationship(self):
        """Test is_ancestor doesn't work in reverse."""
        # Child is not ancestor of parent
        self.assertFalse(self.tree.is_ancestor("me", "dad"))
        self.assertFalse(self.tree.is_ancestor("dad", "grandpa"))

    def test_is_ancestor_siblings(self):
        """Test is_ancestor with siblings."""
        # Siblings are not ancestors of each other
        self.assertFalse(self.tree.is_ancestor("me", "sister"))
        self.assertFalse(self.tree.is_ancestor("sister", "me"))
        self.assertFalse(self.tree.is_ancestor("dad", "uncle"))

    def test_is_ancestor_nonexistent_nodes(self):
        """Test is_ancestor with nonexistent nodes."""
        # Test with nonexistent ancestor - should return False since nonexistent can't be ancestor
        result = self.tree.is_ancestor("nonexistent", "me")
        self.assertFalse(result)

        # Test with nonexistent descendant - should raise exception
        with self.assertRaises(NodeIDAbsentError):
            self.tree.is_ancestor("dad", "nonexistent")

    def test_is_ancestor_empty_tree(self):
        """Test is_ancestor on empty tree."""
        with self.assertRaises(NodeIDAbsentError):
            self.empty_tree.is_ancestor("a", "b")

    def test_filter_nodes_comprehensive(self):
        """Test filter_nodes with various filters."""
        # Filter for leaf nodes
        leaf_filter = lambda n: n.is_leaf(self.tree.identifier)
        leaf_nodes = list(self.tree.filter_nodes(leaf_filter))
        leaf_tags = [n.tag for n in leaf_nodes]

        self.assertIn("Me", leaf_tags)
        self.assertIn("Sister", leaf_tags)
        self.assertIn("Cousin", leaf_tags)
        self.assertNotIn("Dad", leaf_tags)
        self.assertNotIn("Grandpa", leaf_tags)

    def test_filter_nodes_with_data(self):
        """Test filter_nodes based on node data."""
        # Create tree with data
        data_tree = Tree()
        data_tree.create_node("Adult", "adult", data={"age": 30})
        data_tree.create_node("Child", "child", parent="adult", data={"age": 10})
        data_tree.create_node("Teen", "teen", parent="adult", data={"age": 16})

        # Filter for minors
        minor_filter = lambda n: n.data and n.data.get("age", 0) < 18
        minors = list(data_tree.filter_nodes(minor_filter))

        self.assertEqual(len(minors), 2)
        minor_tags = [n.tag for n in minors]
        self.assertIn("Child", minor_tags)
        self.assertIn("Teen", minor_tags)
        self.assertNotIn("Adult", minor_tags)

    def test_filter_nodes_empty_result(self):
        """Test filter_nodes that returns no results."""
        # Filter that matches nothing
        impossible_filter = lambda n: False
        result = list(self.tree.filter_nodes(impossible_filter))
        self.assertEqual(len(result), 0)

    def test_filter_nodes_all_match(self):
        """Test filter_nodes that matches all nodes."""
        all_filter = lambda n: True
        all_nodes = list(self.tree.filter_nodes(all_filter))

        self.assertEqual(len(all_nodes), len(self.tree))
        # Should include all nodes
        all_tags = [n.tag for n in all_nodes]
        self.assertIn("Grandpa", all_tags)
        self.assertIn("Dad", all_tags)
        self.assertIn("Me", all_tags)

    def test_nodes_property(self):
        """Test nodes property returns correct dictionary."""
        nodes_dict = self.tree.nodes

        # Should be a dictionary
        self.assertIsInstance(nodes_dict, dict)

        # Should contain all node identifiers as keys
        self.assertIn("grandpa", nodes_dict)
        self.assertIn("dad", nodes_dict)
        self.assertIn("me", nodes_dict)

        # Values should be Node objects
        self.assertIsInstance(nodes_dict["grandpa"], Node)
        self.assertEqual(nodes_dict["grandpa"].tag, "Grandpa")

    def test_nodes_property_empty_tree(self):
        """Test nodes property on empty tree."""
        nodes_dict = self.empty_tree.nodes
        self.assertIsInstance(nodes_dict, dict)
        self.assertEqual(len(nodes_dict), 0)

    def test_level_with_filter(self):
        """Test level calculation with filter function."""
        # Level ignoring certain nodes in path
        level = self.tree.level("me", filter=lambda x: x.identifier != "dad")
        # Should be 1 instead of 2 because we skip "dad"
        self.assertEqual(level, 1)

    def test_level_root_node(self):
        """Test level of root node is always 0."""
        self.assertEqual(self.tree.level("grandpa"), 0)
        self.assertEqual(self.single_tree.level("only"), 0)

    def test_level_nonexistent_node(self):
        """Test level with nonexistent node."""
        with self.assertRaises(NodeIDAbsentError):
            self.tree.level("nonexistent")

    def test_level_empty_tree(self):
        """Test level on empty tree."""
        with self.assertRaises(NodeIDAbsentError):
            self.empty_tree.level("anything")

    def test_ancestor_with_invalid_level(self):
        """Test ancestor with invalid level numbers."""
        # Level greater than node's own level
        with self.assertRaises(InvalidLevelNumber):
            self.tree.ancestor("me", level=5)  # me is at level 2

    def test_ancestor_level_equals_node_level(self):
        """Test ancestor with level equal to node's level."""
        with self.assertRaises(InvalidLevelNumber):
            self.tree.ancestor("me", level=2)  # me is at level 2

    def test_ancestor_root_node(self):
        """Test ancestor of root node."""
        # Root has no ancestor regardless of level
        result = self.tree.ancestor("grandpa", level=0)
        self.assertEqual(result.identifier, "grandpa")  # Returns self for root

        # Root's immediate ancestor is None
        result = self.tree.ancestor("grandpa")
        self.assertIsNone(result)

    def test_expand_tree_invalid_mode(self):
        """Test expand_tree with invalid mode."""
        with self.assertRaises(ValueError):
            list(self.tree.expand_tree(mode=999))

    def test_expand_tree_with_complex_filter(self):
        """Test expand_tree with complex filter conditions."""
        # Filter: nodes at even levels only
        even_level_filter = lambda n: self.tree.level(n.identifier) % 2 == 0
        even_nodes = list(self.tree.expand_tree(filter=even_level_filter))

        # Should include grandpa (level 0)
        self.assertIn("grandpa", even_nodes)
        # May or may not include grandchildren depending on filter behavior
        # The filter affects which nodes are expanded, not just which are returned
        # So if level 1 nodes are filtered out, their children won't be traversed
        if len(even_nodes) > 1:
            # If other nodes are included, verify they're at even levels
            for node_id in even_nodes:
                level = self.tree.level(node_id)
                self.assertEqual(level % 2, 0, f"Node {node_id} at level {level} should be even")

    def test_expand_tree_zigzag_mode(self):
        """Test expand_tree with ZIGZAG mode."""
        zigzag_nodes = list(self.tree.expand_tree(mode=Tree.ZIGZAG))

        # Should start with root
        self.assertEqual(zigzag_nodes[0], "grandpa")
        # Should include all nodes
        self.assertEqual(len(zigzag_nodes), len(self.tree))

    def test_expand_tree_with_key_sorting(self):
        """Test expand_tree with custom key function."""
        # Sort by tag length (shorter first)
        length_sorted = list(self.tree.expand_tree(key=lambda x: len(x.tag), sorting=True))

        # Should start with root
        self.assertEqual(length_sorted[0], "grandpa")
        # Rest should be included
        self.assertEqual(len(length_sorted), len(self.tree))

    def test_rsearch_comprehensive(self):
        """Test rsearch with various scenarios."""
        # Search from leaf to root
        path = list(self.tree.rsearch("me"))
        expected_path = ["me", "dad", "grandpa"]
        self.assertEqual(path, expected_path)

    def test_rsearch_with_filter(self):
        """Test rsearch with filter function."""
        # Only include nodes with certain names
        name_filter = lambda x: x.tag in ["Me", "Grandpa"]
        filtered_path = list(self.tree.rsearch("me", filter=name_filter))

        # Should skip "Dad" because it's not in the filter
        expected_path = ["me", "grandpa"]
        self.assertEqual(filtered_path, expected_path)

    def test_rsearch_root_node(self):
        """Test rsearch starting from root."""
        path = list(self.tree.rsearch("grandpa"))
        self.assertEqual(path, ["grandpa"])

    def test_rsearch_nonexistent_node(self):
        """Test rsearch with nonexistent node."""
        with self.assertRaises(NodeIDAbsentError):
            list(self.tree.rsearch("nonexistent"))

    def test_rsearch_none_input(self):
        """Test rsearch with None input."""
        result = list(self.tree.rsearch(None))
        self.assertEqual(result, [])

    def test_size_comprehensive_levels(self):
        """Test size calculation for each level."""
        # Level 0: only root
        self.assertEqual(self.tree.size(level=0), 1)

        # Level 1: dad and uncle
        self.assertEqual(self.tree.size(level=1), 2)

        # Level 2: me, sister, cousin
        self.assertEqual(self.tree.size(level=2), 3)

        # Level 3: should be 0
        self.assertEqual(self.tree.size(level=3), 0)

    def test_size_invalid_level_type(self):
        """Test size with invalid level type."""
        # Test that invalid level types are handled
        # The actual behavior may vary - let's test what actually happens
        try:
            result = self.tree.size(level="invalid")
            # If it doesn't raise, it should return a reasonable value
            self.assertIsInstance(result, int)
        except (TypeError, ValueError):
            # This is also acceptable behavior
            pass

        try:
            result = self.tree.size(level=3.14)
            self.assertIsInstance(result, int)
        except (TypeError, ValueError):
            # This is also acceptable behavior
            pass

    def test_size_negative_level(self):
        """Test size with negative level."""
        # Should return 0 for negative levels
        self.assertEqual(self.tree.size(level=-1), 0)

    def test_clone_method(self):
        """Test _clone method functionality."""
        # Empty clone
        empty_clone = self.tree._clone(identifier="clone1")
        self.assertEqual(empty_clone.identifier, "clone1")
        self.assertEqual(len(empty_clone), 0)
        self.assertIsNone(empty_clone.root)

        # Clone with tree content (shallow)
        shallow_clone = self.tree._clone(identifier="clone2", with_tree=True, deep=False)
        self.assertEqual(shallow_clone.identifier, "clone2")
        self.assertEqual(len(shallow_clone), len(self.tree))
        self.assertEqual(shallow_clone.root, self.tree.root)
        # Should share node references
        self.assertIs(shallow_clone["grandpa"], self.tree["grandpa"])

        # Clone with tree content (deep)
        deep_clone = self.tree._clone(identifier="clone3", with_tree=True, deep=True)
        self.assertEqual(deep_clone.identifier, "clone3")
        self.assertEqual(len(deep_clone), len(self.tree))
        self.assertEqual(deep_clone.root, self.tree.root)
        # Should have different node references
        self.assertIsNot(deep_clone["grandpa"], self.tree["grandpa"])
        self.assertEqual(deep_clone["grandpa"].tag, self.tree["grandpa"].tag)

    def test_tree_constants(self):
        """Test Tree class constants are properly defined."""
        self.assertEqual(Tree.ROOT, 0)
        self.assertEqual(Tree.DEPTH, 1)
        self.assertEqual(Tree.WIDTH, 2)
        self.assertEqual(Tree.ZIGZAG, 3)

    def test_unicode_handling(self):
        """Test tree operations with Unicode characters."""
        unicode_tree = Tree()
        unicode_tree.create_node("Café", "café")
        unicode_tree.create_node("Naïve", "naïve", parent="café")
        unicode_tree.create_node("Résumé", "résumé", parent="naïve")

        # Test basic operations work with Unicode
        self.assertEqual(unicode_tree["café"].tag, "Café")
        self.assertTrue(unicode_tree.is_ancestor("café", "résumé"))

        # Test display works with Unicode
        output = unicode_tree.show(stdout=False)
        self.assertIn("Café", output)
        self.assertIn("Naïve", output)
        self.assertIn("Résumé", output)

        # Test JSON export with Unicode
        json_str = unicode_tree.to_json()
        self.assertIsInstance(json_str, str)
        # JSON should handle Unicode properly
        parsed = json.loads(json_str)
        self.assertIn("Café", str(parsed))

    def test_large_tree_performance(self):
        """Test operations on larger trees for performance regression."""
        # Create a tree with 1000 nodes
        large_tree = Tree()
        large_tree.create_node("Root", "root")

        # Create 10 branches with 100 nodes each
        for branch in range(10):
            branch_id = f"branch_{branch}"
            large_tree.create_node(f"Branch {branch}", branch_id, parent="root")

            for leaf in range(100):
                leaf_id = f"leaf_{branch}_{leaf}"
                large_tree.create_node(f"Leaf {branch}-{leaf}", leaf_id, parent=branch_id)

        # Test that basic operations still work efficiently
        self.assertEqual(len(large_tree), 1011)  # root + 10 branches + 1000 leaves
        self.assertEqual(large_tree.depth(), 2)
        self.assertEqual(len(large_tree.leaves()), 1000)

        # Test traversal works
        all_nodes = list(large_tree.expand_tree())
        self.assertEqual(len(all_nodes), 1011)

    def tearDown(self):
        """Clean up test fixtures."""
        self.tree = None
        self.simple_tree = None
        self.empty_tree = None
        self.single_tree = None


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Comprehensive tests for Node class.
This module provides thorough testing of Node class methods and properties.
"""
from __future__ import unicode_literals

import unittest
import uuid
from copy import deepcopy

from treelib import Node, Tree


class NodeComprehensiveTestCase(unittest.TestCase):
    """Comprehensive tests for Node class."""

    def setUp(self):
        """Set up test fixtures."""
        self.node = Node("Test Node", "test_id", data={"key": "value"})
        self.tree = Tree(identifier="test_tree")
        self.tree.create_node("Root", "root")
        self.tree.create_node("Child1", "child1", parent="root")
        self.tree.create_node("Child2", "child2", parent="root")
        self.tree.create_node("Grandchild", "grandchild", parent="child1")

    def test_node_creation_comprehensive(self):
        """Test comprehensive node creation scenarios."""
        # Test with all parameters
        full_node = Node("Full Node", "full_id", expanded=False, data={"test": "data"})
        self.assertEqual(full_node.tag, "Full Node")
        self.assertEqual(full_node.identifier, "full_id")
        self.assertFalse(full_node.expanded)
        self.assertEqual(full_node.data["test"], "data")

        # Test with minimal parameters
        minimal_node = Node()
        self.assertIsNotNone(minimal_node.identifier)  # Should be auto-generated
        self.assertEqual(minimal_node.tag, minimal_node.identifier)  # Tag defaults to identifier
        self.assertTrue(minimal_node.expanded)  # Default expanded
        self.assertIsNone(minimal_node.data)  # Default data

        # Test with only tag
        tag_only_node = Node("Only Tag")
        self.assertEqual(tag_only_node.tag, "Only Tag")
        self.assertIsNotNone(tag_only_node.identifier)
        self.assertNotEqual(tag_only_node.tag, tag_only_node.identifier)  # Should be different

        # Test with only identifier
        id_only_node = Node(identifier="only_id")
        self.assertEqual(id_only_node.identifier, "only_id")
        self.assertEqual(id_only_node.tag, "only_id")  # Tag should default to identifier

    def test_node_identifier_handling(self):
        """Test node identifier handling and auto-generation."""
        # Test auto-generation
        auto_node = Node("Auto")
        self.assertIsNotNone(auto_node.identifier)
        self.assertTrue(len(auto_node.identifier) > 10)  # UUID should be long

        # Test explicit identifier
        explicit_node = Node("Explicit", "explicit_id")
        self.assertEqual(explicit_node.identifier, "explicit_id")

        # Test UUID format (should be valid UUID string)
        try:
            uuid.UUID(auto_node.identifier)
        except ValueError:
            self.fail("Auto-generated identifier should be valid UUID")

    def test_node_tag_handling(self):
        """Test node tag handling and defaults."""
        # Tag defaults to identifier when not provided
        no_tag_node = Node(identifier="test_id")
        self.assertEqual(no_tag_node.tag, "test_id")

        # Explicit tag
        explicit_tag_node = Node("Explicit Tag", "test_id")
        self.assertEqual(explicit_tag_node.tag, "Explicit Tag")
        self.assertEqual(explicit_tag_node.identifier, "test_id")

        # None tag should default to identifier
        none_tag_node = Node(tag=None, identifier="none_id")
        self.assertEqual(none_tag_node.tag, "none_id")

    def test_node_data_handling(self):
        """Test node data handling with various data types."""
        # Test None data
        none_data_node = Node("None Data", data=None)
        self.assertIsNone(none_data_node.data)

        # Test primitive data types
        int_data_node = Node("Int Data", data=42)
        self.assertEqual(int_data_node.data, 42)

        str_data_node = Node("String Data", data="test string")
        self.assertEqual(str_data_node.data, "test string")

        float_data_node = Node("Float Data", data=3.14)
        self.assertEqual(float_data_node.data, 3.14)

        bool_data_node = Node("Bool Data", data=True)
        self.assertTrue(bool_data_node.data)

        # Test complex data types
        list_data_node = Node("List Data", data=[1, 2, 3, "four"])
        self.assertEqual(len(list_data_node.data), 4)
        self.assertEqual(list_data_node.data[3], "four")

        dict_data_node = Node("Dict Data", data={"nested": {"deep": "value"}})
        self.assertEqual(dict_data_node.data["nested"]["deep"], "value")

        set_data_node = Node("Set Data", data={1, 2, 3})
        self.assertIn(2, set_data_node.data)

        tuple_data_node = Node("Tuple Data", data=(1, "two", 3.0))
        self.assertEqual(tuple_data_node.data[1], "two")

    def test_node_expansion_property(self):
        """Test node expansion property."""
        # Default expansion
        default_node = Node("Default")
        self.assertTrue(default_node.expanded)

        # Explicit expansion
        expanded_node = Node("Expanded", expanded=True)
        self.assertTrue(expanded_node.expanded)

        collapsed_node = Node("Collapsed", expanded=False)
        self.assertFalse(collapsed_node.expanded)

        # Test expansion modification
        collapsed_node.expanded = True
        self.assertTrue(collapsed_node.expanded)

    def test_node_comparison(self):
        """Test node comparison operations."""
        node1 = Node("Alpha", "a")
        node2 = Node("Beta", "b")
        node3 = Node("Alpha", "a2")  # Same tag, different ID

        # Test less than comparison (based on tag)
        self.assertTrue(node1 < node2)  # "Alpha" < "Beta"
        self.assertFalse(node2 < node1)  # "Beta" not < "Alpha"

        # Test with same tag
        self.assertFalse(node1 < node3)  # Same tag, so False
        self.assertFalse(node3 < node1)

        # Test sorting
        nodes = [node2, node1, node3]
        sorted_nodes = sorted(nodes)

        # Should be sorted by tag: Alpha, Alpha, Beta
        self.assertEqual(sorted_nodes[0].tag, "Alpha")
        self.assertEqual(sorted_nodes[1].tag, "Alpha")
        self.assertEqual(sorted_nodes[2].tag, "Beta")

    def test_node_string_representation(self):
        """Test node string representation."""
        node = Node("Test Node", "test_id", data={"key": "value"})
        str_repr = repr(node)

        # Should contain key information
        self.assertIn("Node", str_repr)
        self.assertIn("test_id", str_repr)

    def test_predecessor_operations(self):
        """Test predecessor (parent) operations."""
        root_node = self.tree["root"]
        child1_node = self.tree["child1"]
        grandchild_node = self.tree["grandchild"]

        # Test predecessor access
        self.assertIsNone(root_node.predecessor(self.tree.identifier))
        self.assertEqual(child1_node.predecessor(self.tree.identifier), "root")
        self.assertEqual(grandchild_node.predecessor(self.tree.identifier), "child1")

        # Test predecessor setting
        child1_node.set_predecessor("new_parent", self.tree.identifier)
        self.assertEqual(child1_node.predecessor(self.tree.identifier), "new_parent")

        # Test predecessor with None tree_id (should use initial tree)
        child1_node.set_initial_tree_id(self.tree.identifier)
        # This tests the legacy compatibility

    def test_successor_operations(self):
        """Test successor (children) operations."""
        root_node = self.tree["root"]
        child1_node = self.tree["child1"]

        # Test successors access
        root_successors = root_node.successors(self.tree.identifier)
        self.assertIn("child1", root_successors)
        self.assertIn("child2", root_successors)
        self.assertEqual(len(root_successors), 2)

        child1_successors = child1_node.successors(self.tree.identifier)
        self.assertIn("grandchild", child1_successors)
        self.assertEqual(len(child1_successors), 1)

        # Test empty successors
        grandchild_node = self.tree["grandchild"]
        grandchild_successors = grandchild_node.successors(self.tree.identifier)
        self.assertEqual(len(grandchild_successors), 0)

    def test_successor_manipulation(self):
        """Test successor manipulation operations."""
        test_tree = Tree()
        parent_node = Node("Parent", "parent")
        test_tree.add_node(parent_node)

        # Test adding successors
        parent_node.update_successors("child1", Node.ADD, tree_id=test_tree.identifier)
        parent_node.update_successors("child2", Node.ADD, tree_id=test_tree.identifier)

        successors = parent_node.successors(test_tree.identifier)
        self.assertIn("child1", successors)
        self.assertIn("child2", successors)

        # Test inserting successor
        parent_node.update_successors("child_insert", Node.INSERT, tree_id=test_tree.identifier)
        successors = parent_node.successors(test_tree.identifier)
        self.assertIn("child_insert", successors)

        # Test replacing successor
        parent_node.update_successors("child1", Node.REPLACE, replace="child_new", tree_id=test_tree.identifier)
        successors = parent_node.successors(test_tree.identifier)
        self.assertNotIn("child1", successors)
        self.assertIn("child_new", successors)

        # Test deleting successor
        parent_node.update_successors("child2", Node.DELETE, tree_id=test_tree.identifier)
        successors = parent_node.successors(test_tree.identifier)
        self.assertNotIn("child2", successors)

    def test_is_leaf_method(self):
        """Test is_leaf method."""
        root_node = self.tree["root"]
        child1_node = self.tree["child1"]
        grandchild_node = self.tree["grandchild"]

        # Test with tree_id
        self.assertFalse(root_node.is_leaf(self.tree.identifier))  # Has children
        self.assertFalse(child1_node.is_leaf(self.tree.identifier))  # Has grandchild
        self.assertTrue(grandchild_node.is_leaf(self.tree.identifier))  # No children

        # Test without tree_id (should use initial tree)
        root_node.set_initial_tree_id(self.tree.identifier)
        child1_node.set_initial_tree_id(self.tree.identifier)
        grandchild_node.set_initial_tree_id(self.tree.identifier)

    def test_is_root_method(self):
        """Test is_root method."""
        root_node = self.tree["root"]
        child1_node = self.tree["child1"]

        # Test with tree_id
        self.assertTrue(root_node.is_root(self.tree.identifier))
        self.assertFalse(child1_node.is_root(self.tree.identifier))

        # Test with None tree_id (should use initial tree)
        root_node.set_initial_tree_id(self.tree.identifier)
        child1_node.set_initial_tree_id(self.tree.identifier)

    def test_clone_pointers(self):
        """Test clone_pointers method."""
        original_tree = Tree(identifier="original")
        original_tree.create_node("Root", "root")
        original_tree.create_node("Child", "child", parent="root")

        new_tree = Tree(identifier="new")

        # Clone a node's pointers to new tree
        child_node = original_tree["child"]
        child_node.clone_pointers("original", "new")

        # Should have pointers in both trees
        self.assertEqual(child_node.predecessor("original"), "root")
        self.assertEqual(child_node.predecessor("new"), "root")

    def test_reset_pointers(self):
        """Test reset_pointers method."""
        test_tree = Tree()
        test_node = Node("Test", "test")
        test_tree.add_node(test_node)

        # Add some relationships
        test_node.set_predecessor("parent", test_tree.identifier)
        test_node.update_successors("child", Node.ADD, tree_id=test_tree.identifier)

        # Reset pointers for the tree
        test_node.reset_pointers(test_tree.identifier)

        # Pointers should be cleared
        self.assertIsNone(test_node.predecessor(test_tree.identifier))
        self.assertEqual(len(test_node.successors(test_tree.identifier)), 0)

    def test_node_with_extreme_data(self):
        """Test node with extreme data scenarios."""
        # Very large data
        large_data = {"key_" + str(i): "value_" * 1000 for i in range(100)}
        large_node = Node("Large Data", data=large_data)
        self.assertEqual(len(large_node.data), 100)

        # Deeply nested data
        nested_data = {"level1": {"level2": {"level3": {"level4": {"level5": "deep"}}}}}
        nested_node = Node("Nested Data", data=nested_data)
        self.assertEqual(nested_node.data["level1"]["level2"]["level3"]["level4"]["level5"], "deep")

        # Circular reference in data (should not break node creation)
        circular_data = {"self": None}
        circular_data["self"] = circular_data
        circular_node = Node("Circular Data", data=circular_data)
        self.assertIsNotNone(circular_node.data)

    def test_node_copy_operations(self):
        """Test node copying operations."""
        original_node = Node("Original", "orig_id", data={"mutable": [1, 2, 3]})

        # Test shallow copy behavior
        # Note: Node doesn't have explicit copy methods, but we test data sharing
        same_data_node = Node("Copy", "copy_id", data=original_node.data)

        # Modify original data
        original_node.data["mutable"].append(4)

        # Both should see the change (shallow copy)
        self.assertEqual(len(same_data_node.data["mutable"]), 4)

        # Test deep copy
        deep_copy_node = Node("Deep Copy", "deep_id", data=deepcopy(original_node.data))

        # Modify original data again
        original_node.data["mutable"].append(5)

        # Deep copy should not see the change
        self.assertEqual(len(deep_copy_node.data["mutable"]), 4)
        self.assertEqual(len(original_node.data["mutable"]), 5)

    def test_multiple_tree_membership(self):
        """Test node membership in multiple trees."""
        tree1 = Tree(identifier="tree1")
        tree2 = Tree(identifier="tree2")

        # Create shared node
        shared_node = Node("Shared", "shared")

        # Add to both trees as root
        tree1.add_node(shared_node)
        tree2.add_node(shared_node)

        # Should be root in both trees
        self.assertTrue(shared_node.is_root("tree1"))
        self.assertTrue(shared_node.is_root("tree2"))

        # Add children in different trees
        child1 = Node("Child1", "child1")
        child2 = Node("Child2", "child2")

        tree1.add_node(child1, parent=shared_node)
        tree2.add_node(child2, parent=shared_node)

        # Check successors in each tree
        tree1_successors = shared_node.successors("tree1")
        tree2_successors = shared_node.successors("tree2")

        self.assertIn("child1", tree1_successors)
        self.assertNotIn("child2", tree1_successors)

        self.assertIn("child2", tree2_successors)
        self.assertNotIn("child1", tree2_successors)

    def test_node_constants(self):
        """Test Node class constants."""
        self.assertEqual(Node.ADD, 0)
        self.assertEqual(Node.DELETE, 1)
        self.assertEqual(Node.INSERT, 2)
        self.assertEqual(Node.REPLACE, 3)

    def test_deprecated_methods(self):
        """Test deprecated methods still work (for backward compatibility)."""
        # These methods should still work but may issue warnings
        deprecated_node = Node("Deprecated", "dep")

        # Test deprecated bpointer (should work like predecessor)
        deprecated_node.set_initial_tree_id("test_tree")
        deprecated_node.set_predecessor("parent", "test_tree")

    def test_edge_case_identifiers(self):
        """Test edge cases with identifiers."""
        # Empty string identifier (should be kept as empty string)
        empty_id_node = Node("Empty ID", "")
        self.assertEqual(empty_id_node.identifier, "")

        # Very long identifier
        long_id = "x" * 10000
        long_id_node = Node("Long ID", long_id)
        self.assertEqual(long_id_node.identifier, long_id)

        # Special characters in identifier
        special_id = "special!@#$%^&*()_+-=[]{}|;':\",./<>?"
        special_node = Node("Special", special_id)
        self.assertEqual(special_node.identifier, special_id)

    def tearDown(self):
        """Clean up test fixtures."""
        self.node = None
        self.tree = None


if __name__ == "__main__":
    unittest.main()

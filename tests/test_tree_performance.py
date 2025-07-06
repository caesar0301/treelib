#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Performance tests for Tree class.
This module focuses on performance benchmarks and stress tests.
"""
from __future__ import unicode_literals

import time
import unittest

from treelib import Tree


class TreePerformanceTestCase(unittest.TestCase):
    """Performance tests for Tree class."""

    def setUp(self):
        """Set up test fixtures."""
        self.performance_threshold = 5.0  # 5 seconds max for operations

    def test_large_tree_creation_performance(self):
        """Test performance of creating large trees."""
        start_time = time.time()

        # Create a tree with 10,000 nodes
        large_tree = Tree()
        large_tree.create_node("Root", "root")

        # Create 100 branches with 100 nodes each
        for branch in range(100):
            branch_id = f"branch_{branch}"
            large_tree.create_node(f"Branch {branch}", branch_id, parent="root")

            for leaf in range(99):  # 99 + 1 branch = 100 per branch
                leaf_id = f"leaf_{branch}_{leaf}"
                large_tree.create_node(f"Leaf {branch}-{leaf}", leaf_id, parent=branch_id)

        creation_time = time.time() - start_time

        # Verify tree was created correctly
        self.assertEqual(len(large_tree), 10001)  # root + 100 branches + 9900 leaves

        # Performance assertion
        self.assertLess(
            creation_time,
            self.performance_threshold,
            f"Tree creation took {creation_time:.2f}s, expected < {self.performance_threshold}s",
        )

        print(f"Large tree creation: {creation_time:.3f}s for {len(large_tree)} nodes")

    def test_tree_traversal_performance(self):
        """Test performance of tree traversal operations."""
        # Create a balanced tree
        tree = Tree()
        tree.create_node("Root", "root")

        # Create 4 levels with branching factor of 10
        current_level = ["root"]
        for level in range(4):
            next_level = []
            for parent in current_level:
                for i in range(10):
                    child_id = f"{parent}_child_{i}"
                    tree.create_node(f"Node {child_id}", child_id, parent=parent)
                    next_level.append(child_id)
            current_level = next_level

        # Should have 1 + 10 + 100 + 1000 + 10000 = 11,111 nodes
        expected_nodes = 1 + 10 + 100 + 1000 + 10000
        self.assertEqual(len(tree), expected_nodes)

        # Test different traversal methods
        traversal_methods = [("DEPTH", Tree.DEPTH), ("WIDTH", Tree.WIDTH), ("ZIGZAG", Tree.ZIGZAG)]

        for method_name, method_const in traversal_methods:
            start_time = time.time()

            # Perform traversal
            nodes = list(tree.expand_tree(mode=method_const))

            traversal_time = time.time() - start_time

            # Verify all nodes were traversed
            self.assertEqual(len(nodes), expected_nodes)

            # Performance assertion
            self.assertLess(
                traversal_time, self.performance_threshold, f"{method_name} traversal took {traversal_time:.2f}s"
            )

            print(f"{method_name} traversal: {traversal_time:.3f}s for {len(nodes)} nodes")

    def test_node_lookup_performance(self):
        """Test performance of node lookup operations."""
        # Create tree with many nodes
        tree = Tree()
        tree.create_node("Root", "root")

        node_ids = []
        for i in range(5000):
            node_id = f"node_{i}"
            tree.create_node(f"Node {i}", node_id, parent="root")
            node_ids.append(node_id)

        # Test lookup performance
        start_time = time.time()

        # Lookup each node
        for node_id in node_ids:
            node = tree[node_id]
            self.assertEqual(node.identifier, node_id)

        lookup_time = time.time() - start_time

        # Performance assertion
        self.assertLess(lookup_time, self.performance_threshold, f"Node lookups took {lookup_time:.2f}s")

        print(f"Node lookups: {lookup_time:.3f}s for {len(node_ids)} lookups")

    def test_tree_modification_performance(self):
        """Test performance of tree modification operations."""
        tree = Tree()
        tree.create_node("Root", "root")

        # Test adding many nodes
        start_time = time.time()

        for i in range(1000):
            tree.create_node(f"Node {i}", f"node_{i}", parent="root")

        add_time = time.time() - start_time

        # Test moving nodes
        start_time = time.time()

        # Create a new parent for moving nodes
        tree.create_node("New Parent", "new_parent", parent="root")

        # Move first 100 nodes to new parent
        for i in range(100):
            tree.move_node(f"node_{i}", "new_parent")

        move_time = time.time() - start_time

        # Test removing nodes
        start_time = time.time()

        # Remove the last 100 nodes
        for i in range(900, 1000):
            tree.remove_node(f"node_{i}")

        remove_time = time.time() - start_time

        # Performance assertions
        self.assertLess(add_time, self.performance_threshold, f"Adding nodes took {add_time:.2f}s")
        self.assertLess(move_time, self.performance_threshold, f"Moving nodes took {move_time:.2f}s")
        self.assertLess(remove_time, self.performance_threshold, f"Removing nodes took {remove_time:.2f}s")

        print(f"Add 1000 nodes: {add_time:.3f}s")
        print(f"Move 100 nodes: {move_time:.3f}s")
        print(f"Remove 100 nodes: {remove_time:.3f}s")

    def test_tree_copying_performance(self):
        """Test performance of tree copying operations."""
        # Create source tree
        source_tree = Tree()
        source_tree.create_node("Root", "root")

        for i in range(1000):
            source_tree.create_node(f"Node {i}", f"node_{i}", parent="root", data={"index": i, "data": f"data_{i}"})

        # Test shallow copy
        start_time = time.time()
        shallow_copy = Tree(source_tree, deep=False)
        shallow_time = time.time() - start_time

        # Test deep copy
        start_time = time.time()
        deep_copy = Tree(source_tree, deep=True)
        deep_time = time.time() - start_time

        # Verify copies
        self.assertEqual(len(shallow_copy), len(source_tree))
        self.assertEqual(len(deep_copy), len(source_tree))

        # Performance assertions
        self.assertLess(shallow_time, self.performance_threshold, f"Shallow copy took {shallow_time:.2f}s")
        self.assertLess(deep_time, self.performance_threshold, f"Deep copy took {deep_time:.2f}s")

        print(f"Shallow copy: {shallow_time:.3f}s for {len(source_tree)} nodes")
        print(f"Deep copy: {deep_time:.3f}s for {len(source_tree)} nodes")

    def test_subtree_operations_performance(self):
        """Test performance of subtree operations."""
        # Create a large tree
        tree = Tree()
        tree.create_node("Root", "root")

        # Create subtrees
        for i in range(10):
            subtree_root = f"subtree_{i}"
            tree.create_node(f"Subtree {i}", subtree_root, parent="root")

            for j in range(100):
                tree.create_node(f"Node {i}-{j}", f"node_{i}_{j}", parent=subtree_root)

        # Test subtree extraction
        start_time = time.time()

        subtrees = []
        for i in range(10):
            subtree = tree.subtree(f"subtree_{i}")
            subtrees.append(subtree)

        subtree_time = time.time() - start_time

        # Test subtree removal
        start_time = time.time()

        removed_subtrees = []
        for i in range(5):  # Remove half the subtrees
            removed = tree.remove_subtree(f"subtree_{i}")
            removed_subtrees.append(removed)

        removal_time = time.time() - start_time

        # Verify operations
        self.assertEqual(len(subtrees), 10)
        self.assertEqual(len(removed_subtrees), 5)

        # Performance assertions
        self.assertLess(subtree_time, self.performance_threshold, f"Subtree extraction took {subtree_time:.2f}s")
        self.assertLess(removal_time, self.performance_threshold, f"Subtree removal took {removal_time:.2f}s")

        print(f"Subtree extraction: {subtree_time:.3f}s for 10 subtrees")
        print(f"Subtree removal: {removal_time:.3f}s for 5 subtrees")

    def test_filtering_performance(self):
        """Test performance of filtering operations."""
        # Create tree with mixed data
        tree = Tree()
        tree.create_node("Root", "root")

        for i in range(2000):
            tree.create_node(f"Node {i}", f"node_{i}", parent="root", data={"value": i, "even": i % 2 == 0})

        # Test filter_nodes performance
        start_time = time.time()

        even_nodes = list(tree.filter_nodes(lambda n: n.data and n.data.get("even", False)))

        filter_time = time.time() - start_time

        # Test expand_tree with filter
        start_time = time.time()

        high_value_nodes = list(tree.expand_tree(filter=lambda n: n.data and n.data.get("value", 0) > 1500))

        expand_filter_time = time.time() - start_time

        # Verify results
        self.assertEqual(len(even_nodes), 1000)  # Half should be even
        self.assertLess(len(high_value_nodes), 500)  # Should be < 500 high value nodes

        # Performance assertions
        self.assertLess(filter_time, self.performance_threshold, f"Filter nodes took {filter_time:.2f}s")
        self.assertLess(
            expand_filter_time, self.performance_threshold, f"Expand with filter took {expand_filter_time:.2f}s"
        )

        print(f"Filter nodes: {filter_time:.3f}s for {len(even_nodes)} matches")
        print(f"Expand with filter: {expand_filter_time:.3f}s for {len(high_value_nodes)} matches")

    def test_serialization_performance(self):
        """Test performance of serialization operations."""
        # Create tree with rich data
        tree = Tree()
        tree.create_node("Root", "root", data={"type": "root", "metadata": {"created": "2023-01-01"}})

        for i in range(500):
            tree.create_node(
                f"Node {i}",
                f"node_{i}",
                parent="root",
                data={
                    "index": i,
                    "name": f"Node {i}",
                    "properties": {
                        "active": True,
                        "tags": [f"tag_{j}" for j in range(5)],
                        "metadata": {"created": f"2023-01-{i % 28 + 1:02d}"},
                    },
                },
            )

        # Test JSON serialization
        start_time = time.time()

        json_without_data = tree.to_json(with_data=False)
        json_time_no_data = time.time() - start_time

        start_time = time.time()
        json_with_data = tree.to_json(with_data=True)
        json_time_with_data = time.time() - start_time

        # Test dict conversion
        start_time = time.time()
        dict_without_data = tree.to_dict(with_data=False)
        dict_time_no_data = time.time() - start_time

        start_time = time.time()
        dict_with_data = tree.to_dict(with_data=True)
        dict_time_with_data = time.time() - start_time

        # Verify results
        self.assertIsInstance(json_without_data, str)
        self.assertIsInstance(json_with_data, str)
        self.assertGreater(len(json_with_data), len(json_without_data))

        # Performance assertions
        self.assertLess(
            json_time_no_data, self.performance_threshold, f"JSON serialization (no data) took {json_time_no_data:.2f}s"
        )
        self.assertLess(
            json_time_with_data,
            self.performance_threshold,
            f"JSON serialization (with data) took {json_time_with_data:.2f}s",
        )

        print(f"JSON (no data): {json_time_no_data:.3f}s")
        print(f"JSON (with data): {json_time_with_data:.3f}s")
        print(f"Dict (no data): {dict_time_no_data:.3f}s")
        print(f"Dict (with data): {dict_time_with_data:.3f}s")

    def test_memory_usage_large_tree(self):
        """Test memory usage with large trees."""
        import gc

        # Force garbage collection
        gc.collect()

        # Measure initial memory (simplified)
        initial_objects = len(gc.get_objects())

        # Create large tree
        tree = Tree()
        tree.create_node("Root", "root")

        # Create 5000 nodes with data
        for i in range(5000):
            tree.create_node(
                f"Node {i}", f"node_{i}", parent="root", data={"index": i, "name": f"Node {i}", "active": True}
            )

        # Measure memory after creation
        after_creation_objects = len(gc.get_objects())

        # Perform operations
        _ = list(tree.expand_tree())
        _ = tree.leaves()
        _ = tree.to_json()

        # Measure memory after operations
        after_operations_objects = len(gc.get_objects())

        # Clean up
        del tree
        gc.collect()

        final_objects = len(gc.get_objects())

        print(f"Objects created: {after_creation_objects - initial_objects}")
        print(f"Objects after operations: {after_operations_objects - after_creation_objects}")
        print(f"Objects remaining: {final_objects - initial_objects}")

        # Memory should be mostly freed
        self.assertLess(final_objects - initial_objects, 100, "Memory leak detected: too many objects remaining")

    def test_concurrent_operations_simulation(self):
        """Simulate concurrent operations on tree (single-threaded simulation)."""
        tree = Tree()
        tree.create_node("Root", "root")

        # Simulate interleaved operations
        operations = []

        start_time = time.time()

        # Simulate 1000 mixed operations
        for i in range(1000):
            op_type = i % 4

            if op_type == 0:  # Add node
                tree.create_node(f"Node {i}", f"node_{i}", parent="root")
                operations.append(f"ADD node_{i}")
            elif op_type == 1:  # Lookup node
                if i > 0:
                    try:
                        _ = tree[f"node_{i-1}"]
                        operations.append(f"LOOKUP node_{i-1}")
                    except:
                        pass
            elif op_type == 2:  # Traverse
                if i % 10 == 0:  # Only every 10th operation
                    _ = list(tree.expand_tree())
                    operations.append("TRAVERSE")
            elif op_type == 3:  # Check containment
                if i > 0:
                    _ = tree.contains(f"node_{i-1}")
                    operations.append(f"CONTAINS node_{i-1}")

        total_time = time.time() - start_time

        # Performance assertion
        self.assertLess(total_time, self.performance_threshold, f"Mixed operations took {total_time:.2f}s")

        print(f"Mixed operations: {total_time:.3f}s for {len(operations)} operations")
        print(f"Final tree size: {len(tree)} nodes")

    def tearDown(self):
        """Clean up test fixtures."""
        # Force garbage collection to clean up large objects
        import gc

        gc.collect()


if __name__ == "__main__":
    unittest.main()

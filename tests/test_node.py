import unittest
import uuid
import warnings
from collections import defaultdict

from treelib import Node
from treelib.exceptions import NodePropertyError


class NodeCase(unittest.TestCase):
    def setUp(self):
        self.node1 = Node("Test One", "identifier 1")
        self.node2 = Node("Test Two", "identifier 2")
        self.tree_id1 = "tree_1"
        self.tree_id2 = "tree_2"

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

    def test_initialization_defaults(self):
        """Test node initialization with default values"""
        node = Node()
        self.assertIsNotNone(node.identifier)
        # tag defaults to identifier
        self.assertEqual(node.tag, node.identifier)
        self.assertTrue(node.expanded)
        self.assertIsNone(node.data)

    def test_initialization_with_data(self):
        """Test node initialization with custom data"""
        data = {"key": "value", "number": 42}
        node = Node("Test Node", "test_id", expanded=False, data=data)
        self.assertEqual(node.tag, "Test Node")
        self.assertEqual(node.identifier, "test_id")
        self.assertFalse(node.expanded)
        self.assertEqual(node.data, data)

    def test_initialization_auto_identifier(self):
        """Test that auto-generated identifiers are unique"""
        node1 = Node("Node1")
        node2 = Node("Node2")
        self.assertNotEqual(node1.identifier, node2.identifier)
        # Should be valid UUID format
        uuid.UUID(node1.identifier)  # Will raise exception if invalid
        uuid.UUID(node2.identifier)

    def test_set_tag(self):
        self.node1.tag = "Test 1"
        self.assertEqual(self.node1.tag, "Test 1")
        self.node1.tag = "Test One"

    def test_set_tag_none(self):
        """Test setting tag to None"""
        self.node1.tag = None
        self.assertIsNone(self.node1.tag)

    def test_object_as_node_tag(self):
        node = Node(tag=(0, 1))
        self.assertEqual(node.tag, (0, 1))
        self.assertTrue(node.__repr__().startswith("Node"))

    def test_set_identifier(self):
        self.node1.identifier = "ID1"
        self.assertEqual(self.node1.identifier, "ID1")
        self.node1.identifier = "identifier 1"

    def test_set_identifier_none_warning(self):
        """Test that setting identifier to None prints a warning"""
        import io
        import sys

        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.node1.identifier = None
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("WARNING: node ID can not be None", output)

    def test_expanded_property(self):
        """Test the expanded property"""
        self.assertTrue(self.node1.expanded)
        self.node1.expanded = False
        self.assertFalse(self.node1.expanded)

    def test_set_fpointer(self):
        # retro-compatibility
        self.node1.update_fpointer("identifier 2")
        self.assertEqual(self.node1.fpointer, ["identifier 2"])
        self.node1.fpointer = []
        self.assertEqual(self.node1.fpointer, [])

    def test_update_successors(self):
        self.node1.update_successors("identifier 2", tree_id="tree 1")
        self.assertEqual(self.node1.successors("tree 1"), ["identifier 2"])
        self.assertEqual(self.node1._successors["tree 1"], ["identifier 2"])
        self.node1.set_successors([], tree_id="tree 1")
        self.assertEqual(self.node1._successors["tree 1"], [])

    def test_update_successors_modes(self):
        """Test different modes for update_successors"""
        # Test ADD mode (default)
        self.node1.update_successors("child1", tree_id=self.tree_id1)
        self.node1.update_successors("child2", mode=Node.ADD, tree_id=self.tree_id1)
        self.assertEqual(self.node1.successors(self.tree_id1), ["child1", "child2"])

        # Test DELETE mode
        self.node1.update_successors("child1", mode=Node.DELETE, tree_id=self.tree_id1)
        self.assertEqual(self.node1.successors(self.tree_id1), ["child2"])

        # Test DELETE non-existent (should warn)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.node1.update_successors("nonexistent", mode=Node.DELETE, tree_id=self.tree_id1)
            self.assertTrue(len(w) > 0)
            self.assertIn("wasn't present in fpointer", str(w[0].message))

        # Test REPLACE mode
        self.node1.update_successors("child2", mode=Node.REPLACE, replace="child3", tree_id=self.tree_id1)
        self.assertEqual(self.node1.successors(self.tree_id1), ["child3"])

        # Test INSERT mode (deprecated, should warn)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.node1.update_successors("child4", mode=Node.INSERT, tree_id=self.tree_id1)
            self.assertTrue(len(w) > 0)
            self.assertIn("INSERT is deprecated", str(w[0].message))

    def test_update_successors_none(self):
        """Test update_successors with None nid"""
        initial_successors = list(self.node1.successors(self.tree_id1))
        self.node1.update_successors(None, tree_id=self.tree_id1)
        self.assertEqual(self.node1.successors(self.tree_id1), initial_successors)

    def test_update_successors_replace_without_replace_param(self):
        """Test REPLACE mode without replace parameter raises error"""
        self.node1.update_successors("child1", tree_id=self.tree_id1)
        with self.assertRaises(NodePropertyError):
            self.node1.update_successors("child1", mode=Node.REPLACE, tree_id=self.tree_id1)

    def test_update_successors_invalid_mode(self):
        """Test invalid mode raises NotImplementedError"""
        with self.assertRaises(NotImplementedError):
            self.node1.update_successors("child1", mode=999, tree_id=self.tree_id1)

    def test_set_successors_different_types(self):
        """Test set_successors with different data types"""
        # Test with list
        self.node1.set_successors(["child1", "child2"], tree_id=self.tree_id1)
        self.assertEqual(self.node1.successors(self.tree_id1), ["child1", "child2"])

        # Test with set
        self.node1.set_successors({"child3", "child4"}, tree_id=self.tree_id1)
        self.assertEqual(set(self.node1.successors(self.tree_id1)), {"child3", "child4"})

        # Test with dict (keys become successors)
        self.node1.set_successors({"child5": "data1", "child6": "data2"}, tree_id=self.tree_id1)
        self.assertEqual(set(self.node1.successors(self.tree_id1)), {"child5", "child6"})

        # Test with None
        self.node1.set_successors(None, tree_id=self.tree_id1)
        self.assertEqual(self.node1.successors(self.tree_id1), [])

    def test_set_successors_unsupported_type(self):
        """Test set_successors with unsupported type raises NotImplementedError"""
        with self.assertRaises(NotImplementedError):
            self.node1.set_successors("invalid_type", tree_id=self.tree_id1)

    def test_set_bpointer(self):
        # retro-compatibility
        self.node2.update_bpointer("identifier 1")
        self.assertEqual(self.node2.bpointer, "identifier 1")
        self.node2.bpointer = None
        self.assertEqual(self.node2.bpointer, None)

    def test_set_predecessor(self):
        self.node2.set_predecessor("identifier 1", "tree 1")
        self.assertEqual(self.node2.predecessor("tree 1"), "identifier 1")
        self.assertEqual(self.node2._predecessor["tree 1"], "identifier 1")
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

    def test_is_root(self):
        """Test is_root method"""
        # Test with explicit tree_id - need to set predecessor first to avoid
        # KeyError
        self.node1.set_predecessor(None, self.tree_id1)
        self.assertTrue(self.node1.is_root(self.tree_id1))  # No predecessor set
        self.node1.set_predecessor("parent", self.tree_id1)
        self.assertFalse(self.node1.is_root(self.tree_id1))

        # Test without tree_id (uses initial tree)
        self.node1.set_initial_tree_id(self.tree_id1)
        # Has predecessor in initial tree
        self.assertFalse(self.node1.is_root())

        # Test node without any predecessors - use initial tree approach
        node = Node("root")
        node.set_initial_tree_id(self.tree_id1)
        node.set_predecessor(None, self.tree_id1)
        self.assertTrue(node.is_root(self.tree_id1))

    def test_set_initial_tree_id(self):
        """Test set_initial_tree_id method"""
        self.assertIsNone(self.node1._initial_tree_id)
        self.node1.set_initial_tree_id(self.tree_id1)
        self.assertEqual(self.node1._initial_tree_id, self.tree_id1)

        # Should not change if already set
        self.node1.set_initial_tree_id(self.tree_id2)
        self.assertEqual(self.node1._initial_tree_id, self.tree_id1)

    def test_clone_pointers(self):
        """Test clone_pointers method"""
        # Set up source tree pointers
        self.node1.set_predecessor("parent", self.tree_id1)
        self.node1.set_successors(["child1", "child2"], tree_id=self.tree_id1)

        # Clone to new tree
        self.node1.clone_pointers(self.tree_id1, self.tree_id2)

        # Verify cloned pointers
        self.assertEqual(self.node1.predecessor(self.tree_id2), "parent")
        self.assertEqual(self.node1.successors(self.tree_id2), ["child1", "child2"])

        # Verify original pointers are still intact
        self.assertEqual(self.node1.predecessor(self.tree_id1), "parent")
        self.assertEqual(self.node1.successors(self.tree_id1), ["child1", "child2"])

        # Verify that modifying one doesn't affect the other (deep copy)
        self.node1.successors(self.tree_id2).append("child3")
        self.assertNotEqual(self.node1.successors(self.tree_id1), self.node1.successors(self.tree_id2))

    def test_reset_pointers(self):
        """Test reset_pointers method"""
        # Set up pointers
        self.node1.set_predecessor("parent", self.tree_id1)
        self.node1.set_successors(["child1", "child2"], tree_id=self.tree_id1)

        # Reset pointers
        self.node1.reset_pointers(self.tree_id1)

        # Verify reset
        self.assertIsNone(self.node1.predecessor(self.tree_id1))
        self.assertEqual(self.node1.successors(self.tree_id1), [])

    def test_node_constants(self):
        """Test node mode constants"""
        self.assertEqual(Node.ADD, 0)
        self.assertEqual(Node.DELETE, 1)
        self.assertEqual(Node.INSERT, 2)
        self.assertEqual(Node.REPLACE, 3)

    def test_lt_comparison(self):
        """Test __lt__ method for node comparison"""
        node_a = Node("A", "id_a")
        node_b = Node("B", "id_b")
        node_z = Node("Z", "id_z")

        self.assertTrue(node_a < node_b)
        self.assertTrue(node_b < node_z)
        self.assertFalse(node_z < node_a)

    def test_repr(self):
        """Test __repr__ method"""
        node = Node("Test Tag", "test_id", data={"key": "value"})
        repr_str = repr(node)

        self.assertIn("Node(", repr_str)
        self.assertIn("tag=Test Tag", repr_str)
        self.assertIn("identifier=test_id", repr_str)
        self.assertIn("data={'key': 'value'}", repr_str)

        # Test with None data
        node_no_data = Node("Test", "test")
        repr_str_no_data = repr(node_no_data)
        self.assertIn("data=None", repr_str_no_data)

    def test_data(self):
        class Flower(object):
            def __init__(self, color):
                self.color = color

            def __str__(self):
                return "%s" % self.color

        self.node1.data = Flower("red")
        self.assertEqual(self.node1.data.color, "red")

        # Test various data types
        self.node1.data = "string data"
        self.assertEqual(self.node1.data, "string data")

        self.node1.data = [1, 2, 3]
        self.assertEqual(self.node1.data, [1, 2, 3])

        self.node1.data = {"dict": "data"}
        self.assertEqual(self.node1.data, {"dict": "data"})

    def test_deprecated_methods_warnings(self):
        """Test that deprecated methods show warnings"""
        node = Node("test")
        node.set_initial_tree_id("tree1")

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            # Test deprecated bpointer property
            _ = node.bpointer
            node.bpointer = "parent"

            # Test deprecated fpointer property
            _ = node.fpointer
            node.fpointer = ["child"]

            # Test deprecated update methods
            node.update_bpointer("new_parent")
            node.update_fpointer("new_child")

            # Should have generated warnings
            self.assertTrue(len(w) > 0)

    def test_fpointer_setter_different_types(self):
        """Test deprecated fpointer setter with different types"""
        node = Node("test")
        node.set_initial_tree_id("tree1")

        # Test with list
        node.fpointer = ["child1", "child2"]
        self.assertEqual(node.fpointer, ["child1", "child2"])

        # Test with set
        node.fpointer = {"child3", "child4"}
        self.assertEqual(set(node.fpointer), {"child3", "child4"})

        # Test with dict
        node.fpointer = {"child5": "data", "child6": "data"}
        self.assertEqual(set(node.fpointer), {"child5", "child6"})

        # Test with None
        node.fpointer = None
        self.assertEqual(node.fpointer, [])

    def test_multiple_trees(self):
        """Test node behavior with multiple trees"""
        tree1_id = "tree1"
        tree2_id = "tree2"

        # Set different predecessors for different trees
        self.node1.set_predecessor("parent1", tree1_id)
        self.node1.set_predecessor("parent2", tree2_id)

        self.assertEqual(self.node1.predecessor(tree1_id), "parent1")
        self.assertEqual(self.node1.predecessor(tree2_id), "parent2")

        # Set different successors for different trees
        self.node1.set_successors(["child1a", "child1b"], tree_id=tree1_id)
        self.node1.set_successors(["child2a", "child2b"], tree_id=tree2_id)

        self.assertEqual(self.node1.successors(tree1_id), ["child1a", "child1b"])
        self.assertEqual(self.node1.successors(tree2_id), ["child2a", "child2b"])

        # Test is_leaf for different trees
        self.assertFalse(self.node1.is_leaf(tree1_id))
        self.assertFalse(self.node1.is_leaf(tree2_id))

        # Clear one tree's successors
        self.node1.set_successors([], tree_id=tree1_id)
        self.assertTrue(self.node1.is_leaf(tree1_id))
        self.assertFalse(self.node1.is_leaf(tree2_id))

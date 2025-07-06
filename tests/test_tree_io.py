#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Comprehensive tests for Tree I/O operations.
This module focuses on file operations, serialization, and data exchange.
"""
from __future__ import unicode_literals

import json
import os
import tempfile
import unittest

from treelib import Tree


class TreeIOTestCase(unittest.TestCase):
    """Comprehensive tests for Tree I/O operations."""

    def setUp(self):
        """Set up test fixtures."""
        # Company hierarchy tree
        self.company_tree = Tree(identifier="company")
        self.company_tree.create_node("CEO", "ceo")
        self.company_tree.create_node("CTO", "cto", parent="ceo")
        self.company_tree.create_node("CFO", "cfo", parent="ceo")
        self.company_tree.create_node("VP Engineering", "vp_eng", parent="cto")
        self.company_tree.create_node("VP Finance", "vp_fin", parent="cfo")
        self.company_tree.create_node("Senior Dev", "sr_dev", parent="vp_eng")
        self.company_tree.create_node("Junior Dev", "jr_dev", parent="vp_eng")

        # Tree with rich data
        self.data_tree = Tree(identifier="data_tree")
        self.data_tree.create_node("Project", "project", data={"budget": 100000, "status": "active"})
        self.data_tree.create_node("Frontend", "frontend", parent="project", data={"tech": "React", "team_size": 3})
        self.data_tree.create_node("Backend", "backend", parent="project", data={"tech": "Python", "team_size": 5})

    def test_save2file_comprehensive(self):
        """Test save2file with comprehensive scenarios."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # Test basic save
            self.company_tree.save2file(tmp_path)

            with open(tmp_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn("CEO", content)
                self.assertIn("CTO", content)
                self.assertIn("CFO", content)

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_save2file_with_identifiers(self):
        """Test save2file showing node identifiers."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            self.company_tree.save2file(tmp_path, idhidden=False)

            with open(tmp_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Should show identifiers in brackets
                self.assertIn("[ceo]", content)
                self.assertIn("[cto]", content)
                self.assertIn("[vp_eng]", content)

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_save2file_different_line_types(self):
        """Test save2file with different line drawing styles."""
        line_types = ["ascii", "ascii-ex", "ascii-exr", "ascii-em", "ascii-emv", "ascii-emh"]

        for line_type in line_types:
            with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
                tmp_path = tmp.name

            try:
                self.company_tree.save2file(tmp_path, line_type=line_type)

                with open(tmp_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    self.assertIn("CEO", content)
                    # Different line types have different characters
                    if line_type == "ascii":
                        self.assertIn("|--", content)
                    else:
                        # Unicode line types should have special chars
                        self.assertTrue(any(ord(c) > 127 for c in content))

            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

    def test_save2file_with_data_property(self):
        """Test save2file displaying custom data properties."""
        # Create tree with object data that has attributes
        prop_tree = Tree()

        class DataObj:
            def __init__(self, tech):
                self.tech = tech

        prop_tree.create_node("Project", "project", data=DataObj("General"))
        prop_tree.create_node("Frontend", "frontend", parent="project", data=DataObj("React"))
        prop_tree.create_node("Backend", "backend", parent="project", data=DataObj("Python"))

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            prop_tree.save2file(tmp_path, data_property="tech")

            with open(tmp_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn("React", content)
                self.assertIn("Python", content)

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_to_json_basic(self):
        """Test to_json basic functionality."""
        json_str = self.company_tree.to_json()

        # Should be valid JSON
        parsed = json.loads(json_str)
        self.assertIsInstance(parsed, dict)

        # Should contain root
        self.assertIn("CEO", parsed)

        # Should have hierarchical structure
        ceo_data = parsed["CEO"]
        self.assertIn("children", ceo_data)
        self.assertIsInstance(ceo_data["children"], list)

    def test_to_json_with_data(self):
        """Test to_json including node data."""
        json_str = self.data_tree.to_json(with_data=True)
        parsed = json.loads(json_str)

        # Should include data
        project_data = parsed["Project"]
        self.assertIn("data", project_data)
        self.assertEqual(project_data["data"]["budget"], 100000)
        self.assertEqual(project_data["data"]["status"], "active")

    def test_to_json_without_data(self):
        """Test to_json without including node data."""
        json_str = self.data_tree.to_json(with_data=False)
        parsed = json.loads(json_str)

        # Should not include data
        project_data = parsed["Project"]
        self.assertNotIn("data", project_data)

    def test_from_map_basic(self):
        """Test from_map basic functionality."""
        child_parent_dict = {"CEO": None, "CTO": "CEO", "CFO": "CEO", "VP_Eng": "CTO", "Developer": "VP_Eng"}

        tree = Tree.from_map(child_parent_dict)

        # Should create proper tree structure
        self.assertEqual(tree.root, "CEO")
        self.assertEqual(len(tree), 5)
        self.assertTrue(tree.is_ancestor("CEO", "Developer"))
        self.assertEqual(tree.parent("VP_Eng").identifier, "CTO")

    def test_from_map_with_id_func(self):
        """Test from_map with custom ID function."""
        child_parent_dict = {"ceo": None, "cto": "ceo", "developer": "cto"}

        # Convert to uppercase IDs
        tree = Tree.from_map(child_parent_dict, id_func=lambda x: x.upper())

        # Should use transformed IDs
        self.assertEqual(tree.root, "CEO")
        self.assertIn("CTO", tree)
        self.assertIn("DEVELOPER", tree)

        # Original lowercase IDs should not exist
        self.assertNotIn("ceo", tree)
        self.assertNotIn("cto", tree)

    def test_from_map_with_data_func(self):
        """Test from_map with custom data function."""
        child_parent_dict = {"root": None, "child1": "root", "child2": "root"}

        # Add data based on node name
        tree = Tree.from_map(child_parent_dict, data_func=lambda x: {"name": x, "level": x.count("child")})

        # Should have data
        root_node = tree["root"]
        self.assertIsNotNone(root_node.data)
        self.assertEqual(root_node.data["name"], "root")
        self.assertEqual(root_node.data["level"], 0)

        child_node = tree["child1"]
        self.assertEqual(child_node.data["level"], 1)

    def test_from_map_invalid_input(self):
        """Test from_map with invalid input."""
        # No root (no None parent)
        with self.assertRaises(ValueError):
            Tree.from_map({"a": "b", "b": "c"})

        # Multiple roots
        with self.assertRaises(ValueError):
            Tree.from_map({"a": None, "b": None})

    def tearDown(self):
        """Clean up test fixtures."""
        self.company_tree = None
        self.data_tree = None


if __name__ == "__main__":
    unittest.main()

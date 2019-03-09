#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import os

from treelib import Tree
from treelib.plugins import *


class DotExportCase(unittest.TestCase):
    """Test class for the export to dot format function"""

    def setUp(self):
        tree = Tree()
        tree.create_node("Hárry", "hárry")
        tree.create_node("Jane", "jane", parent="hárry")
        tree.create_node("Bill", "bill", parent="hárry")
        tree.create_node("Diane", "diane", parent="jane")
        tree.create_node("George", "george", parent="bill")
        self.tree = tree

    def read_generated_output(self, filename):
        output = codecs.open(filename, 'r', 'utf-8')
        generated = output.read()
        output.close()

        return generated

    def test_export_to_dot(self):
        export_to_dot(self.tree, 'tree.dot')
        expected = """\
digraph tree {
\t"hárry" [label="Hárry", shape=circle]
\t"bill" [label="Bill", shape=circle]
\t"jane" [label="Jane", shape=circle]
\t"george" [label="George", shape=circle]
\t"diane" [label="Diane", shape=circle]

\t"hárry" -> "jane"
\t"hárry" -> "bill"
\t"bill" -> "george"
\t"jane" -> "diane"
}"""

        self.assertTrue(os.path.isfile('tree.dot'), "The file tree.dot could not be found.")
        generated = self.read_generated_output('tree.dot')

        self.assertEqual(generated, expected, "Generated dot tree is not the expected one")
        os.remove('tree.dot')

    def test_export_to_dot_empty_tree(self):
        empty_tree = Tree()
        export_to_dot(empty_tree, 'tree.dot')

        expected = """\
digraph tree {
}"""
        self.assertTrue(os.path.isfile('tree.dot'), "The file tree.dot could not be found.")
        generated = self.read_generated_output('tree.dot')

        self.assertEqual(expected, generated, 'The generated output for an empty tree is not empty')
        os.remove('tree.dot')

    def test_unicode_filename(self):
        tree = Tree()
        tree.create_node('Node 1', 'node_1')
        export_to_dot(tree, 'ŕʩϢ.dot')

        expected = """\
digraph tree {
\t"node_1" [label="Node 1", shape=circle]
}"""
        self.assertTrue(os.path.isfile('ŕʩϢ.dot'), "The file ŕʩϢ.dot could not be found.")
        generated = self.read_generated_output('ŕʩϢ.dot')
        self.assertEqual(expected, generated, "The generated file content is not the expected one")
        os.remove('ŕʩϢ.dot')

    def test_export_with_minus_in_filename(self):
        tree = Tree()
        tree.create_node('Example Node', 'example-node')
        expected = """\
digraph tree {
\t"example-node" [label="Example Node", shape=circle]
}"""

        export_to_dot(tree, 'id_with_minus.dot')
        self.assertTrue(os.path.isfile('id_with_minus.dot'), "The file id_with_minus.dot could not be found.")
        generated = self.read_generated_output('id_with_minus.dot')
        self.assertEqual(expected, generated, "The generated file content is not the expected one")
        os.remove('id_with_minus.dot')

    def tearDown(self):
        self.tree = None

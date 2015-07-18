#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from treelib import Tree
from treelib.plugins import *
import os
import unittest

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
\thárry [label="Hárry", shape=circle]
\tbill [label="Bill", shape=circle]
\tjane [label="Jane", shape=circle]
\tgeorge [label="George", shape=circle]
\tdiane [label="Diane", shape=circle]

\thárry -> jane
\thárry -> bill
\tbill -> george
\tjane -> diane
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
\tnode_1 [label="Node 1", shape=circle]

}"""
        self.assertTrue(os.path.isfile('ŕʩϢ.dot'), "The file ŕʩϢ.dot could not be found.")
        generated = self.read_generated_output('ŕʩϢ.dot')
        self.assertEqual(expected, generated, "The generated file content is not the expected one")
        os.remove('ŕʩϢ.dot')

    def tearDown(self):
        self.tree = None

if __name__ == "__main__":
    unittest.main()
import unittest

from treelib import Node, Tree


class NonCopyableIdentifier(str):
    def __deepcopy__(self, memo):
        raise TypeError("Identifier must not be deep-copied")


class ShallowIdentifierCase(unittest.TestCase):
    def test_clone_pointers_preserves_identifier_identity(self):
        child = type("Identifier", (str,), {})("child")
        node = Node("root", "root")
        node.set_predecessor(None, "source")
        node.set_successors([child], tree_id="source")

        node.clone_pointers("source", "copy")

        self.assertIs(node.successors("copy")[0], child)
        self.assertIsNot(node.successors("source"), node.successors("copy"))
        node.successors("copy").append("other")
        self.assertEqual(node.successors("source"), [child])

    def test_clone_pointers_accepts_noncopyable_identifier(self):
        child = NonCopyableIdentifier("child")
        node = Node("root", "root")
        node.set_predecessor(None, "source")
        node.set_successors([child], tree_id="source")

        node.clone_pointers("source", "copy")

        self.assertIs(node.successors("copy")[0], child)

    def test_shallow_tree_copy_accepts_noncopyable_identifier(self):
        child = NonCopyableIdentifier("child")
        source = Tree(identifier="source")
        source.create_node("root", "root")
        source.create_node("child", child, parent="root")

        copied = Tree(source, deep=False, identifier="copy")

        self.assertIs(copied[child], source[child])
        self.assertEqual(list(copied.expand_tree()), ["root", child])
        copied.remove_node(child)
        self.assertEqual(source["root"].successors(source.identifier), [child])
        self.assertIn(child, source)

    def test_subtree_accepts_noncopyable_identifier(self):
        child = NonCopyableIdentifier("child")
        source = Tree(identifier="source")
        source.create_node("root", "root")
        source.create_node("child", child, parent="root")

        subtree = source.subtree("root", identifier="subtree")

        self.assertIs(subtree[child], source[child])
        self.assertEqual(list(subtree.expand_tree()), ["root", child])
        self.assertIs(subtree["root"].successors(subtree.identifier)[0], child)
        self.assertIsNot(
            subtree["root"].successors(subtree.identifier),
            source["root"].successors(source.identifier),
        )

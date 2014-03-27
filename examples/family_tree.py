#!/usr/bin/env python
# Example usage of treelib
#
# Author: chenxm
#
__author__ = 'chenxm'

from treelib import Tree, Node

## Create the family tree
tree = Tree()
tree.create_node("Harry", "harry")  # root node
tree.create_node("Jane", "jane", parent="harry")
tree.create_node("Bill", "bill", parent="harry")
tree.create_node("Diane", "diane", parent="jane")
tree.create_node("George", "george", parent="diane")
tree.create_node("Mary", "mary", parent="diane")
tree.create_node("Jill", "jill", parent="george")
tree.create_node("Mark", "mark", parent="jane")

sep = "-"*20 + '\n'

print(sep + "Tree of the whole family:")
tree.show(key=lambda x: x.tag, reverse=True)

print(sep + "All family members in DEPTH mode:")
for node in tree.expand_tree(mode=Tree.DEPTH):
    print(tree[node].tag)

print(sep + "All family members without Diane sub-family:")
tree.show(idhidden=False, filter=lambda x: x.identifier != 'diane')
# for node in tree.expand_tree(filter=lambda x: x.identifier != 'diane', mode=Tree.DEPTH):
#     print tree[node].tag

print(sep + "Let me introduce Diane family only:")
sub_t = tree.subtree('diane')
sub_t.show()

print(sep + "Children of Diane")
for child in tree.is_branch('diane'):
	print(tree[child].tag)

print(sep + "OOhh~ new members join Jill's family:")
new_tree = Tree()
new_tree.create_node("n1", 1)  # root node
new_tree.create_node("n2", 2, parent=1)
new_tree.create_node("n3", 3, parent=1)
tree.paste('jill', new_tree)
tree.show()

print(sep + "They leave after a while:")
tree.remove_node(1)
tree.show()

print(sep + "Now Jill moves to live with Grand-x-father Harry:")
tree.move_node('jill', 'harry')
tree.show()

print(sep + "A big family for George to send message to the oldest Harry:")
for node in tree.rsearch('george'):
    print(tree[node].tag)
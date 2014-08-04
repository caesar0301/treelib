#!/usr/bin/env python
# Example usage of treelib
#
# Author: chenxm
#
__author__ = 'chenxm'

from treelib import Tree, Node

def create_family_tree():
    ## Create the family tree
    tree = Tree()
    tree.create_node("Harry", "harry")  # root node
    tree.create_node("Jane", "jane", parent="harry")
    tree.create_node("Bill", "bill", parent="harry")
    tree.create_node("Diane", "diane", parent="jane")
    tree.create_node("Mary", "mary", parent="diane")
    tree.create_node("Mark", "mark", parent="jane")
    return tree

def example(desp):
    sep = "-"*20 + '\n'
    print(sep + desp)

if __name__ == '__main__':
    tree = create_family_tree()

    example("Tree of the whole family:")
    tree.show(key=lambda x: x.tag, reverse=True, line_type='ascii-em')

    example("All family members in DEPTH mode:")
    print(','.join([tree[node].tag for node in tree.expand_tree()]))

    example("All family members (with identifiers) but Diane's sub-family:")
    tree.show(idhidden=False, filter=lambda x: x.identifier != 'diane')

    example("Let me introduce Diane family only:")
    sub_t = tree.subtree('diane')
    sub_t.show()

    example("Children of Diane:")
    for child in tree.is_branch('diane'):
        print(tree[child].tag)

    example("New members join Jill's family:")
    new_tree = Tree()
    new_tree.create_node("n1", 1)  # root node
    new_tree.create_node("n2", 2, parent=1)
    new_tree.create_node("n3", 3, parent=1)
    tree.paste('bill', new_tree)
    tree.show()

    example("They leave after a while:")
    tree.remove_node(1)
    tree.show()

    example("Now Mary moves to live with grandfather Harry:")
    tree.move_node('mary', 'harry')
    tree.show()

    example("A big family for Mark to send message to the oldest Harry:")
    print(','.join([tree[node].tag for node in tree.rsearch('mark')]))

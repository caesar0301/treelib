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


print("#"*4 + "Breakdown of out family")
tree.show(cmp=lambda x,y: cmp(x.tag, y.tag), key=None, reverse=True)
#tree.show(key=lambda x: x.tag, reverse=False)
#tree.save2file("/home/chenxm/Desktop/tree.txt", idhidden=False)
#print('\n')


print("#"*4 + "All family members in DEPTH mode")
for node in tree.expand_tree(mode=Tree.ZIGZAG):
    print tree[node].tag
print('\n') 


print("#"*4 + "All family members without Diane sub-family")
tree.show(idhidden=False, filter=lambda x: x.identifier != 'diane')
# for node in tree.expand_tree(filter=lambda x: x.identifier != 'diane', mode=Tree.DEPTH):
#     print tree[node].tag
print('\n') 


print("#"*4 + "Let me introduce Diane family only")
sub_t = tree.subtree('diane')
sub_t.show()
print('\n') 


print("#"*4 + "Children of Diane")
print tree.is_branch('diane')
print('\n')


print("#"*4 + "OOhh~ new members enter Jill's family")
new_tree = Tree()
new_tree.create_node("n1", 1)  # root node
new_tree.create_node("n2", 2, parent=1)
new_tree.create_node("n3", 3, parent=1)
tree.paste('jill', new_tree)
tree.show()
print('\n')


print("#"*4 + "We are sorry they are gone accidently :(")
tree.remove_node(1)
tree.show()
print('\n')


print("#"*4 + "Now Jill moves to live with Grand-x-father Harry")
tree.move_node('jill', 'harry')
tree.show()
print('\n')


print("#"*4 + "A big family for George to talk to Grand-x-father Harry")
for node in tree.rsearch('george', filter=lambda x: x.identifier != 'harry'):
    print node
print('harry')
print('\n')
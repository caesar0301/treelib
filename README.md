pyTree
========

Tree Implementation in python

History
=======

Published by: Brett Alistair Kromkamp - brettkromkamp@gmail.com

Edited by: Xiaming Chen - chenxm35@gmail.com


Usage Examples
=======

Example 1: Create a tree

    tree = Tree()
    tree.create_node("Harry", "harry")  # root node
    tree.create_node("Jane", "jane", parent = "harry")
    tree.create_node("Bill", "bill", parent = "harry")
    tree.create_node("Joe", "joe", parent = "jane")
    tree.create_node("Diane", "diane", parent = "jane")
    tree.create_node("George", "george", parent = "diane")
    tree.create_node("Mary", "mary", parent = "diane")
    tree.create_node("Jill", "jill", parent = "george")
    tree.create_node("Carol", "carol", parent = "jill")
    tree.create_node("Grace", "grace", parent = "bill")
    tree.create_node("Mark", "mark", parent = "jane")
    tree.show()

Result:

    Harry [harry]
    ('+', 'Jane [jane]')
    ('++', 'Joe [joe]')
    ('++', 'Diane [diane]')
    ('+++', 'George [george]')
    ('++++', 'Jill [jill]')
    ('+++++', 'Carol [carol]')
    ('+++', 'Mary [mary]')
    ('++', 'Mark [mark]')
    ('+', 'Bill [bill]')
    ('++', 'Grace [grace]')

Example 2: expand a tree with mode being _DEPTH or _WIDTH

    for node in tree.expand_tree(mode=_DEPTH):
	print tree[node].name

Result:

    Harry
    Jane
    Joe
    Diane
    George
    Jill
    Carol
    Mary
    Mark
    Bill
    Grace

Example 3: expand tree with filter

    for node in tree.expand_tree(filter = lambda x: x != 'george', mode=_DEPTH):
	print tree[node].name

Result:

    Harry
    Jane
    Joe
    Diane
    Mary
    Mark
    Bill
    Grace

Example 4: get a subtree

    sub_t = tree.subtree('diane')
    sub_t.show()

Result:

    Diane [diane]
    ('+', 'George [george]')
    ('++', 'Jill [jill]')
    ('+++', 'Carol [carol]')
    ('+', 'Mary [mary]')

Example 5: paste a new tree to original one

    new_tree = Tree()
    new_tree.create_node("1", "1")  # root node
    new_tree.create_node("2", "2", parent = "1")
    new_tree.create_node("3", "3", parent = "1")
    tree.paste('jill', new_tree)
    tree.show()

Result:

    ['harry', 'jane', 'bill', 'joe', 'diane', 'george', 'mary', 'jill', 'carol', 'grace', 'mark', '1', '2', '3']
    Harry [harry]
    ('+', 'Jane [jane]')
    ('++', 'Joe [joe]')
    ('++', 'Diane [diane]')
    ('+++', 'George [george]')
    ('++++', 'Jill [jill]')
    ('+++++', 'Carol [carol]')
    ('+++++', '1 [1]')
    ('++++++', '2 [2]')
    ('++++++', '3 [3]')
    ('+++', 'Mary [mary]')
    ('++', 'Mark [mark]')
    ('+', 'Bill [bill]')
    ('++', 'Grace [grace]')

Example 6: temove a node from tree

    tree.remove_node('1')
    tree.show()

Result:

    Harry [harry]
    ('+', 'Jane [jane]')
    ('++', 'Joe [joe]')
    ('++', 'Diane [diane]')
    ('+++', 'George [george]')
    ('++++', 'Jill [jill]')
    ('+++++', 'Carol [carol]')
    ('+++', 'Mary [mary]')
    ('++', 'Mark [mark]')
    ('+', 'Bill [bill]')
    ('++', 'Grace [grace]')

Example 7: Move a node

    tree.move_node('jill', 'harry')
    tree.show()
	
Result:

    Harry [harry]
    ('+', 'Jane [jane]')
    ('++', 'Joe [joe]')
    ('++', 'Diane [diane]')
    ('+++', 'George [george]')
    ('+++', 'Mary [mary]')
    ('++', 'Mark [mark]')
    ('+', 'Bill [bill]')
    ('++', 'Grace [grace]')
    ('+', 'Jill [jill]')
    ('++', 'Carol [carol]')

pyTree
========

Tree Implementation in python: simple to use for you.

History
=======

Published by: Brett Alistair Kromkamp - brettkromkamp@gmail.com

Edited by: Xiaming Chen - chenxm35@gmail.com


Useful APIs
=======

Add the import declaration to use pyTree in your project:

    from pyTree import node, tree

This module `pyTree` mainly contains two classes: class `node` and class `tree`.

The class `node` defines basic properties and operations of a node like node identifier 
(the mostly used property as ID which is unique for a node in a specific tree), node name 
(readable for human), parent node, and children nodes. Some public methods are provided 
to operate with an exsiting node (e.g., `a` in the description below):

    a = Node(name, identifier=None, expanded=True) # To create a new node object
    a.identifier       # To get the ID of the node
    a.bpointer         # To get the ID of the parent node
    a.bpointer=value   # To set parent node ID (value) to a
    a.fpointer         # To get the ID list of the children (only sons) of the node
    a.fpointer=[value] # To set the children with a list of node IDs
    a.update_fpointer(identifier, mode=[_ADD, _DELETE, _INSERT])  # Update the children list with different modes

The class `tree` defines the tree-like structure based on the node structure. Public methods
are also available to make operations on the tree (e.g., `t` in the description below):

    t = Tree()        # To create a new object of tree structure
    t.root            # To give the ID of the root
    t.nodes           # To get the list of all the nodes (in the order of being added) belonging to the tree
    t.add_node(node, parent=None)  # Add a new node object to the tree and make the parent as the root by default
    t.create_node(name, identifier=None, parent=None)  # To create a new node and add it to the tree
    t.expand_tree(nid = None, mode=_DEPTH, filter = None) # To traverse the tree nodes with different modes (_DEPTH, _WIDTH); `nid` refers to the expanding point to start; `filter` refers to the function of one varible to act on the node
    t.get_index(nid)  # To get the index of the node with ID == nid
    t.get_node(nid)   # To get the object of the node with ID == nid
    t.is_branch(nid)  # To get the children (only sons) list of the node with ID == nid
    t.move_node(source, destination) # To move node (source) from its parent to another parent (destination)
    t.paste(nid, new_tree)           # To paste a new tree to an existing tree, with `nid` becoming the parent of the root of this new tree
    t.remove_node(identifier)        # To remove the node (with all its successor) from the tree
    t.rsearch(nid, filter=None)      # To search the tree from `nid` to the root along links reversedly
    t.show(nid = None, level=_ROOT)  # To print the tree structure in hierarchy style; `nid` refers to the expanding point to start; `level` refers to the node level in the tree (root as level 0)
    t.subtree(nid)    # To return a shaddow copy of the subtree with `nid` being the root; "shaddow" here means all the nodes of the subtree are shared between the original tree and it

Basic Usage
=======

Example 1: Create a tree

    tree = Tree()
    tree.create_node("Harry", "harry")  # root node
    tree.create_node("Jane", "jane", parent = "harry")
    tree.create_node("Bill", "bill", parent = "harry")
    tree.create_node("Diane", "diane", parent = "jane")
    tree.create_node("George", "george", parent = "diane")
    tree.create_node("Mary", "mary", parent = "diane")
    tree.create_node("Jill", "jill", parent = "george")
    tree.create_node("Mark", "mark", parent = "jane")
    tree.show()

Result:

    Harry[harry]
    |___ Jane[jane]
    |    |___ Diane[diane]
    |         |___ George[george]
    |              |___ Jill[jill]
    |         |___ Mary[mary]
    |    |___ Mark[mark]
    |___ Bill[bill]

Example 2: expand a tree with mode being _DEPTH or _WIDTH

    for node in tree.expand_tree(mode=_DEPTH):
	   print tree[node].name

Result:

    Harry
    Jane
    Diane
    George
    Jill
    Mary
    Mark
    Bill

Example 3: expand tree with filter

    for node in tree.expand_tree(filter = lambda x: x != 'george', mode=_DEPTH):
	   print tree[node].name

Result:

    Harry
    Jane
    Mark
    Bill

Example 4: get a subtree

    sub_t = tree.subtree('diane')
    sub_t.show()

Result:

    Diane[diane]
    |___ George[george]
    |    |___ Jill[jill]
    |___ Mary[mary]

Example 5: paste a new tree to original one

    new_tree = Tree()
    new_tree.create_node("n1", "1")  # root node
    new_tree.create_node("n2", "2", parent = "1")
    new_tree.create_node("n3", "3", parent = "1")
    tree.paste('jill', new_tree)
    tree.show()

Result:

    Harry[harry]
    |___ Jane[jane]
    |    |___ Diane[diane]
    |         |___ George[george]
    |              |___ Jill[jill]
    |                   |___ n1[1]
    |                        |___ n2[2]
    |                        |___ n3[3]
    |         |___ Mary[mary]
    |    |___ Mark[mark]
    |___ Bill[bill]

Example 6: remove the existing node from the tree

    tree.remove_node('1')
    tree.show()

Result:

    As the result of example 1

Example 7: Move a node

    tree.move_node('jill', 'harry')
    tree.show()
	
Result:

    Harry[harry]
    |___ Jane[jane]
    |    |___ Diane[diane]
    |         |___ George[george]
    |         |___ Mary[mary]
    |    |___ Mark[mark]
    |___ Bill[bill]
    |___ Jill[jill]


Advanced Usage
=======

You can also inherit and modify the behaviors of the tree structure to meet your need easily and conveniently.
For example, to define a tree structure with data payload for each node, you can program like the way below:

    import pyTree

    class myNode(pyTree.node):
        def __init__(self, payload):
            self.data = payload
    ...
    new_node = myNode("1234567890")

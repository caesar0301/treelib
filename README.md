treelib 
========

(previous pyTree to avoid conflict on PyPI)
--------

Tree Implementation in python: simple to use for you.

Contributors
=======

Brett Alistair Kromkamp - brettkromkamp@gmail.com

Basic framework finished.

Xiaming Chen - chenxm35@gmail.com

For reasearch utility, I finish main parts and make the library freely public.

Holger Bast - holgerbast@gmx.de

Replace list with dict for nodes indexing and improve the performance to a
large extend.


Useful APIs
=======

Add the import declaration to use `treelib` in your project:

    from treelib import Node, Tree

This module `treelib` mainly contains two data structures: `Node` and `Tree`.

The structure `Node` defines basic properties such as node identifier 
(unique ID in the environment of a tree), node name (readable for human), 
parent node, children nodes etc., and some public operations on a node. 
(e.g., `a` in the description below):

    # To create a new node object.

    a = Node([tag[, identifier[, expanded]]])
    
    
    # To get the ID of the node
    
    a.identifier
    
    
    # To get the ID of the parent node
    
    a.bpointer
    
    
    # To set parent node ID (value) to a
    
    a.bpointer=value
    
    
    # To get the ID list of the children (only sons) of the node
    
    a.fpointer
    
    
    # To set the children with a list of node IDs
    
    a.fpointer=[value]
    
    
    # Update the children list with different modes
    
    a.update_fpointer(identifier, mode=[Node.ADD, Node.DELETE, Node.INSERT])

The class `tree` defines the tree-like structure based on the node structure. Public methods
are also available to make operations on the tree (e.g., `t` in the description below):

    # To create a new object of tree structure
    
    t = Tree()
    
    
    # To give the ID of the root
    
    t.root 
    
    
    # To get the list of all the nodes (in arbitrary order) belonging to the tree
    
    t.nodes.values()
    
    
    # Add a new node object to the tree and make the parent as the root by default
    
    t.add_node(node[, parent])
    
    
    # To create a new node and add it to the tree
    
    t.create_node(name[,identifier[,parent]])
    
    
    # To traverse the tree nodes with different modes (Tree.DEPTH, Tree.WIDTH);
    # NOTE:
    # `nid` refers to the expanding point to start;
    # `mode` refers to the search mode;
    # `filter` refers to the function of one varible to act on the **node object**;
    # `cmp`, `key`, `reverse` are present to sort **node objects** in the same level.
    
    t.expand_tree([nid[,mode[,filter[,cmp[,key[,reverse]]]]]]) 
    
    
    # To get the object of the node with ID of nid
    # An alternative way is using '[]' operation on the tree.
    # But small difference exists between them:
    # the get_node() will return None if nid is absent, whereas '[]' will raise KeyError.
    
    t.get_node(nid)
    
    
    # To get the children (only sons) list of the node with ID == nid.
    
    t.is_branch(nid)
    
    
    # To move node (source) from its parent to another parent (destination).
    
    t.move_node(source, destination)
    
    
    # To paste a new tree to an existing tree, with `nid` becoming the parent of the root of this new tree.
    
    t.paste(nid, new_tree) 
    
    
    # To remove the node (with all its successor) from the tree.
    
    t.remove_node(identifier)
 
 
    # To search the tree from `nid` to the root along links reversedly
    # Note: `filter` refers to the function of one varible to act on the **node object**.
    
    t.rsearch(nid[,filter]) 
    
    
    # To print the tree structure in hierarchy style;
    # Note:
    # `nid` refers to the expanding point to start;
    # `level` refers to the node level in the tree (root as level 0);
    # `idhidden` refers to hiding the node ID when priting;
    # `filter` refers to the function of one varible to act on the **node object**;
    # `cmp`, `key`, `reverse` are present to sort **node objects** in the same level.
    
    t.show([nid[,level[,idhidden[,filter[,cmp[,key[,reverse]]]]]]])


    # Save the tree into file for offline analysis.

    t.save2file(filename[,nid[,level[,idhidden[,filter[,cmp[,key[,reverse]]]]]]])
    
    
    # To return a shaddow copy of the subtree with `nid` being the root; "shaddow" here means all the nodes of the subtree are shared between the original tree and it
    
    t.subtree(nid)
    

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

Example 2: expand a tree with mode being Tree.DEPTH or Tree.WIDTH

    for node in tree.expand_tree(mode=Tree.DEPTH):
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

    for node in tree.expand_tree(filter = lambda x: x.identifier != 'george'):
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

    import treelib

    class myNode(treelib.node):
        def __init__(self, payload):
            self.data = payload
    ...
    new_node = myNode("1234567890")

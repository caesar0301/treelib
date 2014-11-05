treelib
--------

Tree Implementation in python: simple to use for you.

[![Build Status](https://travis-ci.org/caesar0301/pyTree.png?branch=master)](https://travis-ci.org/caesar0301/pyTree)



Install from PyPI
---------

    sudo pip install -U treelib  (OR)      
    sudo easy_install -U treelib

    

Basic Usage
----------

**Example 1**: Create a tree

    tree = Tree()
    tree.create_node("Harry", "harry")  # root node
    tree.create_node("Jane", "jane", parent="harry")
    tree.create_node("Bill", "bill", parent="harry")
    tree.create_node("Diane", "diane", parent="jane")
    tree.create_node("Mary", "mary", parent="diane")
    tree.create_node("Mark", "mark", parent="jane")
    tree.show()

*Result*:

    Harry
    ├── Jane
    │   ├── Mark
    │   └── Diane
    │       └── Mary
    └── Bill

**Example 2**: expand a tree with specific mode (Tree.DEPTH [default], Tree.WIDTH, Tree.ZIGZAG)

    print(','.join([tree[node].tag for node in \
                    tree.expand_tree(mode=Tree.DEPTH)]))

*Result*:

    Harry,Bill,Jane,Diane,Mary,Mark

**Example 3**: expand tree with filter

    print(','.join([tree[node].tag for node in \
                    tree.expand_tree(filter = lambda x: \
                    x.identifier != 'diane')]))

*Result*:

    Harry,Bill,Jane,Mark

**Example 4**: get a subtree

    sub_t = tree.subtree('diane')
    sub_t.show()

*Result*:

    Diane
    └── Mary

**Example 5**: paste a new tree to original one

    new_tree = Tree()
    new_tree.create_node("n1", 1)  # root node
    new_tree.create_node("n2", 2, parent=1)
    new_tree.create_node("n3", 3, parent=1)
    tree.paste('bill', new_tree)
    tree.show()
    
*Result*:

    Harry
    ├── Bill
    │   └── n1
    │       ├── n2
    │       └── n3
    └── Jane
        ├── Diane
        │   └── Mary
        └── Mark

**Example 6**: remove the existing node from the tree

    tree.remove_node('1')
    tree.show()

*Result*:

    As the result of **Example 1**.

**Example 7**: Move a node to another parent.

    tree.move_node('mary', 'harry')
    tree.show()

*Result*:

    Harry
    ├── Bill
    ├── Jane
    │   ├── Diane
    │   └── Mark
    └── Mary

**Example 8**: Get the height of the tree

    tree.depth()

**Example 9**: Get the level of a node

    node = tree.get_node("bill")
    tree.depth(node)
    
**Example 10**: Print or dump tree structure. You now have three ways to output
your tree data, i.e., stdout with `show()`, plain text file with `save2file()`,
and json string with `to_json()`. The former two use the same backend to generate
a string of tree structure in a text graph. After the version 1.2.7a, you can
also spicify the `line_type` parameter (now supporting 'ascii' [default],
'ascii-ex', 'ascii-exr', 'ascii-em', 'ascii-emv', 'ascii-emh') to the change graphical form.
For example, the same tree in example 1 can be printed with 'ascii-em' like

    Harry
    ╠══ Jane
    ║   ╠══ Mark
    ║   ╚══ Diane
    ║       ╚══ Mary
    ╚══ Bill
    
In the json form, `to_json()` takes optional parameter `with_data` to trigger if
the data field is appended into json string. For example,

    print tree.to_json(with_data=True) #output
    {"Harry": {"data": null, "children": [{"Bill": {"data": null, "children": [{"George": {"data": null}}]}}, {"Jane": {"data": null, "children": [{"Diane": {"data": null}}]}}]}}


Advanced Usage
---------

Sometimes, you need trees to store your own data.
The newsest version of `treelib` supports `.data` variable to store whatever you want.
For example, to define a flower tree with your own data:

    class Flower(object):
        def __init__(self, color):
            self.color = color
            
You can create a flower tree now:
    
    ftree = Tree()
    ftree.create_node("Root", "root")
    ftree.create_node("F1", "f1", parent='root', data=Flower("white"))
    ftree.create_node("F2", "f2", parent='root', data=Flower("red"))

Before version 1.2.5, you should inherit and modify the behaviors of the tree. For flower example,

    class FlowerNode(treelib.Node):
        def __init__(self, color):
            self.color = color

    # create a new node
    fnode = FlowerNode("white")


  
Useful APIs
-----------

Add the import declaration to use `treelib` in your project:

    from treelib import Node, Tree

This module `treelib` mainly contains two data structures: `Node` and `Tree`.

The structure `Node` defines basic properties such as node identifier 
(unique ID in the environment of a tree), node tag (readable name for human), 
parent node, children nodes etc., and some public operations on a node. 
(e.g., `a` in the description below):

    # To create a new node object.
    a = Node([tag[, identifier[, expanded]]])
    
    # To get or set the ID of the node
    a.identifier [=nid]
    
    # To get or set the ID of a's parent node
    a.bpointer [=value]
    a.update_bpointer(nid) # for set only
    
    # As a getting operator, ID list of a's SON nodes is obtained.
    # As a setting operator, the value can be list, set, or dict.
    # For list or set, it is converted to a list type by the packeage;
    # For dict, the keys are treated as the node IDs
    a.fpointer [=value]

    # Update the children list with different modes
    a.update_fpointer(identifier, mode=[Node.ADD, Node.DELETE, Node.INSERT])

    # Check if it's a leaf node
    a.is_leaf()


The class `Tree` defines the tree-like structure based on the node structure.
Public methods are also available to make operations on the tree, e.g. a Tree object `t`:

    # Create a new object of tree structure
    t = Tree()
    
    # Get or set the ID of the root
    t.root [=nid]

    # Get the number of nodes in this tree
    t.size()

    # Get node level in this tree.
    # More advancedly, you can calculate the level by skiping some unwanted nodes.
    t.level(nid[,filter])

    # Get maximum depth of the tree, which equals to `t.level(t.root)`.
    t.depth()

    # Check if the tree contains given node
    t.contains(nid)

    # Get the list of all the nodes randomly belonging to this tree
    t.all_nodes()

    # Obtain node's parent (Node instance)
    # Return None if the parent is None or does not exist in the tree
    t.parent(nid)

    # Get the children list of the node (nid).
    t.children(nid) # return node instances
    t.is_branch(nid) # return node IDs

    # Get all the siblings of given nid.
    t.siblings(nid)

    # Get leaves of give root. If `nid` is not given, leaves of the maximum level are returned.
    t.leaves([nid])

    # Add a new node object to the tree and make the parent as the root by default
    t.add_node(node[,parent])
    
    # Create a new node and add it to this tree
    t.create_node([tag[,identifier[,parent[,data]]]])
    
    # Get the object of the node with ID of nid
    # An alternative way is using '[]' operation on the tree.
    # But small difference exists between them:
    # the get_node() will return None if nid is absent, whereas '[]' will raise KeyError.
    t.get_node(nid)
    
    # Move node (source) from its parent to another parent (destination).
    t.move_node(source, destination)
    
    # Paste a new tree to an existing tree, with `nid` becoming the parent of the root of this new tree.
    t.paste(nid, new_tree) 
    
    # Remove a node and free the memory along with its successors.
    t.remove_node(nid)

    # Remove a node and link its children to its parent (root is not allowed)
    t.link_past_node(nid)

    # Traverse the tree nodes with different modes; NOTE:
    # `nid` refers to the expanding point to start;
    # `mode` refers to the search mode (Tree.DEPTH, Tree.WIDTH);
    # `filter` refers to the function of one varible to act on the **node object**;
    # `key`, `reverse` are present to sort **node objects** in the same level.
    t.expand_tree([nid[,mode[,filter[,key[,reverse]]]]]]) 
 
    # Search the tree from `nid` to the root along links reversedly
    # Note: `filter` refers to the function of one varible to act on the **node object**.
    t.rsearch(nid[,filter]) 
    
    # Print the tree structure in hierarchy style;
    # Note:
    # `nid` refers to the expanding point to start;
    # `level` refers to the node level in the tree (root as level 0);
    # `idhidden` refers to hiding the node ID when priting;
    # `filter` refers to the function of one varible to act on the **node object**;
    # `key`, `reverse` are present to sort **node objects** in the same level.
    t.show([nid[,level[,idhidden[,filter[,key[,reverse[,line_type]]]]]]])

    # Return a soft copy of the subtree with `nid` being the root; The softness 
    # means all the nodes are shared between subtree and the original.
    t.subtree(nid)

    # Return a subtree with `nid` being the root, and
    # remove all nodes in the subtree from the original one
    t.remove_subtree(nid)

    # Save the tree into file for offline analysis.
    t.save2file(filename[,nid[,level[,idhidden[,filter[,key[,reverse[,line_type]]]]]]]])
    
    # To format the tree in a json format.
    t.to_json([with_data])
    
    
Contributors
---------

* Brett Alistair Kromkamp (brettkromkamp@gmail.com): 
  Basic framework finished.

* Xiaming Chen (chenxm35@gmail.com): For reasearch utility, 
I finish main parts and make the library freely public.

* Holger Bast (holgerbast@gmx.de): Replaces list with dict 
for nodes indexing and improves the performance to a
large extend.

* Ilya Kuprik (ilya-spy@ynadex.ru): Added ZIGZAG tree-walk mode to
function tree_expand()

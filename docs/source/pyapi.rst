Useful APIs
============

.. module:: treelib
    :synopsis: Tree data structure in Python.

This `treelib` is a simple module containing only two classes: ``Node`` and
``Tree``. Tree is a self-contained structure with some nodes and connected by
branches. One tree has and only has one root, while a node (except root) has
several children and merely one parent.

*Note:* To solve the string compatibility between Python 2.x and 3.x, treelib
follows the way of porting Python 3.x to 2/3. That means, all strings are
manipulated as unicode and you do not need `u''` prefix anymore. The impacted
functions include `str()`, `show()` and `save2file()` routines. But if your
data contains non-ascii characters and Python 2.x is used, you have to trigger
the compatibility by declaring `unicode_literals` in the code:

.. code-block:: sh

    >>> from __future__ import unicode_literals


:class:`Node` Objects
---------------------

.. class:: Node([tag[, identifier[, expanded]]])

   A :class:`Node` object contains basic properties such as node identifier,
   node tag, parent node, children nodes etc., and some operations for a node.


Class attributes are:

.. attribute:: Node.ADD

    Addition mode for method `update_fpointer()`.

.. attribute:: Node.DELETE

    Deletion mode for method `update_fpointer()`.

.. attribute:: Node.INSERT

    Behave in the same way with Node.ADD since version 1.1.


.. currentmodule:: node

Instance attributes:

.. attribute:: identifier

    The unique ID of a node within the scope of a tree. This attribute can be
    accessed and modified with ``.`` and ``=`` operator respectively.

.. attribute:: tag

    The readable node name for human. This attribute can be accessed and
    modified with ``.`` and ``=`` operator respectively.

.. attribute:: bpointer

    The parent ID of a node. This attribute can be
    accessed and modified with ``.`` and ``=`` operator respectively.

.. attribute:: fpointer

    With a getting operator, a list of IDs of node's children is obtained. With
    a setting operator, the value can be list, set, or dict. For list or set,
    it is converted to a list type by the package; for dict, the keys are
    treated as the node IDs.


Instance methods:

.. method:: is_leaf ()

    Check if the node has children. Return False if the ``fpointer`` is empty
    or None.

.. method:: is_root ()

    Check if the node is the root of present tree.

.. method:: update_bpointer (nid)

    Set the parent (indicated by the ``nid`` parameter) of a node.

.. method:: update_fpointer (nid, mode=Node.ADD)

    Update the children list with different modes: addition (Node.ADD or
    Node.INSERT) and deletion (Node.DELETE).


:mod:`Tree` Objects
---------------------

.. class:: Tree(tree=None, deep=False)

    The :class:`Tree` object defines the tree-like structure based on
    :class:`Node` objects. A new tree can be created from scratch without any
    parameter or a shallow/deep copy of another tree. When ``deep=True``, a
    deepcopy operation is performed on feeding ``tree`` parameter and *more
    memory is required to create the tree*.


Class attributes are:

.. attribute:: Tree.ROOT

    Default value for the ``level`` parameter in tree's methods.

.. attribute:: Tree.DEPTH

    The depth-first search mode for tree.

.. attribute:: Tree.WIDTH

    The width-first search mode for tree.

.. attribute:: Tree.ZIGZAG

    The `ZIGZAG search
    <http://en.wikipedia.org/wiki/Tree_%28data_structure%29>`_ mode for tree.


.. currentmodule:: tree

Instance attributes:

.. attribute:: root

    Get or set the ID of the root.  This attribute can be accessed and modified
    with ``.`` and ``=`` operator respectively.


Instance methods:

.. method:: size ()

    Get the number of nodes in this tree.

.. method:: contains (nid)

    Check if the tree contains given node.

.. method:: parent (nid)

    Obtain specific node's parent (Node instance). Return None if the parent is
    None or does not exist in the tree.

.. method:: all_nodes ()

    Get the list of all the nodes randomly belonging to this tree.

.. method:: depth ()

    Get depth of the tree.

.. method:: leaves (nid)

    Get leaves from given node.

.. method:: add_node(node[, parent])

    Add a new node object to the tree and make the parent as the root by
    default.

.. method:: create_node(tag[, identifier[, parent]])

    Create a new node and add it to this tree.

.. method:: expand_tree([nid[, mode[, filter[, key[, reverse]]]]]])

    Traverse the tree nodes with different modes. ``nid`` refers to the
    expanding point to start; ``mode`` refers to the search mode (Tree.DEPTH,
    Tree.WIDTH); ``filter`` refers to the function of one variable to act on
    the :class:`Node` object; ``key``, ``reverse`` are present to sort
    :class:Node objects at the same level.

.. method:: get_node(nid)

    Get the object of the node with ID of ``nid`` An alternative way is using
    '[]' operation on the tree. But small difference exists between them: the
    get_node() will return None if ``nid`` is absent, whereas '[]' will raise
    ``KeyError``.

.. method:: is_branch(nid)

    Get the children (only sons) list of the node with ID == nid.

.. method:: siblings(nid)

    Get all the siblings of given nid.

.. method:: move_node(source, destination)

    Move node (source) from its parent to another parent (destination).

.. method:: paste(nid, new_tree)

    Paste a new tree to an existing tree, with ``nid`` becoming the parent of the
    root of this new tree.

.. method:: remove_node(nid)

    Remove a node and free the memory along with its successors.

.. method:: link_past_node(nid)

    Remove a node and link its children to its parent (root is not allowed).

.. method:: rsearch(nid[, filter])

    Search the tree from ``nid`` to the root along links reservedly. Parameter
    ``filter`` refers to the function of one variable to act on the
    :class:`Node` object.

.. method:: show([nid[, level[, idhidden[, filter[, key[, reverse[, line_type]]]]]]]])

    Print the tree structure in hierarchy style. ``nid`` refers to the
    expanding point to start; ``level`` refers to the node level in the tree
    (root as level 0); ``idhidden`` refers to hiding the node ID when printing;
    ``filter`` refers to the function of one variable to act on the
    :class:`Node` object; ``key``, ``reverse`` are present to sort
    :class:`Node` object in the same level.

    You have three ways to output your tree data, i.e., stdout with ``show()``,
    plain text file with ``save2file()``, and json string with ``to_json()``. The
    former two use the same backend to generate a string of tree structure in a
    text graph.

    *Version >= 1.2.7a*: you can also spicify the ``line_type`` parameter (now
     supporting 'ascii' [default], 'ascii-ex', 'ascii-exr', 'ascii-em',
     'ascii-emv', 'ascii-emh') to the change graphical form.

.. method:: subtree(nid)

    Return a soft copy of the subtree with ``nid`` being the root. The softness
    means all the nodes are shared between subtree and the original.

.. method:: remove_subtree(nid)

    Return a subtree with ``nid`` being the root, and remove all nodes in the
    subtree from the original one.

.. method:: save2file(filename[, nid[, level[, idhidden[, filter[, key[, reverse]]]]]]])

    Save the tree into file for offline analysis.

.. method:: to_json()

    To format the tree in a JSON format.

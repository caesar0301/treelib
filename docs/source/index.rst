.. treelib documentation master file, created by
   sphinx-quickstart on Thu Dec 20 16:30:18 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to treelib's documentation!
***********************************

.. toctree::
   :maxdepth: 2
   :caption: Contents:

🌳 Introduction
===============

`Tree <http://en.wikipedia.org/wiki/Tree_%28data_structure%29>`_ is a fundamental data structure in computer science, essential for organizing hierarchical data efficiently. `treelib <https://github.com/caesar0301/treelib>`_ provides a comprehensive, high-performance implementation of tree data structures in Python.

**Why choose treelib?**

* 🚀 **Blazing Fast**: O(1) node lookup and access operations
* 🎨 **Rich Visualization**: Beautiful tree display with multiple formatting options
* 🔧 **Flexible Operations**: Comprehensive tree manipulation (add, move, copy, delete)
* 📊 **Export Ready**: JSON, dictionary, and GraphViz export capabilities
* 🔍 **Advanced Search**: Powerful filtering and traversal algorithms
* 💾 **Memory Efficient**: Optimized for both small and large tree structures

**Perfect for:**

* File system representations and directory scanning
* Organizational charts and hierarchical structures
* Decision trees and machine learning models
* Menu systems and navigation structures
* Category taxonomies and classification systems
* Family trees and genealogical data
* Abstract syntax trees for parsers
* Game tree structures and AI algorithms

📦 Installation
===============

Install treelib using pip for the latest stable version:

.. code-block:: bash

    pip install treelib

Or install from source for the latest development features:

.. code-block:: bash

    git clone https://github.com/caesar0301/treelib.git
    cd treelib
    pip install poetry
    poetry install

**System Requirements:**
    * Python 3.7+

🚀 Quick Start Guide
====================

Ready to build your first tree? Let's start with a simple example:

Basic Tree Creation
-------------------

.. code-block:: python

    from treelib import Tree

    # Create a new tree
    tree = Tree()

    # Add root node
    tree.create_node("Company", "company")

    # Add departments
    tree.create_node("Engineering", "eng", parent="company")
    tree.create_node("Sales", "sales", parent="company")
    tree.create_node("HR", "hr", parent="company")

    # Add team members
    tree.create_node("Alice (CTO)", "alice", parent="eng")
    tree.create_node("Bob (Developer)", "bob", parent="eng")
    tree.create_node("Carol (Sales Manager)", "carol", parent="sales")
    tree.create_node("Dave (HR Manager)", "dave", parent="hr")

    # Display the tree
    tree.show()

Output:

.. code-block:: text

    Company
    ├── Engineering
    │   ├── Alice (CTO)
    │   └── Bob (Developer)
    ├── Sales
    │   └── Carol (Sales Manager)
    └── HR
        └── Dave (HR Manager)

Working with Custom Data
------------------------

Store rich data in your tree nodes:

.. code-block:: python

    from treelib import Tree

    # Employee data structure
    class Employee:
        def __init__(self, name, role, salary):
            self.name = name
            self.role = role
            self.salary = salary

        def __str__(self):
            return f"{self.name} ({self.role})"

    # Create tree with custom data
    tree = Tree()
    tree.create_node("Company", "company")

    # Add employees with rich data
    tree.create_node("Alice", "alice", parent="company",
                    data=Employee("Alice Johnson", "CTO", 150000))
    tree.create_node("Bob", "bob", parent="alice",
                    data=Employee("Bob Smith", "Senior Developer", 120000))

    # Display with custom data property
    tree.show(data_property="role")

Output:

.. code-block:: text

    Company
    ├── CTO
    └── Senior Developer

🎯 Core Concepts
================

Understanding Nodes
-------------------

**Nodes** are the building blocks of trees. Each node contains:

* **Identifier**: Unique ID for referencing (auto-generated if not provided)
* **Tag**: Human-readable label for display
* **Data**: Optional custom payload (any Python object)
* **Parent/Children**: Relationships to other nodes

.. code-block:: python

    from treelib import Node, Tree

    # Create nodes with different configurations
    node1 = Node("Simple Node", "n1")
    node2 = Node("Rich Node", "n2", data={"type": "folder", "size": 1024})
    node3 = Node("Hidden Node", "n3", expanded=False)  # Initially collapsed

Understanding Trees
-------------------

**Trees** manage collections of nodes with these key properties:

* **Single Root**: Every tree has exactly one root node (or is empty)
* **Hierarchy**: Each non-root node has exactly one parent
* **Unique IDs**: Node identifiers must be unique within the tree
* **Efficient Access**: O(1) lookup time for any node

.. code-block:: python

    tree = Tree()

    # Tree properties
    print(f"Tree size: {tree.size()}")           # Number of nodes
    print(f"Tree depth: {tree.depth()}")         # Maximum depth
    print(f"Root node: {tree.root}")             # Root identifier
    print(f"Is empty: {len(tree) == 0}")         # Empty check

📚 Comprehensive API Guide
==========================

Tree Creation and Basic Operations
----------------------------------

**Creating Trees**

.. code-block:: python

    # Empty tree
    tree1 = Tree()

    # Copy existing tree (shallow)
    tree2 = Tree(tree1)

    # Deep copy with independent data
    tree3 = Tree(tree1, deep=True)

    # Tree with custom identifier
    tree4 = Tree(identifier="my_tree")

**Adding Nodes**

.. code-block:: python

    # Basic node creation
    tree.create_node("Root", "root")
    tree.create_node("Child", "child", parent="root")

    # Node with custom data
    tree.create_node("Data Node", "data", parent="root",
                    data={"key": "value"})

    # Pre-created node
    node = Node("Pre-made", "premade")
    tree.add_node(node, parent="root")

Tree Navigation and Search
--------------------------

**Accessing Nodes**

.. code-block:: python

    # Direct access (raises KeyError if not found)
    node = tree["node_id"]

    # Safe access (returns None if not found)
    node = tree.get_node("node_id")

    # Check if node exists
    if "node_id" in tree:
        print("Node exists!")

**Tree Traversal**

.. code-block:: python

    # Depth-first traversal (default)
    for node_id in tree.expand_tree():
        print(f"Visiting: {tree[node_id].tag}")

    # Breadth-first traversal
    for node_id in tree.expand_tree(mode=Tree.WIDTH):
        print(f"Level order: {tree[node_id].tag}")

    # ZigZag traversal
    for node_id in tree.expand_tree(mode=Tree.ZIGZAG):
        print(f"ZigZag: {tree[node_id].tag}")

    # Filtered traversal
    for node_id in tree.expand_tree(filter=lambda x: x.tag.startswith("A")):
        print(f"Starts with A: {tree[node_id].tag}")

**Finding Relationships**

.. code-block:: python

    # Get parent node
    parent = tree.parent("child_id")

    # Get all children
    children = tree.children("parent_id")

    # Get siblings
    siblings = tree.siblings("node_id")

    # Get path to root
    path = list(tree.rsearch("node_id"))
    path_names = [tree[nid].tag for nid in path]

    # Check if node is leaf (no children)
    is_leaf = tree["node_id"].is_leaf(tree.identifier)

    # Check if node is root
    is_root = tree["node_id"].is_root(tree.identifier)

Tree Modification
-----------------

**Moving and Reorganizing**

.. code-block:: python

    # Move node to new parent
    tree.move_node("source_id", "new_parent_id")

    # Remove node and all descendants
    removed_count = tree.remove_node("node_id")

    # Link past a node (remove node but keep children)
    tree.link_past_node("node_id")

**Copying and Merging**

.. code-block:: python

    # Create subtree
    subtree = tree.subtree("root_of_subtree")

    # Remove subtree (returns removed tree)
    removed_tree = tree.remove_subtree("node_id")

    # Paste another tree
    tree.paste("target_node", another_tree)

    # Merge another tree (paste children only)
    tree.merge("target_node", another_tree)

Advanced Features
-----------------

**Filtering and Analysis**

.. code-block:: python

    # Filter nodes by condition
    large_files = tree.filter_nodes(lambda node:
        hasattr(node.data, 'size') and node.data.size > 1000)

    # Get all leaf nodes
    leaves = tree.leaves()

    # Get nodes at specific level
    level_2_nodes = [node for node in tree.all_nodes()
                    if tree.level(node.identifier) == 2]

    # Get all paths from root to leaves
    all_paths = tree.paths_to_leaves()

**Tree Metrics**

.. code-block:: python

    # Basic metrics
    total_nodes = tree.size()
    max_depth = tree.depth()

    # Level-specific metrics
    nodes_at_level_2 = tree.size(level=2)

    # Custom analysis
    def analyze_tree(tree):
        analysis = {
            'total_nodes': tree.size(),
            'depth': tree.depth(),
            'leaves': len(tree.leaves()),
            'internal_nodes': tree.size() - len(tree.leaves()),
            'branching_factor': sum(len(tree.children(node.identifier))
                                  for node in tree.all_nodes()) / tree.size()
        }
        return analysis

🎨 Visualization and Display
============================

Rich Display Options
--------------------

.. code-block:: python

    # Basic display
    tree.show()

    # Custom line styles
    tree.show(line_type="ascii-em")     # Double lines
    tree.show(line_type="ascii-emv")    # Mixed vertical
    tree.show(line_type="ascii")        # Simple ASCII

    # Show node IDs
    tree.show(idhidden=False)

    # Sort nodes at each level
    tree.show(key=lambda x: x.tag, reverse=True)

    # Display custom data property
    tree.show(data_property="name")

Available Line Styles:

.. code-block:: text

    ascii:        |-- Child
    ascii-ex:     ├── Child  (default)
    ascii-exr:    ├── Child  (rounded)
    ascii-em:     ╠══ Child  (double)
    ascii-emv:    ╟── Child  (mixed vertical)
    ascii-emh:    ╞══ Child  (mixed horizontal)

Conditional Display
-------------------

.. code-block:: python

    # Hide specific branches
    tree.show(filter=lambda x: x.identifier != "hidden_branch")

    # Show only certain node types
    tree.show(filter=lambda x: hasattr(x.data, 'type') and x.data.type == "folder")

    # Custom formatting function
    def custom_filter(node):
        # Show only nodes with tags starting with uppercase
        return node.tag[0].isupper()

    tree.show(filter=custom_filter)

💾 Export and Persistence
=========================

JSON Export/Import
------------------

.. code-block:: python

    # Export to JSON string
    json_string = tree.to_json()

    # Export with data included
    json_with_data = tree.to_json(with_data=True)

    # Pretty printed JSON
    import json
    formatted_json = json.dumps(json.loads(tree.to_json()), indent=2)

Dictionary Conversion
--------------------

.. code-block:: python

    # Convert to dictionary
    tree_dict = tree.to_dict()

    # Include data in dictionary
    tree_dict = tree.to_dict(with_data=True)

    # Custom sorting
    tree_dict = tree.to_dict(sort=True, reverse=True)

File Operations
---------------

.. code-block:: python

    # Save tree structure to file
    tree.save2file("tree_structure.txt")

    # Custom formatting when saving
    tree.save2file("tree.txt", line_type="ascii-em", data_property="name")

GraphViz Export
---------------

.. code-block:: python

    # Export to DOT format for GraphViz
    tree.to_graphviz("tree.dot")

    # Custom node shapes
    tree.to_graphviz("tree.dot", shape="box")

    # Directed graph
    tree.to_graphviz("tree.dot", graph="digraph")

🏗️ Real-World Examples
======================

File System Scanner
-------------------

Build a directory tree scanner:

.. code-block:: python

    import os
    from treelib import Tree

    def scan_directory(path, tree=None, parent=None, max_depth=3, current_depth=0):
        """Scan directory and build tree structure."""
        if tree is None:
            tree = Tree()
            tree.create_node(os.path.basename(path) or path, path)
            parent = path

        if current_depth >= max_depth:
            return tree

        try:
            for item in sorted(os.listdir(path)):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    tree.create_node(f"📁 {item}", item_path, parent=parent)
                    scan_directory(item_path, tree, item_path, max_depth, current_depth + 1)
                else:
                    size = os.path.getsize(item_path)
                    tree.create_node(f"📄 {item} ({size} bytes)", item_path, parent=parent)
        except PermissionError:
            pass

        return tree

    # Usage
    file_tree = scan_directory("/path/to/directory", max_depth=2)
    file_tree.show()

Organization Chart
------------------

Create a company organizational structure:

.. code-block:: python

    from treelib import Tree

    class Employee:
        def __init__(self, name, title, department, email=None):
            self.name = name
            self.title = title
            self.department = department
            self.email = email

        def __str__(self):
            return f"{self.name} - {self.title}"

    def build_org_chart():
        org = Tree()

        # CEO
        org.create_node("CEO", "ceo",
                       data=Employee("John Smith", "Chief Executive Officer", "Executive"))

        # VPs
        org.create_node("VP Engineering", "vp_eng", parent="ceo",
                       data=Employee("Sarah Johnson", "VP Engineering", "Engineering"))
        org.create_node("VP Sales", "vp_sales", parent="ceo",
                       data=Employee("Mike Wilson", "VP Sales", "Sales"))

        # Engineering Team
        org.create_node("Engineering Manager", "eng_mgr", parent="vp_eng",
                       data=Employee("Alice Brown", "Engineering Manager", "Engineering"))
        org.create_node("Senior Developer", "senior_dev", parent="eng_mgr",
                       data=Employee("Bob Davis", "Senior Developer", "Engineering"))
        org.create_node("Junior Developer", "junior_dev", parent="eng_mgr",
                       data=Employee("Carol White", "Junior Developer", "Engineering"))

        # Sales Team
        org.create_node("Sales Manager", "sales_mgr", parent="vp_sales",
                       data=Employee("Dave Green", "Sales Manager", "Sales"))
        org.create_node("Sales Rep", "sales_rep", parent="sales_mgr",
                       data=Employee("Eve Black", "Sales Representative", "Sales"))

        return org

    # Usage
    org_chart = build_org_chart()

    # Display with titles
    org_chart.show(data_property="title")

    # Find all engineering employees
    engineering_staff = [node for node in org_chart.all_nodes()
                        if node.data.department == "Engineering"]

Decision Tree
-------------

Implement a simple decision tree:

.. code-block:: python

    from treelib import Tree

    class DecisionNode:
        def __init__(self, question=None, answer=None, condition=None):
            self.question = question
            self.answer = answer
            self.condition = condition

        def __str__(self):
            if self.answer:
                return f"Answer: {self.answer}"
            return f"Question: {self.question}"

    def build_decision_tree():
        """Build a simple decision tree for weather activities."""
        tree = Tree()

        # Root decision
        tree.create_node("Weather Decision", "root",
                        data=DecisionNode("Is it sunny?"))

        # Sunny branch
        tree.create_node("Sunny", "sunny", parent="root",
                        data=DecisionNode("Is it hot?"))
        tree.create_node("Go Swimming", "swim", parent="sunny",
                        data=DecisionNode(answer="Go to the beach!"))
        tree.create_node("Go Hiking", "hike", parent="sunny",
                        data=DecisionNode(answer="Perfect for a hike!"))

        # Not sunny branch
        tree.create_node("Not Sunny", "cloudy", parent="root",
                        data=DecisionNode("Is it raining?"))
        tree.create_node("Stay Inside", "inside", parent="cloudy",
                        data=DecisionNode(answer="Movie day!"))
        tree.create_node("Light Activity", "light", parent="cloudy",
                        data=DecisionNode(answer="Good for shopping!"))

        return tree

    # Usage
    decision_tree = build_decision_tree()
    decision_tree.show()

📊 Performance and Best Practices
=================================

Performance Characteristics
---------------------------

**Time Complexity:**
    * Node access: O(1)
    * Node insertion: O(1)
    * Tree traversal: O(n)
    * Search operations: O(n)
    * Subtree operations: O(k) where k is subtree size

**Memory Usage:**
    * Each node: ~200 bytes + data size
    * Tree overhead: ~100 bytes + node dictionary
    * Shallow copy: Shares node references (minimal memory)
    * Deep copy: Duplicates all data (2x memory usage)

Best Practices
--------------

**Choosing Identifiers**

.. code-block:: python

    # Good: Meaningful, unique identifiers
    tree.create_node("User Profile", "user_123")
    tree.create_node("Settings", "user_123_settings", parent="user_123")

    # Avoid: Generic or potentially conflicting IDs
    tree.create_node("Item", "1")  # Too generic
    tree.create_node("Data", "data")  # Might conflict

**Memory Management**

.. code-block:: python

    # For large trees, consider lazy loading
    def load_children_on_demand(tree, node_id):
        if not tree.is_branch(node_id):  # No children loaded yet
            # Load children from database/file
            load_node_children(tree, node_id)

    # Use shallow copies when possible
    backup_tree = Tree(original_tree, deep=False)

    # Clean up references when done
    del large_tree

**Error Handling**

.. code-block:: python

    from treelib.exceptions import NodeIDAbsentError, DuplicatedNodeIdError

    try:
        tree.create_node("New Node", "existing_id")
    except DuplicatedNodeIdError:
        print("Node ID already exists!")

    try:
        node = tree["nonexistent"]
    except NodeIDAbsentError:
        print("Node not found!")

    # Safe alternative
    node = tree.get_node("might_not_exist")
    if node is not None:
        print(f"Found: {node.tag}")

🔧 Advanced Topics
==================

Custom Node Classes
-------------------

Extend the Node class for specialized functionality:

.. code-block:: python

    from treelib import Node, Tree

    class FileNode(Node):
        def __init__(self, tag, identifier=None, size=0, file_type="unknown"):
            super().__init__(tag, identifier)
            self.size = size
            self.file_type = file_type

        @property
        def size_mb(self):
            return self.size / (1024 * 1024)

        def is_large_file(self):
            return self.size > 10 * 1024 * 1024  # 10MB

    # Use custom node class
    file_tree = Tree(node_class=FileNode)
    file_tree.create_node("Large File", "big_file", size=50*1024*1024, file_type="video")

Tree Algorithms
---------------

Implement custom tree algorithms:

.. code-block:: python

    def find_path(tree, start_id, end_id):
        """Find path between two nodes."""
        # Get path from start to root
        start_path = list(tree.rsearch(start_id))
        # Get path from end to root
        end_path = list(tree.rsearch(end_id))

        # Find common ancestor
        common_ancestors = set(start_path) & set(end_path)
        if not common_ancestors:
            return None

        # Find lowest common ancestor
        lca = min(common_ancestors, key=lambda x: tree.level(x))

        # Construct path
        start_to_lca = start_path[:start_path.index(lca)]
        lca_to_end = end_path[:end_path.index(lca)]

        return start_to_lca + [lca] + lca_to_end[::-1]

    def tree_statistics(tree):
        """Calculate comprehensive tree statistics."""
        stats = {}

        # Basic stats
        stats['total_nodes'] = tree.size()
        stats['depth'] = tree.depth()
        stats['leaves'] = len(tree.leaves())

        # Level distribution
        level_counts = {}
        for node in tree.all_nodes():
            level = tree.level(node.identifier)
            level_counts[level] = level_counts.get(level, 0) + 1
        stats['level_distribution'] = level_counts

        # Branching factor
        branching_factors = []
        for node in tree.all_nodes():
            children_count = len(tree.children(node.identifier))
            if children_count > 0:
                branching_factors.append(children_count)

        if branching_factors:
            stats['avg_branching_factor'] = sum(branching_factors) / len(branching_factors)
            stats['max_branching_factor'] = max(branching_factors)

        return stats

Multi-Tree Operations
--------------------

Work with multiple trees simultaneously:

.. code-block:: python

    def merge_trees(tree1, tree2, merge_point):
        """Merge two trees at specified point."""
        if not tree1.contains(merge_point):
            raise ValueError(f"Merge point {merge_point} not found in tree1")

        # Create deep copy to avoid modifying original
        merged_tree = Tree(tree1, deep=True)
        tree2_copy = Tree(tree2, deep=True)

        # Merge at specified point
        merged_tree.paste(merge_point, tree2_copy)

        return merged_tree

    def compare_trees(tree1, tree2):
        """Compare two trees structurally."""
        def get_structure(tree, node_id=None):
            if node_id is None:
                node_id = tree.root

            children = tree.children(node_id)
            if not children:
                return tree[node_id].tag

            return {
                'tag': tree[node_id].tag,
                'children': [get_structure(tree, child.identifier) for child in children]
            }

        return get_structure(tree1) == get_structure(tree2)

🚨 Troubleshooting
==================

Common Issues and Solutions
---------------------------

**Problem: "NodeIDAbsentError" when accessing nodes**

.. code-block:: python

    # Problem: Node doesn't exist
    try:
        node = tree["nonexistent_id"]
    except NodeIDAbsentError:
        print("Node not found!")

    # Solution: Use safe access
    node = tree.get_node("nonexistent_id")
    if node is None:
        print("Node not found!")

**Problem: "DuplicatedNodeIdError" when creating nodes**

.. code-block:: python

    # Problem: ID already exists
    tree.create_node("First", "duplicate_id")
    # tree.create_node("Second", "duplicate_id")  # This will fail!

    # Solution: Check existence first
    if "duplicate_id" not in tree:
        tree.create_node("Second", "duplicate_id")

**Problem: Memory issues with large trees**

.. code-block:: python

    # Problem: Deep copying large trees
    # large_tree_copy = Tree(large_tree, deep=True)  # Uses lots of memory

    # Solution: Use shallow copy when possible
    large_tree_copy = Tree(large_tree, deep=False)  # Shares references

**Problem: Performance issues with frequent modifications**

.. code-block:: python

    # Problem: Adding many nodes one by one
    for i in range(10000):
        tree.create_node(f"Node {i}", f"node_{i}", parent="root")

    # Solution: Batch operations when possible
    root_id = "root"
    nodes_to_add = [(f"Node {i}", f"node_{i}") for i in range(10000)]

    for tag, node_id in nodes_to_add:
        tree.create_node(tag, node_id, parent=root_id)

Debug and Inspection Tools
-------------------------

.. code-block:: python

    def debug_tree(tree, node_id=None):
        """Print detailed tree debug information."""
        print(f"Tree Debug Info:")
        print(f"  Tree ID: {tree.identifier}")
        print(f"  Root: {tree.root}")
        print(f"  Size: {tree.size()}")
        print(f"  Depth: {tree.depth()}")

        if node_id:
            if tree.contains(node_id):
                node = tree[node_id]
                print(f"\nNode '{node_id}' Debug:")
                print(f"  Tag: {node.tag}")
                print(f"  Level: {tree.level(node_id)}")
                print(f"  Is Leaf: {node.is_leaf(tree.identifier)}")
                print(f"  Is Root: {node.is_root(tree.identifier)}")
                print(f"  Children: {len(tree.children(node_id))}")
                print(f"  Parent: {tree.parent(node_id)}")
            else:
                print(f"Node '{node_id}' not found!")

    def validate_tree_integrity(tree):
        """Validate tree structure integrity."""
        issues = []

        # Check root existence
        if tree.root and not tree.contains(tree.root):
            issues.append("Root node reference is invalid")

        # Check parent-child consistency
        for node_id, node in tree.nodes.items():
            parent_id = node.predecessor(tree.identifier)
            if parent_id:
                if not tree.contains(parent_id):
                    issues.append(f"Node {node_id} has invalid parent {parent_id}")
                else:
                    parent_children = tree.children(parent_id)
                    if node not in parent_children:
                        issues.append(f"Parent-child relationship inconsistent for {node_id}")

        return issues

📖 API Reference
================

For detailed API documentation of all methods and classes, see the automatically generated documentation sections below.

.. toctree::
   :maxdepth: 2

   modules

🤝 Contributing and Support
===========================

**Found a bug or have a feature request?**
    Open an issue on `GitHub <https://github.com/caesar0301/treelib/issues>`_

**Want to contribute?**
    Fork the repository and submit a pull request!

**Need help?**
    Check out the `examples directory <https://github.com/caesar0301/treelib/tree/master/examples>`_ for comprehensive usage examples.

**Performance benchmarks and advanced examples:**
    See the `tree_algorithms.py <https://github.com/caesar0301/treelib/blob/master/examples/tree_algorithms.py>`_ example for algorithmic implementations and performance analysis.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

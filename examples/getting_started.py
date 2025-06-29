#!/usr/bin/env python
"""
Getting Started with TreeLib - A Beginner's Guide

This example provides a gentle introduction to treelib for new users.
It covers all the essential concepts and basic operations step by step.

Topics covered:
- Creating trees and nodes
- Basic tree navigation
- Displaying trees
- Common tree operations

Perfect for newcomers to the library!

Author: treelib contributors
"""

from treelib import Tree


def lesson_1_creating_trees():
    """Lesson 1: Creating your first tree."""
    print("=" * 60)
    print("📚 LESSON 1: Creating Your First Tree")
    print("=" * 60)

    print("🌱 Creating an empty tree:")
    tree = Tree()
    print(f"   Tree created! Size: {tree.size()}")

    print("\n🌳 Adding the root node:")
    tree.create_node("Root", "root")  # tag="Root", identifier="root"
    print("   Root node added!")
    tree.show()

    print("\n📝 Key concepts:")
    print("   • Every tree needs a root node")
    print("   • Nodes have a 'tag' (display name) and 'identifier' (unique ID)")
    print("   • The identifier is used to reference the node later")


def lesson_2_adding_children():
    """Lesson 2: Building a tree structure."""
    print("\n" + "=" * 60)
    print("📚 LESSON 2: Adding Children to Build Structure")
    print("=" * 60)

    # Start with a tree
    tree = Tree()
    tree.create_node("Company", "company")

    print("🏢 Building a company organization tree:")

    # Add departments
    tree.create_node("Engineering", "eng", parent="company")
    tree.create_node("Sales", "sales", parent="company")
    tree.create_node("HR", "hr", parent="company")

    print("   Added departments...")

    # Add people to engineering
    tree.create_node("Alice (CTO)", "alice", parent="eng")
    tree.create_node("Bob (Developer)", "bob", parent="eng")
    tree.create_node("Carol (Developer)", "carol", parent="eng")

    # Add people to sales
    tree.create_node("Dave (Sales Manager)", "dave", parent="sales")
    tree.create_node("Eve (Sales Rep)", "eve", parent="sales")

    # Add people to HR
    tree.create_node("Frank (HR Manager)", "frank", parent="hr")

    print("\n🌳 Complete organization structure:")
    tree.show()

    print("\n📝 Key concepts:")
    print("   • Use 'parent' parameter to specify where new nodes attach")
    print("   • Trees automatically organize the hierarchy")
    print("   • Each node can have multiple children")


def lesson_3_tree_information():
    """Lesson 3: Getting information about your tree."""
    print("\n" + "=" * 60)
    print("📚 LESSON 3: Getting Tree Information")
    print("=" * 60)

    # Create a sample tree
    tree = Tree()
    tree.create_node("Animals", "animals")
    tree.create_node("Mammals", "mammals", parent="animals")
    tree.create_node("Birds", "birds", parent="animals")
    tree.create_node("Dogs", "dogs", parent="mammals")
    tree.create_node("Cats", "cats", parent="mammals")
    tree.create_node("Eagles", "eagles", parent="birds")
    tree.create_node("Sparrows", "sparrows", parent="birds")

    print("🦎 Animal classification tree:")
    tree.show()

    print("\n📊 Tree statistics:")
    print(f"   • Total nodes: {tree.size()}")
    print(f"   • Tree depth: {tree.depth()}")
    print(f"   • Root node: {tree.root}")

    print("\n🍃 Leaf nodes (nodes with no children):")
    leaves = tree.leaves()
    for leaf_node in leaves:
        print(f"   • {leaf_node.tag}")

    print("\n🔍 Node relationships:")
    mammals_node = tree["mammals"]
    print(f"   • 'Mammals' node: {mammals_node.tag}")
    print(f"   • Its parent: {tree.parent('mammals').tag}")

    children = tree.children("mammals")
    print(f"   • Its children: {[tree[child.identifier].tag for child in children]}")

    print("\n📝 Key concepts:")
    print("   • tree.size() gives total number of nodes")
    print("   • tree.depth() gives maximum depth")
    print("   • tree.leaves() finds nodes with no children")
    print("   • Use tree[id] to get a specific node")


def lesson_4_navigating_trees():
    """Lesson 4: Different ways to navigate and traverse trees."""
    print("\n" + "=" * 60)
    print("📚 LESSON 4: Navigating and Traversing Trees")
    print("=" * 60)

    # Create a file system like tree
    tree = Tree()
    tree.create_node("📁 /", "root")
    tree.create_node("📁 home", "home", parent="root")
    tree.create_node("📁 var", "var", parent="root")
    tree.create_node("📁 user1", "user1", parent="home")
    tree.create_node("📁 user2", "user2", parent="home")
    tree.create_node("📁 log", "log", parent="var")
    tree.create_node("📄 document.txt", "doc1", parent="user1")
    tree.create_node("📄 photo.jpg", "photo1", parent="user1")
    tree.create_node("📄 readme.md", "readme", parent="user2")
    tree.create_node("📄 system.log", "syslog", parent="log")

    print("🗂️  File system tree:")
    tree.show()

    print("\n🚶 Depth-first traversal (like 'find' command):")
    for node_id in tree.expand_tree():
        node = tree[node_id]
        level = tree.level(node_id)
        indent = "  " * level
        print(f"{indent}{node.tag}")

    print("\n🌊 Breadth-first traversal (level by level):")
    for node_id in tree.expand_tree(mode=Tree.WIDTH):
        node = tree[node_id]
        level = tree.level(node_id)
        print(f"   Level {level}: {node.tag}")

    print("\n🔄 Path from a file to root:")
    path = tree.rsearch("doc1")  # Path from document.txt to root
    path_names = [tree[node_id].tag for node_id in path]
    print(f"   {' ← '.join(path_names)}")

    print("\n📝 Key concepts:")
    print("   • expand_tree() gives all nodes in depth-first order")
    print("   • expand_tree(mode=Tree.WIDTH) gives breadth-first order")
    print("   • rsearch() finds path from node to root")
    print("   • level() tells you how deep a node is")


def lesson_5_searching_filtering():
    """Lesson 5: Searching and filtering trees."""
    print("\n" + "=" * 60)
    print("📚 LESSON 5: Searching and Filtering Trees")
    print("=" * 60)

    # Create a product catalog tree
    tree = Tree()
    tree.create_node("🛍️ Store", "store")
    tree.create_node("📱 Electronics", "electronics", parent="store")
    tree.create_node("👕 Clothing", "clothing", parent="store")
    tree.create_node("📚 Books", "books", parent="store")

    # Electronics
    tree.create_node("📱 iPhone 13", "iphone", parent="electronics")
    tree.create_node("💻 MacBook Pro", "macbook", parent="electronics")
    tree.create_node("🎧 AirPods", "airpods", parent="electronics")

    # Clothing
    tree.create_node("👔 Shirts", "shirts", parent="clothing")
    tree.create_node("👖 Pants", "pants", parent="clothing")
    tree.create_node("👕 T-Shirt Blue", "tshirt1", parent="shirts")
    tree.create_node("👕 T-Shirt Red", "tshirt2", parent="shirts")

    # Books
    tree.create_node("📖 Python Guide", "python_book", parent="books")
    tree.create_node("📖 JavaScript Bible", "js_book", parent="books")

    print("🛍️ Product catalog:")
    tree.show()

    print("\n🔍 Finding all products containing 'T-Shirt':")
    for node_id in tree.expand_tree():
        node = tree[node_id]
        if "T-Shirt" in node.tag:
            print(f"   Found: {node.tag}")

    print("\n📱 Showing only Electronics section:")
    electronics_subtree = tree.subtree("electronics")
    electronics_subtree.show()

    print("\n🎯 Using filter to show only leaf products:")
    tree.show(filter=lambda node: node.is_leaf(tree.identifier))

    print("\n📝 Key concepts:")
    print("   • Use loops with expand_tree() to search nodes")
    print("   • subtree() creates a new tree from a branch")
    print("   • show(filter=...) displays only matching nodes")
    print("   • node.is_leaf() checks if node has children")


def lesson_6_modifying_trees():
    """Lesson 6: Modifying tree structure."""
    print("\n" + "=" * 60)
    print("📚 LESSON 6: Modifying Tree Structure")
    print("=" * 60)

    # Create initial tree
    tree = Tree()
    tree.create_node("🏠 Family", "family")
    tree.create_node("👴 Grandpa", "grandpa", parent="family")
    tree.create_node("👩 Mom", "mom", parent="grandpa")
    tree.create_node("👨 Dad", "dad", parent="grandpa")
    tree.create_node("👧 Alice", "alice", parent="mom")
    tree.create_node("👦 Bob", "bob", parent="dad")

    print("👨‍👩‍👧‍👦 Original family tree:")
    tree.show()

    print("\n🚚 Moving Alice to be under Dad instead:")
    tree.move_node("alice", "dad")
    tree.show()

    print("\n👶 Adding a new family member:")
    tree.create_node("👶 Baby Charlie", "charlie", parent="mom")
    tree.show()

    print("\n❌ Removing Bob from the family:")
    removed_count = tree.remove_node("bob")
    print(f"   Removed {removed_count} node(s)")
    tree.show()

    print("\n📋 Copying a branch:")
    # Create a new tree to paste into
    new_tree = Tree()
    new_tree.create_node("🌳 New Tree", "new_root")

    # Copy mom's branch to the new tree
    mom_subtree = tree.subtree("mom")
    new_tree.paste("new_root", mom_subtree)

    print("   Mom's branch copied to new tree:")
    new_tree.show()

    print("\n📝 Key concepts:")
    print("   • move_node() changes a node's parent")
    print("   • remove_node() deletes nodes and their children")
    print("   • subtree() + paste() copies branches between trees")
    print("   • All changes update the tree structure automatically")


def lesson_7_node_data():
    """Lesson 7: Storing custom data in nodes."""
    print("\n" + "=" * 60)
    print("📚 LESSON 7: Storing Custom Data in Nodes")
    print("=" * 60)

    tree = Tree()

    # Create nodes with custom data
    tree.create_node("🏢 Company", "company", data={"type": "corporation", "employees": 500})

    tree.create_node(
        "💻 Engineering",
        "eng",
        parent="company",
        data={"budget": 2000000, "headcount": 50, "location": "Building A"},
    )

    tree.create_node(
        "📊 Sales",
        "sales",
        parent="company",
        data={"budget": 800000, "headcount": 30, "location": "Building B"},
    )

    # Add employees with detailed data
    tree.create_node(
        "👩‍💻 Alice Smith",
        "alice",
        parent="eng",
        data={
            "role": "Senior Engineer",
            "salary": 120000,
            "years": 5,
            "skills": ["Python", "React"],
        },
    )

    tree.create_node(
        "👨‍💻 Bob Jones",
        "bob",
        parent="eng",
        data={
            "role": "Junior Engineer",
            "salary": 80000,
            "years": 1,
            "skills": ["JavaScript", "HTML"],
        },
    )

    print("🏢 Company structure:")
    tree.show()

    print("\n📊 Accessing node data:")
    alice = tree["alice"]
    print(f"   Alice's role: {alice.data['role']}")
    print(f"   Alice's salary: ${alice.data['salary']:,}")
    print(f"   Alice's skills: {', '.join(alice.data['skills'])}")

    print("\n💰 Department budgets:")
    for dept_id in ["eng", "sales"]:
        dept = tree[dept_id]
        budget = dept.data["budget"]
        headcount = dept.data["headcount"]
        print(f"   {dept.tag}: ${budget:,} budget, {headcount} people")

    print("\n📈 Total company salary expenses:")
    total_salary = 0
    for node_id in tree.expand_tree():
        node = tree[node_id]
        if node.data and "salary" in node.data:
            total_salary += node.data["salary"]
    print(f"   Total: ${total_salary:,}")

    print("\n📝 Key concepts:")
    print("   • Use 'data' parameter to store custom information")
    print("   • Data can be any Python object (dict, list, custom class)")
    print("   • Access data with node.data['key']")
    print("   • Perfect for business logic and domain-specific data")


def lesson_8_advanced_display():
    """Lesson 8: Advanced display and export options."""
    print("\n" + "=" * 60)
    print("📚 LESSON 8: Advanced Display and Export Options")
    print("=" * 60)

    # Create a project tree
    tree = Tree()
    tree.create_node("🚀 MyProject", "project")
    tree.create_node("📁 src", "src", parent="project")
    tree.create_node("📁 tests", "tests", parent="project")
    tree.create_node("📁 docs", "docs", parent="project")
    tree.create_node("🐍 main.py", "main", parent="src")
    tree.create_node("🐍 utils.py", "utils", parent="src")
    tree.create_node("🧪 test_main.py", "test_main", parent="tests")
    tree.create_node("📖 README.md", "readme", parent="docs")

    print("📁 Project structure (default style):")
    tree.show()

    print("\n🎨 Fancy ASCII style:")
    tree.show(line_type="ascii-em")

    print("\n🏷️ Showing node identifiers:")
    tree.show(idhidden=False)

    print("\n📋 Tree as JSON:")
    json_output = tree.to_json()
    print(f"   {json_output}")

    print("\n📋 Tree as dictionary:")
    dict_output = tree.to_dict()
    print(f"   {dict_output}")

    print("\n💾 Saving to file:")
    tree.save2file("project_tree.txt")
    print("   Tree saved to 'project_tree.txt'")

    # Clean up the file
    import os

    try:
        os.remove("project_tree.txt")
        print("   (Cleaned up temporary file)")
    except BaseException:
        pass

    print("\n📝 Key concepts:")
    print("   • line_type parameter changes visual style")
    print("   • idhidden=False shows node identifiers")
    print("   • to_json() and to_dict() export data")
    print("   • save2file() exports visual representation")


def main():
    """Run all lessons in sequence."""
    print("🌳 Welcome to TreeLib - A Beginner's Guide!")
    print("This tutorial will teach you everything you need to know about treelib.")
    print("Each lesson builds on the previous one, so follow along step by step.\n")

    # Run all lessons
    lesson_1_creating_trees()
    lesson_2_adding_children()
    lesson_3_tree_information()
    lesson_4_navigating_trees()
    lesson_5_searching_filtering()
    lesson_6_modifying_trees()
    lesson_7_node_data()
    lesson_8_advanced_display()

    print("\n" + "=" * 60)
    print("🎉 CONGRATULATIONS!")
    print("=" * 60)
    print("You've completed the TreeLib beginner's guide!")
    print("You now know how to:")
    print("  • Create and build tree structures")
    print("  • Navigate and search trees")
    print("  • Modify tree structure dynamically")
    print("  • Store custom data in nodes")
    print("  • Display and export trees")
    print("\nNext steps:")
    print("  • Check out the other examples for advanced use cases")
    print("  • Read the documentation for complete API reference")
    print("  • Start building your own tree-based applications!")
    print("=" * 60)


if __name__ == "__main__":
    main()

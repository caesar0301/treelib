#!/usr/bin/env python
"""
Family Tree Example - Comprehensive demonstration of treelib features

This example shows how to:
- Create a family tree structure
- Display trees in different formats
- Navigate and filter tree data
- Modify tree structure (add, remove, move nodes)
- Work with subtrees

Author: treelib contributors
"""

from treelib import Tree


def create_family_tree():
    """
    Create a sample family tree structure.

    Tree structure:
        Harry (root)
        ├── Jane
        │   ├── Diane
        │   │   └── Mary
        │   └── Mark
        └── Bill

    Returns:
        Tree: A populated family tree
    """
    tree = Tree()

    # Create root node
    tree.create_node("Harry", "harry")

    # Add Harry's children
    tree.create_node("Jane", "jane", parent="harry")
    tree.create_node("Bill", "bill", parent="harry")

    # Add Jane's children
    tree.create_node("Diane", "diane", parent="jane")
    tree.create_node("Mark", "mark", parent="jane")

    # Add Diane's child
    tree.create_node("Mary", "mary", parent="diane")

    return tree


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 50)
    print(f"📋 {title}")
    print("=" * 50)


def demonstrate_basic_display(tree):
    """Demonstrate different ways to display the tree."""
    print_section("BASIC TREE DISPLAY")

    print("🌳 Family tree (default format):")
    tree.show()

    print("\n🎨 Family tree (fancy format with sorting):")
    tree.show(key=lambda x: x.tag, reverse=True, line_type="ascii-em")

    print("\n🏷️  Family tree (showing node identifiers):")
    tree.show(idhidden=False)


def demonstrate_tree_traversal(tree):
    """Demonstrate different tree traversal methods."""
    print_section("TREE TRAVERSAL")

    print("👥 All family members (depth-first order):")
    members = [tree[node].tag for node in tree.expand_tree()]
    print("   ", " → ".join(members))

    print("\n👥 All family members (breadth-first order):")
    members = [tree[node].tag for node in tree.expand_tree(mode=Tree.WIDTH)]
    print("   ", " → ".join(members))

    print("\n📊 Family tree statistics:")
    print(f"   Total members: {tree.size()}")
    print(f"   Tree depth: {tree.depth()}")
    print(f"   Number of leaves: {len(tree.leaves())}")


def demonstrate_filtering(tree):
    """Demonstrate tree filtering capabilities."""
    print_section("FILTERING AND SEARCHING")

    print("🔍 Family tree excluding Diane's branch:")
    tree.show(filter=lambda x: x.identifier != "diane")

    print("\n👶 Only leaf nodes (family members with no children):")
    leaves = [leaf.tag for leaf in tree.leaves()]
    print("   ", ", ".join(leaves))

    print("\n👴 Path from Mary to root (ancestors):")
    ancestors = [tree[node].tag for node in tree.rsearch("mary")]
    print("   ", " ← ".join(ancestors))


def demonstrate_subtrees(tree):
    """Demonstrate working with subtrees."""
    print_section("WORKING WITH SUBTREES")

    print("🌲 Diane's family subtree:")
    diane_subtree = tree.subtree("diane")
    diane_subtree.show()

    print("\n👨‍👩‍👧‍👦 Jane's children:")
    for child_id in tree.is_branch("jane"):
        child_name = tree[child_id].tag
        print(f"   • {child_name}")


def demonstrate_tree_modifications(tree):
    """Demonstrate tree modification operations."""
    print_section("TREE MODIFICATIONS")

    # Make a copy for modifications to avoid affecting original
    modified_tree = Tree(tree, deep=True)

    print("➕ Adding new family members:")
    # Create a small family to join
    new_family = Tree()
    new_family.create_node("New Member 1", "new1")
    new_family.create_node("New Member 2", "new2", parent="new1")
    new_family.create_node("New Member 3", "new3", parent="new1")

    # Paste new family under Bill
    modified_tree.paste("bill", new_family)
    print("   Added new family under Bill:")
    modified_tree.show()

    print("\n🏠 Mary moves to live with grandfather Harry:")
    modified_tree.move_node("mary", "harry")
    modified_tree.show()

    print("\n❌ Removing New Member 1 and their descendants:")
    removed_count = modified_tree.remove_node("new1")
    print(f"   Removed {removed_count} nodes")
    modified_tree.show()


def demonstrate_advanced_features(tree):
    """Demonstrate advanced treelib features."""
    print_section("ADVANCED FEATURES")

    print("📄 Tree as JSON:")
    json_output = tree.to_json()
    print(f"   {json_output}")

    print("\n📋 Tree as dictionary:")
    dict_output = tree.to_dict()
    print(f"   {dict_output}")

    print("\n🔍 Finding nodes:")
    jane_node = tree.get_node("jane")
    print(f"   Jane's node: {jane_node}")
    print(f"   Jane's parent: {tree.parent('jane').tag}")
    print(f"   Jane's children: {[child.tag for child in tree.children('jane')]}")

    siblings = tree.siblings("jane")
    if siblings:
        sibling_names = [sibling.tag for sibling in siblings]
        print(f"   Jane's siblings: {', '.join(sibling_names)}")


def main():
    """Main function demonstrating all treelib features."""
    print("🌳 Welcome to the TreeLib Family Tree Example!")
    print("This example demonstrates the key features of the treelib library.")

    # Create the family tree
    tree = create_family_tree()

    # Run all demonstrations
    demonstrate_basic_display(tree)
    demonstrate_tree_traversal(tree)
    demonstrate_filtering(tree)
    demonstrate_subtrees(tree)
    demonstrate_tree_modifications(tree)
    demonstrate_advanced_features(tree)

    print("\n" + "=" * 50)
    print("🎉 Example completed! Try modifying the code to experiment further.")
    print("=" * 50)


if __name__ == "__main__":
    main()

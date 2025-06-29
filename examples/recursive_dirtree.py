#!/usr/bin/env python
"""
Recursive Directory Tree Generator - Simulate directory structures

This example demonstrates how to:
- Generate recursive tree structures programmatically
- Work with custom node data
- Create realistic directory-like hierarchies
- Use different tree traversal methods

This is useful for:
- Testing tree operations with large datasets
- Simulating file system structures
- Creating mock data for applications

Author: treelib contributors (originally by samuelsh)
"""

import hashlib
import random
import string

from treelib import Tree

# Configuration constants
MAX_FILES_PER_DIR = 10
DEFAULT_TREE_DEPTH = 3
DEFAULT_TREE_WIDTH = 5


def get_random_string(length=8):
    """
    Generate a random string of specified length.

    Args:
        length (int): Length of the string to generate

    Returns:
        str: Random string containing letters and digits
    """
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def create_unique_id(name):
    """
    Create a unique identifier from a name using MD5 hash.

    Args:
        name (str): Name to hash

    Returns:
        str: Hexadecimal hash string
    """
    return hashlib.md5(name.encode("utf-8")).hexdigest()


class Directory:
    """
    Represents a directory with files.

    Attributes:
        name (str): Directory name
        files (list): List of File objects in this directory
        created_at (str): Simulated creation timestamp
    """

    def __init__(self, name=None):
        """
        Initialize a directory.

        Args:
            name (str, optional): Directory name. If None, generates random name.
        """
        self.name = name if name else get_random_string(12)
        self.files = [File() for _ in range(random.randint(1, MAX_FILES_PER_DIR))]
        self.created_at = f"2023-{random.randint(1, 12): 02d}-{random.randint(1, 28): 02d}"

    def __str__(self):
        return f"Directory(name='{self.name}', files={len(self.files)})"

    def __repr__(self):
        return self.__str__()


class File:
    """
    Represents a file within a directory.

    Attributes:
        name (str): File name
        size (int): File size in bytes
        extension (str): File extension
    """

    def __init__(self, name=None):
        """
        Initialize a file.

        Args:
            name (str, optional): File name. If None, generates random name.
        """
        extensions = [".txt", ".pdf", ".doc", ".jpg", ".png", ".py", ".js", ".css"]

        self.name = name if name else get_random_string(8)
        self.extension = random.choice(extensions)
        self.size = random.randint(1024, 1024 * 1024)  # 1KB to 1MB

    @property
    def full_name(self):
        """Get the full filename with extension."""
        return f"{self.name}{self.extension}"

    def __str__(self):
        return f"File(name='{self.full_name}', size={self.size})"

    def __repr__(self):
        return self.__str__()


def build_recursive_tree(tree, base_node, depth, width):
    """
    Recursively build a tree structure with the specified depth and width.

    Args:
        tree (Tree): The tree to build
        base_node (Node): The node to attach children to
        depth (int): How many more levels to create
        width (int): How many children to create at each level
    """
    if depth <= 0:
        return

    # Create children at current level
    for i in range(width):
        directory = Directory()

        # Create unique node identifier
        node_id = create_unique_id(f"{base_node.identifier}_{directory.name}_{i}")

        # Create node with directory data
        child_node = tree.create_node(
            tag=directory.name,
            identifier=node_id,
            parent=base_node.identifier,
            data=directory,
        )

        # Recursively create children
        build_recursive_tree(tree, child_node, depth - 1, width)


def create_directory_tree(depth=DEFAULT_TREE_DEPTH, width=DEFAULT_TREE_WIDTH, root_name="Root"):
    """
    Create a tree representing a directory structure.

    Args:
        depth (int): Maximum depth of the tree
        width (int): Number of children per node
        root_name (str): Name of the root directory

    Returns:
        Tree: Generated directory tree
    """
    tree = Tree()

    # Create root directory
    root_directory = Directory(root_name)
    root_node = tree.create_node(tag=root_directory.name, identifier="root", data=root_directory)

    # Build the recursive structure
    build_recursive_tree(tree, root_node, depth, width)

    return tree


def analyze_tree(tree):
    """
    Analyze and display statistics about the generated tree.

    Args:
        tree (Tree): Tree to analyze
    """
    print("\n" + "=" * 50)
    print("📊 TREE ANALYSIS")
    print("=" * 50)

    print(f"📁 Total directories: {tree.size()}")
    print(f"📏 Tree depth: {tree.depth()}")
    print(f"🍃 Leaf directories: {len(tree.leaves())}")

    # Count total files
    total_files = 0
    total_size = 0

    for node_id in tree.expand_tree():
        node = tree.get_node(node_id)
        if node.data and hasattr(node.data, "files"):
            total_files += len(node.data.files)
            for file in node.data.files:
                total_size += file.size

    print(f"📄 Total files: {total_files}")
    print(f"💾 Total size: {total_size:, } bytes ({total_size/1024/1024: .2f} MB)")


def demonstrate_tree_traversal(tree):
    """
    Demonstrate different ways to traverse the tree.

    Args:
        tree (Tree): Tree to traverse
    """
    print("\n" + "=" * 50)
    print("🚶 TREE TRAVERSAL METHODS")
    print("=" * 50)

    print("📋 Depth-first traversal (first 10 directories):")
    depth_first = list(tree.expand_tree())[:10]
    for node_id in depth_first:
        node = tree.get_node(node_id)
        print(f"   📁 {node.tag}")

    print("\n📋 Breadth-first traversal (first 10 directories):")
    breadth_first = list(tree.expand_tree(mode=Tree.WIDTH))[:10]
    for node_id in breadth_first:
        node = tree.get_node(node_id)
        print(f"   📁 {node.tag}")

    print("\n📋 Leaf directories (directories with no subdirectories):")
    leaves = tree.leaves()[:5]  # Show first 5 leaves
    for leaf_node in leaves:
        file_count = len(leaf_node.data.files) if leaf_node.data else 0
        print(f"   📁 {leaf_node.tag} ({file_count} files)")


def demonstrate_directory_operations(tree):
    """
    Demonstrate operations on the directory tree.

    Args:
        tree (Tree): Tree to operate on
    """
    print("\n" + "=" * 50)
    print("🔧 DIRECTORY OPERATIONS")
    print("=" * 50)

    # Find directories with many files
    print("📁 Directories with most files:")
    directories_with_files = []

    for node_id in tree.expand_tree():
        node = tree.get_node(node_id)
        if node.data and hasattr(node.data, "files"):
            directories_with_files.append((node.tag, len(node.data.files), node_id))

    # Sort by file count (descending)
    directories_with_files.sort(key=lambda x: x[1], reverse=True)

    for dir_name, file_count, node_id in directories_with_files[:5]:
        print(f"   📁 {dir_name}: {file_count} files")

    # Show path to a specific directory
    if directories_with_files:
        target_dir = directories_with_files[0][2]  # Directory with most files
        path = tree.rsearch(target_dir)
        path_names = [tree.get_node(node_id).tag for node_id in path]
        print(f"\n🗂️  Path to '{directories_with_files[0][0]}': ")
        print(f"   {' → '.join(path_names)}")


def main():
    """
    Main function demonstrating the recursive directory tree generator.
    """
    print("🌳 Welcome to the Recursive Directory Tree Generator!")
    print("This example creates a simulated directory structure with files.")

    # Create different sized trees
    print("\n" + "=" * 50)
    print("🏗️  GENERATING DIRECTORY TREES")
    print("=" * 50)

    # Small tree for detailed viewing
    print("📁 Creating small directory tree (depth=2, width=3)...")
    small_tree = create_directory_tree(depth=2, width=3, root_name="SmallProject")

    print("\n🌳 Small tree structure:")
    small_tree.show(line_type="ascii-em")

    analyze_tree(small_tree)
    demonstrate_tree_traversal(small_tree)
    demonstrate_directory_operations(small_tree)

    # Larger tree for performance demonstration
    print("\n" + "=" * 50)
    print("🏗️  GENERATING LARGER TREE")
    print("=" * 50)

    print("📁 Creating larger directory tree (depth=4, width=4)...")
    large_tree = create_directory_tree(depth=4, width=4, root_name="LargeProject")

    print("🌳 Large tree structure (showing first 20 directories):")
    nodes_to_show = list(large_tree.expand_tree())[:20]
    for node_id in nodes_to_show:
        node = large_tree.get_node(node_id)
        level = large_tree.level(node_id)
        indent = "  " * level
        print(f"{indent}📁 {node.tag}")

    if large_tree.size() > 20:
        print(f"   ... and {large_tree.size() - 20} more directories")

    analyze_tree(large_tree)

    print("\n" + "=" * 50)
    print("🎉 Directory tree generation completed!")
    print("💡 Try modifying the depth and width parameters to create different structures.")
    print("=" * 50)


if __name__ == "__main__":
    main()

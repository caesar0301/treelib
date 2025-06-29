#!/usr/bin/env python
"""
Tree Algorithms Example - Advanced tree operations and algorithms

This example demonstrates:
- Tree traversal algorithms
- Tree analysis and metrics
- Tree transformation operations
- Tree comparison and merging
- Path finding and navigation
- Tree balancing concepts

Perfect for understanding algorithmic aspects of trees!

Author: treelib contributors
"""

import random
from collections import defaultdict, deque

from treelib import Tree


def create_sample_binary_tree():
    """Create a sample binary-like tree for algorithm demonstrations."""
    tree = Tree()

    # Create a binary search tree structure
    tree.create_node("50", "50")
    tree.create_node("30", "30", parent="50")
    tree.create_node("70", "70", parent="50")
    tree.create_node("20", "20", parent="30")
    tree.create_node("40", "40", parent="30")
    tree.create_node("60", "60", parent="70")
    tree.create_node("80", "80", parent="70")
    tree.create_node("10", "10", parent="20")
    tree.create_node("25", "25", parent="20")
    tree.create_node("35", "35", parent="40")
    tree.create_node("45", "45", parent="40")

    return tree


def create_sample_organization_tree():
    """Create a sample organizational tree."""
    tree = Tree()

    tree.create_node("CEO", "ceo", data={"level": 1, "salary": 300000})
    tree.create_node("CTO", "cto", parent="ceo", data={"level": 2, "salary": 200000})
    tree.create_node("CFO", "cfo", parent="ceo", data={"level": 2, "salary": 180000})
    tree.create_node("VP Eng", "vp_eng", parent="cto", data={"level": 3, "salary": 150000})
    tree.create_node("VP Product", "vp_product", parent="cto", data={"level": 3, "salary": 140000})
    tree.create_node("Accounting Dir", "acc_dir", parent="cfo", data={"level": 3, "salary": 120000})
    tree.create_node("Senior Dev 1", "senior1", parent="vp_eng", data={"level": 4, "salary": 120000})
    tree.create_node("Senior Dev 2", "senior2", parent="vp_eng", data={"level": 4, "salary": 115000})
    tree.create_node(
        "Product Manager",
        "pm",
        parent="vp_product",
        data={"level": 4, "salary": 110000},
    )
    tree.create_node("Junior Dev 1", "junior1", parent="senior1", data={"level": 5, "salary": 80000})
    tree.create_node("Junior Dev 2", "junior2", parent="senior1", data={"level": 5, "salary": 75000})
    tree.create_node("Intern", "intern", parent="senior2", data={"level": 6, "salary": 40000})

    return tree


def demonstrate_traversal_algorithms():
    """Demonstrate different tree traversal algorithms."""
    print("=" * 60)
    print("🚶 TREE TRAVERSAL ALGORITHMS")
    print("=" * 60)

    tree = create_sample_binary_tree()

    print("🌳 Binary tree structure:")
    tree.show()

    print("\n📋 Depth-First Traversal (Pre-order):")

    def preorder_traversal(tree, node_id):
        """Pre-order: Root → Left → Right"""
        result = []

        def traverse(nid):
            result.append(tree[nid].tag)
            children = tree.children(nid)
            for child in children:
                traverse(child.identifier)

        traverse(node_id)
        return result

    preorder = preorder_traversal(tree, tree.root)
    print(f"   {' → '.join(preorder)}")

    print("\n📋 Breadth-First Traversal (Level-order):")

    def breadth_first_traversal(tree, start_node):
        """Level-by-level traversal using queue."""
        result = []
        queue = deque([start_node])

        while queue:
            node_id = queue.popleft()
            result.append(tree[node_id].tag)

            children = tree.children(node_id)
            for child in children:
                queue.append(child.identifier)

        return result

    breadth_first = breadth_first_traversal(tree, tree.root)
    print(f"   {' → '.join(breadth_first)}")

    print("\n📋 Leaves-to-Root Traversal:")

    def leaves_to_root_traversal(tree):
        """Traverse from leaves towards root."""
        result = []
        leaves = tree.leaves()

        # Start with all leaves
        for leaf in leaves:
            path = tree.rsearch(leaf.identifier)
            result.extend([tree[nid].tag for nid in path])

        return result

    leaves_to_root = leaves_to_root_traversal(tree)
    print(f"   {' → '.join(leaves_to_root)}")


def demonstrate_tree_analysis():
    """Demonstrate tree analysis and metric calculations."""
    print("\n" + "=" * 60)
    print("📊 TREE ANALYSIS AND METRICS")
    print("=" * 60)

    tree = create_sample_organization_tree()

    print("🏢 Organization tree:")
    tree.show()

    print("\n📈 Basic Tree Metrics:")
    print(f"   • Total nodes: {tree.size()}")
    print(f"   • Tree depth: {tree.depth()}")
    print(f"   • Number of leaves: {len(tree.leaves())}")
    print(f"   • Root node: {tree[tree.root].tag}")

    print("\n📊 Node Distribution by Level:")
    level_counts = defaultdict(int)
    for node_id in tree.expand_tree():
        level = tree.level(node_id)
        level_counts[level] += 1

    for level in sorted(level_counts.keys()):
        print(f"   • Level {level}: {level_counts[level]} nodes")

    print("\n💰 Salary Analysis:")
    total_salary = 0
    salary_by_level = defaultdict(list)

    for node_id in tree.expand_tree():
        node = tree[node_id]
        if node.data and "salary" in node.data:
            salary = node.data["salary"]
            total_salary += salary
            level = tree.level(node_id)
            salary_by_level[level].append(salary)

    print(f"   • Total payroll: ${total_salary:, }")
    print(f"   • Average salary: ${total_salary/tree.size():, .0f}")

    for level in sorted(salary_by_level.keys()):
        salaries = salary_by_level[level]
        avg_salary = sum(salaries) / len(salaries)
        print(f"   • Level {level} average: ${avg_salary:, .0f}")

    print("\n🔍 Tree Balance Analysis:")

    def calculate_balance_factor(tree, node_id):
        """Calculate balance factor for each node."""
        children = tree.children(node_id)
        if not children:
            return 0

        child_depths = []
        for child in children:
            child_depth = tree.depth(child.identifier)
            child_depths.append(child_depth)

        return max(child_depths) - min(child_depths) if len(child_depths) > 1 else 0

    balance_factors = {}
    for node_id in tree.expand_tree():
        balance_factors[node_id] = calculate_balance_factor(tree, node_id)

    avg_balance = sum(balance_factors.values()) / len(balance_factors)
    print(f"   • Average balance factor: {avg_balance: .2f}")
    print(f"   • Most unbalanced node: {max(balance_factors, key=balance_factors.get)}")


def demonstrate_path_finding():
    """Demonstrate path finding algorithms."""
    print("\n" + "=" * 60)
    print("🗺️ PATH FINDING ALGORITHMS")
    print("=" * 60)

    tree = create_sample_organization_tree()

    print("🏢 Finding paths in organization tree:")
    tree.show()

    print("\n🔍 Path from Intern to CEO:")
    intern_to_ceo = tree.rsearch("intern")
    path_names = [tree[nid].tag for nid in intern_to_ceo]
    print(f"   {' ← '.join(path_names)}")

    print("\n🔍 Shortest path between two nodes:")

    def find_shortest_path(tree, start_id, end_id):
        """Find shortest path between two nodes."""
        # Get paths to root for both nodes
        start_to_root = tree.rsearch(start_id)
        end_to_root = tree.rsearch(end_id)

        # Find common ancestor
        start_ancestors = set(start_to_root)
        common_ancestor = None

        for node_id in end_to_root:
            if node_id in start_ancestors:
                common_ancestor = node_id
                break

        if not common_ancestor:
            return []

        # Build path: start → common ancestor → end
        start_to_ancestor = []
        for node_id in start_to_root:
            start_to_ancestor.append(node_id)
            if node_id == common_ancestor:
                break

        ancestor_to_end = []
        for node_id in end_to_root:
            ancestor_to_end.append(node_id)
            if node_id == common_ancestor:
                break

        # Combine paths (remove duplicate common ancestor)
        full_path = start_to_ancestor + ancestor_to_end[1:][::-1]
        return full_path

    path = find_shortest_path(tree, "junior1", "pm")
    path_names = [tree[nid].tag for nid in path]
    print(f"   From Junior Dev 1 to Product Manager: {' → '.join(path_names)}")

    print("\n🌐 All paths from root to leaves:")

    def find_all_root_to_leaf_paths(tree):
        """Find all paths from root to leaves."""
        paths = []
        leaves = tree.leaves()

        for leaf in leaves:
            path = list(tree.rsearch(leaf.identifier))
            path_names = [tree[nid].tag for nid in reversed(path)]
            paths.append(path_names)

        return paths

    all_paths = find_all_root_to_leaf_paths(tree)
    for i, path in enumerate(all_paths, 1):
        print(f"   Path {i}: {' → '.join(path)}")


def demonstrate_tree_transformations():
    """Demonstrate tree transformation operations."""
    print("\n" + "=" * 60)
    print("🔄 TREE TRANSFORMATION OPERATIONS")
    print("=" * 60)

    tree = create_sample_binary_tree()

    print("🌳 Original tree:")
    tree.show()

    print("\n🔄 Tree Mirroring (Flipping left-right):")

    def mirror_tree(tree):
        """Create a mirrored version of the tree."""
        mirrored = Tree()

        # Copy all nodes first
        for node_id in tree.expand_tree():
            node = tree[node_id]
            parent_id = tree.parent(node_id)
            parent_id = parent_id.identifier if parent_id else None

            mirrored.create_node(
                tag=node.tag,
                identifier=node.identifier,
                parent=parent_id,
                data=node.data,
            )

        # Reverse children order for each node
        for node_id in mirrored.expand_tree():
            children = mirrored.children(node_id)
            if len(children) > 1:
                # Remove and re-add children in reverse order
                child_data = [(child.identifier, child.tag, child.data) for child in children]
                for child in children:
                    mirrored.remove_node(child.identifier)

                for child_id, child_tag, child_data in reversed(child_data):
                    mirrored.create_node(child_tag, child_id, parent=node_id, data=child_data)

        return mirrored

    mirrored = mirror_tree(tree)
    print("🪞 Mirrored tree:")
    mirrored.show()

    print("\n📏 Tree Pruning (Remove nodes below certain depth):")

    def prune_tree(tree, max_depth):
        """Remove all nodes below specified depth."""
        pruned = Tree(tree, deep=True)  # Create a deep copy

        nodes_to_remove = []
        for node_id in pruned.expand_tree():
            if pruned.level(node_id) > max_depth:
                nodes_to_remove.append(node_id)

        for node_id in nodes_to_remove:
            if pruned.contains(node_id):  # Check if node still exists
                pruned.remove_node(node_id)

        return pruned

    pruned = prune_tree(tree, 2)
    print("✂️ Tree pruned to depth 2:")
    pruned.show()

    print("\n🔍 Filter Tree (Keep only nodes matching criteria):")

    def filter_tree(tree, predicate):
        """Keep only nodes that match the predicate."""
        filtered = Tree()

        # First pass: collect nodes that match predicate
        matching_nodes = []
        for node_id in tree.expand_tree():
            node = tree[node_id]
            if predicate(node):
                matching_nodes.append(node_id)

        # Second pass: rebuild tree with matching nodes and their ancestors
        needed_nodes = set()
        for node_id in matching_nodes:
            path = tree.rsearch(node_id)
            needed_nodes.update(path)

        # Build filtered tree
        for node_id in tree.expand_tree():
            if node_id in needed_nodes:
                node = tree[node_id]
                parent = tree.parent(node_id)
                parent_id = parent.identifier if parent and parent.identifier in needed_nodes else None

                filtered.create_node(
                    tag=node.tag,
                    identifier=node.identifier,
                    parent=parent_id,
                    data=node.data,
                )

        return filtered

    # Filter to keep only even numbers
    filtered = filter_tree(tree, lambda node: int(node.tag) % 2 == 0)
    print("🔢 Tree filtered to even numbers (with ancestors):")
    filtered.show()


def demonstrate_tree_comparison():
    """Demonstrate tree comparison algorithms."""
    print("\n" + "=" * 60)
    print("⚖️ TREE COMPARISON ALGORITHMS")
    print("=" * 60)

    # Create two similar trees
    tree1 = Tree()
    tree1.create_node("A", "a")
    tree1.create_node("B", "b", parent="a")
    tree1.create_node("C", "c", parent="a")
    tree1.create_node("D", "d", parent="b")
    tree1.create_node("E", "e", parent="b")

    tree2 = Tree()
    tree2.create_node("A", "a")
    tree2.create_node("B", "b", parent="a")
    tree2.create_node("C", "c", parent="a")
    tree2.create_node("D", "d", parent="b")
    tree2.create_node("F", "f", parent="b")  # Different node

    print("🌳 Tree 1:")
    tree1.show()

    print("\n🌳 Tree 2:")
    tree2.show()

    print("\n🔍 Tree Comparison Analysis:")

    def compare_trees(tree1, tree2):
        """Compare two trees and find differences."""
        nodes1 = {node_id: tree1[node_id].tag for node_id in tree1.expand_tree()}
        nodes2 = {node_id: tree2[node_id].tag for node_id in tree2.expand_tree()}

        common_nodes = set(nodes1.keys()) & set(nodes2.keys())
        only_in_tree1 = set(nodes1.keys()) - set(nodes2.keys())
        only_in_tree2 = set(nodes2.keys()) - set(nodes1.keys())

        structure_matches = True
        for node_id in common_nodes:
            parent1 = tree1.parent(node_id)
            parent2 = tree2.parent(node_id)

            parent1_id = parent1.identifier if parent1 else None
            parent2_id = parent2.identifier if parent2 else None

            if parent1_id != parent2_id:
                structure_matches = False
                break

        return {
            "common_nodes": common_nodes,
            "only_in_tree1": only_in_tree1,
            "only_in_tree2": only_in_tree2,
            "structure_matches": structure_matches,
            "similarity": len(common_nodes) / max(len(nodes1), len(nodes2)),
        }

    comparison = compare_trees(tree1, tree2)

    print(f"   • Common nodes: {sorted(comparison['common_nodes'])}")
    print(f"   • Only in Tree 1: {sorted(comparison['only_in_tree1'])}")
    print(f"   • Only in Tree 2: {sorted(comparison['only_in_tree2'])}")
    print(f"   • Structure matches: {comparison['structure_matches']}")
    print(f"   • Similarity score: {comparison['similarity']: .2%}")


def demonstrate_tree_algorithms_performance():
    """Demonstrate performance characteristics of tree algorithms."""
    print("\n" + "=" * 60)
    print("⚡ ALGORITHM PERFORMANCE ANALYSIS")
    print("=" * 60)

    print("🏗️ Creating large random tree for performance testing...")

    def create_large_random_tree(size=100):
        """Create a large random tree for performance testing."""
        tree = Tree()
        tree.create_node("Root", "0")

        for i in range(1, size):
            # Choose random parent from existing nodes
            existing_nodes = list(tree.expand_tree())
            parent_id = random.choice(existing_nodes)
            tree.create_node(f"Node_{i}", str(i), parent=parent_id)

        return tree

    large_tree = create_large_random_tree(50)  # Smaller for demo

    print("📊 Large tree statistics:")
    print(f"   • Nodes: {large_tree.size()}")
    print(f"   • Depth: {large_tree.depth()}")
    print(f"   • Leaves: {len(large_tree.leaves())}")

    import time

    print("\n⏱️ Performance benchmarks:")

    # Benchmark traversal
    start_time = time.time()
    all_nodes = list(large_tree.expand_tree())
    traversal_time = time.time() - start_time
    print(f"   • Full traversal: {traversal_time * 1000: .2f}ms ({len(all_nodes)} nodes)")

    # Benchmark search
    start_time = time.time()
    target_node = random.choice(all_nodes)
    path = list(large_tree.rsearch(target_node))
    search_time = time.time() - start_time
    print(f"   • Path search: {search_time * 1000: .2f}ms (path length: {len(path)})")

    # Benchmark filtering
    start_time = time.time()
    leaves = large_tree.leaves()
    filter_time = time.time() - start_time
    print(f"   • Find leaves: {filter_time * 1000: .2f}ms ({len(leaves)} leaves)")

    print("\n💡 Performance Tips:")
    print("   • Use expand_tree() for bulk operations")
    print("   • Cache frequently accessed paths")
    print("   • Consider tree depth when designing algorithms")
    print("   • Use subtree() for isolated operations")


def main():
    """Main function demonstrating all tree algorithms."""
    print("🧮 Welcome to the TreeLib Algorithms Example!")
    print("This example demonstrates advanced tree algorithms and operations.")

    demonstrate_traversal_algorithms()
    demonstrate_tree_analysis()
    demonstrate_path_finding()
    demonstrate_tree_transformations()
    demonstrate_tree_comparison()
    demonstrate_tree_algorithms_performance()

    print("\n" + "=" * 60)
    print("🎉 TREE ALGORITHMS EXAMPLES COMPLETED!")
    print("=" * 60)
    print("You've learned about:")
    print("  • Tree traversal algorithms (DFS, BFS, custom)")
    print("  • Tree analysis and metrics calculation")
    print("  • Path finding and navigation algorithms")
    print("  • Tree transformation operations")
    print("  • Tree comparison and similarity analysis")
    print("  • Performance characteristics and optimization")
    print("\n🚀 Next steps:")
    print("  • Implement your own tree algorithms")
    print("  • Optimize for your specific use cases")
    print("  • Combine multiple algorithms for complex operations")
    print("  • Consider memory and time complexity in your designs")
    print("=" * 60)


if __name__ == "__main__":
    main()

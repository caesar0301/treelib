#!/usr/bin/env python
"""
JSON Trees Example - Import/Export trees from/to JSON

This example demonstrates how to:
- Export trees to JSON format
- Import trees from JSON data
- Work with JSON from external sources
- Handle complex data structures in JSON
- Convert between different JSON schemas

Use cases:
- Saving tree state to files
- API data integration
- Data exchange between applications
- Configuration management

Author: treelib contributors
"""

import json
import tempfile

from treelib import Tree


def create_sample_menu_tree():
    """Create a sample restaurant menu tree structure."""
    tree = Tree()

    # Root
    tree.create_node(
        "🍽️ Restaurant Menu",
        "menu",
        data={"type": "menu", "currency": "USD", "last_updated": "2023-12-01"},
    )

    # Main categories
    categories = [
        {
            "tag": "🍕 Pizza",
            "id": "pizza",
            "data": {"category": "main", "preparation_time": "15-20 min"},
        },
        {
            "tag": "🍝 Pasta",
            "id": "pasta",
            "data": {"category": "main", "preparation_time": "12-15 min"},
        },
        {
            "tag": "🥗 Salads",
            "id": "salads",
            "data": {"category": "side", "preparation_time": "5-8 min"},
        },
        {
            "tag": "🍰 Desserts",
            "id": "desserts",
            "data": {"category": "dessert", "preparation_time": "3-5 min"},
        },
        {
            "tag": "🥤 Beverages",
            "id": "beverages",
            "data": {"category": "drink", "preparation_time": "1-2 min"},
        },
    ]

    for cat in categories:
        tree.create_node(cat["tag"], cat["id"], parent="menu", data=cat["data"])

    # Pizza items
    pizza_items = [
        {
            "tag": "🍕 Margherita",
            "id": "margherita",
            "data": {
                "price": 12.99,
                "ingredients": ["tomato", "mozzarella", "basil"],
                "vegetarian": True,
            },
        },
        {
            "tag": "🍕 Pepperoni",
            "id": "pepperoni",
            "data": {
                "price": 15.99,
                "ingredients": ["tomato", "mozzarella", "pepperoni"],
                "vegetarian": False,
            },
        },
        {
            "tag": "🍕 Hawaiian",
            "id": "hawaiian",
            "data": {
                "price": 16.99,
                "ingredients": ["tomato", "mozzarella", "ham", "pineapple"],
                "vegetarian": False,
            },
        },
    ]

    for item in pizza_items:
        tree.create_node(item["tag"], item["id"], parent="pizza", data=item["data"])

    # Pasta items
    pasta_items = [
        {
            "tag": "🍝 Spaghetti Carbonara",
            "id": "carbonara",
            "data": {
                "price": 14.99,
                "ingredients": ["spaghetti", "eggs", "bacon", "parmesan"],
                "vegetarian": False,
            },
        },
        {
            "tag": "🍝 Penne Arrabbiata",
            "id": "arrabbiata",
            "data": {
                "price": 13.99,
                "ingredients": ["penne", "tomato", "chili", "garlic"],
                "vegetarian": True,
            },
        },
    ]

    for item in pasta_items:
        tree.create_node(item["tag"], item["id"], parent="pasta", data=item["data"])

    # Salad items
    salad_items = [
        {
            "tag": "🥗 Caesar Salad",
            "id": "caesar",
            "data": {
                "price": 9.99,
                "ingredients": ["lettuce", "croutons", "parmesan", "caesar_dressing"],
                "vegetarian": True,
            },
        },
        {
            "tag": "🥗 Greek Salad",
            "id": "greek",
            "data": {
                "price": 10.99,
                "ingredients": ["lettuce", "tomato", "cucumber", "olives", "feta"],
                "vegetarian": True,
            },
        },
    ]

    for item in salad_items:
        tree.create_node(item["tag"], item["id"], parent="salads", data=item["data"])

    return tree


def demonstrate_basic_json_export():
    """Demonstrate basic JSON export functionality."""
    print("=" * 60)
    print("📤 BASIC JSON EXPORT")
    print("=" * 60)

    tree = create_sample_menu_tree()

    print("🍽️ Original menu tree:")
    tree.show(line_type="ascii-em")

    print("\n📋 Exporting tree to JSON:")
    json_output = tree.to_json()

    # Pretty print the JSON
    json_data = json.loads(json_output)
    pretty_json = json.dumps(json_data, indent=2, ensure_ascii=False)

    print("📄 JSON representation:")
    print(pretty_json[:500] + "..." if len(pretty_json) > 500 else pretty_json)

    print("\n📊 JSON statistics:")
    print(f"   • JSON length: {len(json_output): , } characters")
    print(f"   • Number of nodes in JSON: {len(json_data)}")


def demonstrate_json_import():
    """Demonstrate importing trees from JSON."""
    print("\n" + "=" * 60)
    print("📥 JSON IMPORT AND RECONSTRUCTION")
    print("=" * 60)

    # Create original tree
    original_tree = create_sample_menu_tree()

    print("🔄 Steps: Export → Import → Verify")

    # Export to JSON
    json_data = original_tree.to_json()
    print("   ✅ Step 1: Exported to JSON")

    # Parse JSON and reconstruct tree from dict format
    tree_dict = json.loads(json_data)
    reconstructed_tree = Tree()

    def parse_dict_node(node_data, parent_id=None):
        """Recursively parse dictionary format into tree nodes."""
        if isinstance(node_data, str):
            # Simple string node
            node_id = f"node_{len(reconstructed_tree._nodes)}"
            reconstructed_tree.create_node(tag=node_data, identifier=node_id, parent=parent_id)
            return

        elif isinstance(node_data, dict):
            # Dictionary node with potential children
            for tag, content in node_data.items():
                node_id = f"node_{len(reconstructed_tree._nodes)}"
                reconstructed_tree.create_node(tag=tag, identifier=node_id, parent=parent_id)

                if isinstance(content, dict) and "children" in content:
                    # Process children
                    for child in content["children"]:
                        parse_dict_node(child, node_id)

    # Start parsing from root
    for root_tag, root_content in tree_dict.items():
        root_id = "root"
        reconstructed_tree.create_node(tag=root_tag, identifier=root_id)

        if isinstance(root_content, dict) and "children" in root_content:
            for child in root_content["children"]:
                parse_dict_node(child, root_id)
        break  # Only process first root

    print("   ✅ Step 2: Reconstructed tree from JSON")

    print("\n🌳 Reconstructed tree:")
    reconstructed_tree.show(line_type="ascii-em")

    # Verify they're the same
    print("\n🔍 Verification:")
    print(f"   • Original size: {original_tree.size()}")
    print(f"   • Reconstructed size: {reconstructed_tree.size()}")
    print(f"   • Sizes match: {original_tree.size() == reconstructed_tree.size()}")


def demonstrate_custom_json_schema():
    """Demonstrate working with custom JSON schemas."""
    print("\n" + "=" * 60)
    print("🔧 CUSTOM JSON SCHEMAS")
    print("=" * 60)

    # Create a simple tree
    tree = Tree()
    tree.create_node("📂 Project", "project", data={"type": "folder", "created": "2023-01-01"})
    tree.create_node(
        "📁 src",
        "src",
        parent="project",
        data={"type": "folder", "created": "2023-01-02"},
    )
    tree.create_node(
        "📄 main.py",
        "main",
        parent="src",
        data={"type": "file", "size": 1024, "language": "python"},
    )
    tree.create_node(
        "📄 utils.py",
        "utils",
        parent="src",
        data={"type": "file", "size": 512, "language": "python"},
    )

    print("📂 Project tree:")
    tree.show()

    print("\n🔄 Converting to custom JSON schema:")

    def tree_to_custom_json(tree):
        """Convert tree to a custom nested JSON format."""

        def node_to_dict(node_id):
            node = tree[node_id]
            result = {
                "name": node.tag,
                "id": node.identifier,
                "metadata": node.data or {},
            }

            children = tree.children(node_id)
            if children:
                result["children"] = [node_to_dict(child.identifier) for child in children]

            return result

        if tree.root:
            return node_to_dict(tree.root)
        return {}

    custom_json = tree_to_custom_json(tree)
    print("📄 Custom JSON format:")
    print(json.dumps(custom_json, indent=2, ensure_ascii=False))

    print("\n🔄 Converting custom JSON back to tree:")

    def custom_json_to_tree(json_data):
        """Convert custom JSON format back to tree."""
        tree = Tree()

        def add_node(node_data, parent_id=None):
            node_id = node_data["id"]
            tree.create_node(
                tag=node_data["name"],
                identifier=node_id,
                parent=parent_id,
                data=node_data.get("metadata"),
            )

            for child_data in node_data.get("children", []):
                add_node(child_data, node_id)

        add_node(json_data)
        return tree

    restored_tree = custom_json_to_tree(custom_json)
    print("🌳 Restored tree:")
    restored_tree.show()


def demonstrate_real_world_json():
    """Demonstrate working with real-world JSON data."""
    print("\n" + "=" * 60)
    print("🌍 REAL-WORLD JSON INTEGRATION")
    print("=" * 60)

    # Simulate API response data
    api_response = {
        "company": {
            "name": "TechCorp Inc.",
            "departments": [
                {
                    "name": "Engineering",
                    "manager": "Alice Johnson",
                    "teams": [
                        {
                            "name": "Frontend Team",
                            "lead": "Bob Smith",
                            "members": ["Carol Wilson", "Dave Brown"],
                        },
                        {
                            "name": "Backend Team",
                            "lead": "Eve Davis",
                            "members": ["Frank Miller", "Grace Lee"],
                        },
                    ],
                },
                {
                    "name": "Sales",
                    "manager": "Henry Adams",
                    "teams": [
                        {
                            "name": "Enterprise Sales",
                            "lead": "Ivy Chen",
                            "members": ["Jack White", "Kelly Green"],
                        }
                    ],
                },
            ],
        }
    }

    print("📡 Simulated API response:")
    print(json.dumps(api_response, indent=2)[:300] + "...")

    print("\n🔄 Converting API data to tree structure:")

    def api_to_tree(data):
        """Convert API response to tree structure."""
        tree = Tree()

        # Add company root
        company = data["company"]
        tree.create_node(
            f"🏢 {company['name']}",
            "company",
            data={"type": "company", "name": company["name"]},
        )

        # Add departments
        for dept_idx, dept in enumerate(company["departments"]):
            dept_id = f"dept_{dept_idx}"
            tree.create_node(
                f"🏬 {dept['name']} (Manager: {dept['manager']})",
                dept_id,
                parent="company",
                data={"type": "department", "manager": dept["manager"]},
            )

            # Add teams
            for team_idx, team in enumerate(dept["teams"]):
                team_id = f"team_{dept_idx}_{team_idx}"
                tree.create_node(
                    f"👥 {team['name']} (Lead: {team['lead']})",
                    team_id,
                    parent=dept_id,
                    data={"type": "team", "lead": team["lead"]},
                )

                # Add team members
                for member_idx, member in enumerate(team["members"]):
                    member_id = f"member_{dept_idx}_{team_idx}_{member_idx}"
                    tree.create_node(
                        f"👤 {member}",
                        member_id,
                        parent=team_id,
                        data={"type": "employee", "name": member},
                    )

        return tree

    org_tree = api_to_tree(api_response)

    print("🌳 Organization tree from API data:")
    org_tree.show(line_type="ascii-em")

    print("\n📊 Organization statistics:")
    dept_count = sum(
        1 for nid in org_tree.expand_tree() if org_tree[nid].data and org_tree[nid].data.get("type") == "department"
    )
    team_count = sum(
        1 for nid in org_tree.expand_tree() if org_tree[nid].data and org_tree[nid].data.get("type") == "team"
    )
    employee_count = sum(
        1 for nid in org_tree.expand_tree() if org_tree[nid].data and org_tree[nid].data.get("type") == "employee"
    )

    print(f"   • Departments: {dept_count}")
    print(f"   • Teams: {team_count}")
    print(f"   • Employees: {employee_count}")


def demonstrate_json_file_operations():
    """Demonstrate saving/loading JSON files."""
    print("\n" + "=" * 60)
    print("💾 JSON FILE OPERATIONS")
    print("=" * 60)

    tree = create_sample_menu_tree()

    print("💾 Saving tree to JSON file:")

    # Save to temporary file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp_file:
        json_file_path = tmp_file.name
        json_data = tree.to_json()

        # Pretty format for file
        parsed_data = json.loads(json_data)
        tmp_file.write(json.dumps(parsed_data, indent=2, ensure_ascii=False))

    print(f"   ✅ Saved to: {json_file_path}")

    print("\n📖 Loading tree from JSON file:")

    # Load from file
    with open(json_file_path, "r", encoding="utf-8") as f:
        loaded_data = json.load(f)

    print(f"   ✅ Loaded {len(loaded_data)} nodes from file")

    # Display first few nodes
    print("\n📋 First few nodes from file:")

    def display_nodes(data, prefix="", count=[0]):
        """Recursively display nodes from JSON data."""
        if count[0] >= 3:
            return

        if isinstance(data, dict):
            for tag, content in data.items():
                if count[0] < 3:
                    print(f"   {prefix}• {tag}")
                    count[0] += 1
                    if isinstance(content, dict) and "children" in content:
                        for child in content["children"][:2]:  # Limit children shown
                            display_nodes(child, prefix + "  ", count)
                        if len(content["children"]) > 2:
                            print(f"   {prefix}  ... and more children")
        elif isinstance(data, str):
            if count[0] < 3:
                print(f"   {prefix}• {data}")
                count[0] += 1

    display_nodes(loaded_data)

    # Cleanup
    import os

    try:
        os.remove(json_file_path)
        print("\n🧹 Cleaned up temporary file")
    except BaseException:
        pass


def main():
    """Main function demonstrating all JSON operations."""
    print("📄 Welcome to the TreeLib JSON Integration Example!")
    print("This example shows how to work with JSON data and trees.")

    demonstrate_basic_json_export()
    demonstrate_json_import()
    demonstrate_custom_json_schema()
    demonstrate_real_world_json()
    demonstrate_json_file_operations()

    print("\n" + "=" * 60)
    print("🎉 JSON INTEGRATION EXAMPLES COMPLETED!")
    print("=" * 60)
    print("You've learned how to:")
    print("  • Export trees to JSON format")
    print("  • Import and reconstruct trees from JSON")
    print("  • Work with custom JSON schemas")
    print("  • Integrate with real-world API data")
    print("  • Save and load JSON files")
    print("\n💡 Use cases:")
    print("  • Configuration management")
    print("  • API data visualization")
    print("  • Data persistence")
    print("  • Cross-application data exchange")
    print("=" * 60)


if __name__ == "__main__":
    main()

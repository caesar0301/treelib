#!/usr/bin/env python
"""
Save Tree to File Example - Demonstrate tree export capabilities

This example shows how to:
- Save trees to text files
- Export trees in different formats
- Load and manipulate saved tree data
- Export to various file formats (JSON, Graphviz DOT)

Author: treelib contributors
"""

import os
import tempfile

from treelib import Tree


def create_sample_tree():
    """
    Create a sample tree for demonstration.

    Returns:
        Tree: A populated tree
    """
    tree = Tree()

    # Create a simple organizational structure
    tree.create_node("CEO", "ceo")
    tree.create_node("CTO", "cto", parent="ceo")
    tree.create_node("CFO", "cfo", parent="ceo")
    tree.create_node("VP Engineering", "vp_eng", parent="cto")
    tree.create_node("VP Finance", "vp_fin", parent="cfo")
    tree.create_node("Senior Developer", "dev1", parent="vp_eng")
    tree.create_node("Junior Developer", "dev2", parent="vp_eng")
    tree.create_node("Accountant", "acc1", parent="vp_fin")

    return tree


def demonstrate_text_export():
    """Demonstrate saving tree to text file."""
    print("=" * 60)
    print("📄 SAVING TREE TO TEXT FILE")
    print("=" * 60)

    tree = create_sample_tree()

    print("🌳 Original tree structure:")
    tree.show()

    # Save to text file
    filename = "organization_tree.txt"
    tree.save2file(filename)

    print(f"\n💾 Tree saved to '{filename}'")

    # Display file contents
    print("\n📖 File contents:")
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
            print(content)
    except FileNotFoundError:
        print(f"❌ Error: Could not read file '{filename}'")

    # Clean up
    try:
        os.remove(filename)
        print(f"🧹 Cleaned up temporary file '{filename}'")
    except FileNotFoundError:
        pass


def demonstrate_json_export():
    """Demonstrate exporting tree to JSON format."""
    print("\n" + "=" * 60)
    print("📄 EXPORTING TREE TO JSON")
    print("=" * 60)

    tree = create_sample_tree()

    # Export to JSON
    json_output = tree.to_json()
    print("📋 Tree as JSON:")
    print(json_output)

    # Save JSON to file
    json_filename = "organization_tree.json"
    with open(json_filename, "w", encoding="utf-8") as f:
        f.write(json_output)

    print(f"\n💾 JSON saved to '{json_filename}'")

    # Clean up
    try:
        os.remove(json_filename)
        print(f"🧹 Cleaned up temporary file '{json_filename}'")
    except FileNotFoundError:
        pass


def demonstrate_dict_export():
    """Demonstrate converting tree to dictionary format."""
    print("\n" + "=" * 60)
    print("📄 CONVERTING TREE TO DICTIONARY")
    print("=" * 60)

    tree = create_sample_tree()

    # Convert to dictionary
    tree_dict = tree.to_dict()
    print("📋 Tree as dictionary:")
    print(tree_dict)

    # Convert to dictionary with data
    print("\n📋 Tree as dictionary (with custom data):")
    # Add some custom data to nodes
    tree["ceo"].data = {"salary": 200000, "department": "Executive"}
    tree["cto"].data = {"salary": 150000, "department": "Technology"}
    tree["cfo"].data = {"salary": 140000, "department": "Finance"}

    tree_dict_with_data = tree.to_dict(with_data=True)
    print(tree_dict_with_data)


def demonstrate_custom_formatting():
    """Demonstrate custom tree formatting and export."""
    print("\n" + "=" * 60)
    print("📄 CUSTOM TREE FORMATTING")
    print("=" * 60)

    tree = create_sample_tree()

    # Add custom data to demonstrate data property display
    class JobInfo:
        def __init__(self, title, level):
            self.title = title
            self.level = level

    tree["ceo"].data = JobInfo("Chief Executive Officer", 1)
    tree["cto"].data = JobInfo("Chief Technology Officer", 2)
    tree["cfo"].data = JobInfo("Chief Financial Officer", 2)
    tree["vp_eng"].data = JobInfo("Vice President of Engineering", 3)
    tree["vp_fin"].data = JobInfo("Vice President of Finance", 3)
    tree["dev1"].data = JobInfo("Senior Developer", 4)
    tree["dev2"].data = JobInfo("Junior Developer", 4)
    tree["acc1"].data = JobInfo("Accountant", 4)

    print("🌳 Tree with custom formatting:")

    # Use show() with custom parameters
    output = tree.show(
        idhidden=False,  # Show node IDs
        line_type="ascii-em",  # Fancy line style
        data_property="title",  # Show custom data property
        stdout=False,  # Return as string instead of printing
    )
    print(output)

    # Save formatted output to file
    formatted_filename = "formatted_tree.txt"
    tree.save2file(formatted_filename, idhidden=False, line_type="ascii-em", data_property="title")

    print(f"\n💾 Formatted tree saved to '{formatted_filename}'")

    # Clean up
    try:
        os.remove(formatted_filename)
        print(f"🧹 Cleaned up temporary file '{formatted_filename}'")
    except FileNotFoundError:
        pass


def demonstrate_graphviz_export():
    """Demonstrate exporting tree to Graphviz DOT format."""
    print("\n" + "=" * 60)
    print("📄 EXPORTING TO GRAPHVIZ DOT FORMAT")
    print("=" * 60)

    tree = create_sample_tree()

    # Create temporary file for DOT output
    with tempfile.NamedTemporaryFile(mode="w", suffix=".dot", delete=False) as tmp_file:
        dot_filename = tmp_file.name

    print("🌳 Exporting tree to Graphviz DOT format...")
    tree.to_graphviz(filename=dot_filename, shape="box")

    print(f"💾 DOT file saved to '{dot_filename}'")

    # Display DOT file contents
    print("\n📖 DOT file contents:")
    try:
        with open(dot_filename, "r", encoding="utf-8") as f:
            content = f.read()
            print(content)
    except FileNotFoundError:
        print(f"❌ Error: Could not read DOT file '{dot_filename}'")

    print("\n💡 Tip: You can use Graphviz tools to convert this to SVG, PNG, or PDF:")
    print(f"    dot -Tsvg {dot_filename} -o tree.svg")
    print(f"    dot -Tpng {dot_filename} -o tree.png")

    # Clean up
    try:
        os.remove(dot_filename)
        print(f"\n🧹 Cleaned up temporary file '{dot_filename}'")
    except FileNotFoundError:
        pass


def main():
    """Main function demonstrating tree export capabilities."""
    print("💾 Welcome to the TreeLib Tree Export Example!")
    print("This example shows different ways to save and export trees.")

    # Run all demonstrations
    demonstrate_text_export()
    demonstrate_json_export()
    demonstrate_dict_export()
    demonstrate_custom_formatting()
    demonstrate_graphviz_export()

    print("\n" + "=" * 60)
    print("🎉 All export examples completed!")
    print("💡 Try experimenting with different formatting options and export methods.")
    print("=" * 60)


if __name__ == "__main__":
    main()

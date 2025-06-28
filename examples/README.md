# TreeLib Examples

This directory contains comprehensive examples demonstrating all aspects of the TreeLib library. These examples are designed to help you learn TreeLib from basics to advanced usage.

## 🚀 Quick Start

**New to TreeLib?** Start here:
1. [`getting_started.py`](#getting_started) - Complete beginner's tutorial
2. [`family_tree.py`](#family_tree) - Real-world tree operations
3. [`save_tree2file.py`](#save_tree2file) - Export and save trees

## 📚 Example Overview

### 🌱 Getting Started
**File:** `getting_started.py`
**Perfect for:** Complete beginners to TreeLib

A comprehensive tutorial covering all the basics:
- Creating trees and nodes
- Tree navigation and traversal
- Searching and filtering
- Tree modifications
- Working with custom data
- Display and export options

**Run it:**
```bash
python examples/getting_started.py
```

### 👨‍👩‍👧‍👦 Family Tree
**File:** `family_tree.py`
**Perfect for:** Understanding real-world tree operations

Demonstrates TreeLib features using a family tree:
- Different display formats
- Tree traversal methods
- Filtering and searching
- Subtree operations
- Tree modifications
- Advanced features (JSON, paths, etc.)

**Run it:**
```bash
python examples/family_tree.py
```

### 💾 Save Tree to File
**File:** `save_tree2file.py`
**Perfect for:** Learning export and persistence

Shows different ways to export trees:
- Text file export
- JSON export
- Dictionary conversion
- Custom formatting
- Graphviz DOT format

**Run it:**
```bash
python examples/save_tree2file.py
```

### 📁 Folder Tree Scanner
**File:** `folder_tree.py`
**Perfect for:** Real file system applications

Advanced file system scanner with:
- Command-line interface
- Real directory scanning
- File filtering by patterns
- Performance optimization
- Multiple export formats
- Error handling

**Run it:**
```bash
# Demo mode
python examples/folder_tree.py --demo

# Scan current directory for Python files
python examples/folder_tree.py . "*.py" --max-depth 3

# Scan with file sizes
python examples/folder_tree.py /path/to/scan "*" --show-sizes --limit 100

# Export to JSON
python examples/folder_tree.py . "*.txt" --export json --output my_tree.json
```

### 🌳 Recursive Directory Generator
**File:** `recursive_dirtree.py`
**Perfect for:** Understanding programmatic tree creation

Simulates directory structures programmatically:
- Recursive tree generation
- Custom node data (files, sizes, etc.)
- Tree analysis and statistics
- Performance testing
- Large tree handling

**Run it:**
```bash
python examples/recursive_dirtree.py
```

### 📄 JSON Trees
**File:** `json_trees.py`
**Perfect for:** API integration and data exchange

Comprehensive JSON integration:
- Export trees to JSON
- Import trees from JSON
- Custom JSON schemas
- Real-world API data integration
- File operations with JSON

**Run it:**
```bash
python examples/json_trees.py
```

### 🧮 Tree Algorithms
**File:** `tree_algorithms.py`
**Perfect for:** Advanced tree operations and algorithms

Advanced algorithmic operations:
- Tree traversal algorithms (DFS, BFS, custom)
- Tree analysis and metrics
- Path finding algorithms
- Tree transformations
- Tree comparison
- Performance analysis

**Run it:**
```bash
python examples/tree_algorithms.py
```

## 📋 Example Categories

### 🔰 Beginner Examples
- `getting_started.py` - Complete tutorial
- `family_tree.py` - Basic operations
- `save_tree2file.py` - Export basics

### 🏗️ Real-World Applications
- `folder_tree.py` - File system scanner
- `json_trees.py` - API integration
- `recursive_dirtree.py` - Programmatic generation

### 🚀 Advanced Topics
- `tree_algorithms.py` - Algorithms and analysis

## 🎯 Use Case Guide

### I want to...

**Learn TreeLib basics**
→ Start with `getting_started.py`

**Build a file/folder visualizer**
→ Check out `folder_tree.py`

**Work with JSON/API data**
→ See `json_trees.py`

**Export trees to files**
→ Look at `save_tree2file.py`

**Implement tree algorithms**
→ Study `tree_algorithms.py`

**Create large test trees**
→ Use `recursive_dirtree.py`

**Understand all features**
→ Run `family_tree.py`

## 🚀 Running Examples

### Prerequisites
Make sure TreeLib is in your Python path:

```bash
# If running from the treelib directory
PYTHONPATH=. python examples/example_name.py

# Or if TreeLib is installed
python examples/example_name.py
```

### Interactive Learning
Each example includes:
- ✨ **Rich output** with emojis and formatting
- 📖 **Explanatory comments** throughout the code
- 🎯 **Focused demonstrations** of specific features
- 💡 **Tips and best practices**

## 🔧 Customization

All examples are designed to be:
- **Modifiable** - Easy to adapt for your needs
- **Educational** - Clear, commented code
- **Practical** - Real-world applicable patterns

Feel free to modify any example to experiment with different:
- Tree structures
- Data types
- Algorithms
- Export formats
- Display options

## 📖 Learning Path

**Recommended order for learning:**

1. **`getting_started.py`** - Learn the fundamentals
2. **`family_tree.py`** - See practical usage
3. **`save_tree2file.py`** - Understand export options
4. **`folder_tree.py`** - Real-world application
5. **`json_trees.py`** - Data integration
6. **`recursive_dirtree.py`** - Programmatic creation
7. **`tree_algorithms.py`** - Advanced algorithms

## 🆘 Need Help?

- **📚 Documentation:** Check the main TreeLib documentation
- **🐛 Issues:** Report bugs in the main repository
- **💡 Questions:** Look at the example code comments
- **🔧 Customization:** Modify examples to fit your needs

## 🎉 Contributing

Found an issue or want to improve an example?
- Fix bugs in existing examples
- Add new example use cases
- Improve documentation
- Enhance code clarity

Remember: Examples should be **educational**, **practical**, and **easy to understand**!

---

**Happy tree building! 🌳** 
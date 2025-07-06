# Treelib Comprehensive Testing Suite

This directory contains a comprehensive test suite for the treelib library, providing thorough coverage of all Tree and Node class functionality.

## Test Structure

### Core Test Files

- **`test_tree.py`** - Original test file enhanced with additional comprehensive tests for Tree class
- **`test_node.py`** - Original test file for Node class functionality

### Additional Test Modules

- **`test_tree_comprehensive.py`** - Additional comprehensive tests for Tree methods and edge cases
- **`test_tree_io.py`** - Focused tests for I/O operations (save2file, to_json, to_graphviz, from_map)
- **`test_tree_edge_cases.py`** - Edge cases, boundary conditions, and error handling tests
- **`test_node_comprehensive.py`** - Comprehensive tests for Node class methods and properties
- **`test_tree_performance.py`** - Performance benchmarks and stress tests

## Running Tests

### Run Individual Test Modules
```bash
# Original tests
python -m unittest tests.test_tree
python -m unittest tests.test_node

# New comprehensive tests
python -m unittest tests.test_tree_comprehensive
python -m unittest tests.test_tree_io
python -m unittest tests.test_tree_edge_cases
python -m unittest tests.test_node_comprehensive
python -m unittest tests.test_tree_performance
```

### Run Specific Test Cases
```bash
python -m unittest tests.test_tree.TreeCase.test_nodes
python -m unittest tests.test_tree_io.TreeIOTestCase.test_save2file_comprehensive
```

## Test Coverage Areas

### Tree Class Coverage

#### Core Functionality
- Tree creation and initialization
- Node creation and management
- Tree traversal (depth-first, breadth-first, zigzag)
- Tree modification (add, remove, move nodes)
- Tree relationships (parent, children, siblings, ancestors)

#### I/O Operations
- File output (`save2file`)
- JSON serialization (`to_json`, `to_dict`)
- Graphviz export (`to_graphviz`)
- Tree construction from mappings (`from_map`)

#### Advanced Features
- Subtree operations (`subtree`, `remove_subtree`)
- Tree merging and pasting
- Node filtering (`filter_nodes`)
- Tree metrics (size, depth, levels)
- Display formatting with various options

#### Edge Cases & Error Handling
- Empty trees
- Single-node trees
- Very large trees (performance)
- Very deep trees
- Very wide trees
- Unicode content
- Special characters
- Invalid operations
- Memory management

### Node Class Coverage

#### Core Properties
- Node creation and initialization
- Identifier and tag management
- Data handling (all data types)
- Expansion state

#### Relationships
- Parent-child relationships
- Multi-tree membership
- Pointer management
- Tree-specific operations

#### Advanced Features
- Node comparison and sorting
- Pointer cloning and resetting
- Legacy compatibility methods
- String representation

## Test Categories

### 1. Functional Tests
Verify that all methods work correctly with valid inputs and expected use cases.

### 2. Edge Case Tests
Test boundary conditions, unusual inputs, and corner cases.

### 3. Error Handling Tests
Verify proper exception handling for invalid operations.

### 4. Performance Tests
Benchmark operations with large datasets and measure execution time.

### 5. Integration Tests
Test interactions between different Tree and Node methods.

### 6. Unicode & Encoding Tests
Ensure proper handling of international characters and encodings.

## Test Data Scenarios

### Tree Structures
- Empty trees
- Single-node trees
- Linear chains (very deep)
- Wide trees (many children)
- Balanced trees
- Unbalanced trees
- Trees with mixed data types

### Content Types
- Simple strings
- Unicode text (multiple scripts)
- Complex nested data structures
- Large data payloads
- None/null values
- Special characters

### Operations
- CRUD operations on nodes
- Tree traversal and search
- Tree transformation
- Serialization/deserialization
- Display and formatting

## Performance Benchmarks

The performance tests verify that operations complete within reasonable time limits:

- Tree creation: < 5 seconds for 10,000 nodes
- Tree traversal: < 5 seconds for 10,000+ nodes
- Node lookup: < 5 seconds for 5,000 lookups
- Tree modification: < 5 seconds for 1,000 operations

## Extending the Tests

### Adding New Test Cases

1. Choose the appropriate test module based on functionality
2. Follow the existing naming convention: `test_<feature>_<scenario>`
3. Include comprehensive docstrings
4. Test both success and failure cases
5. Add performance considerations for large datasets

### Creating New Test Modules

1. Follow the naming convention: `test_<component>_<focus>.py`
2. Include comprehensive docstrings and module header
3. Inherit from `unittest.TestCase`
4. Include setUp and tearDown methods

## Dependencies

Most tests use only Python standard library modules. Some optional dependencies:

- `memory_profiler` - For memory profiling in performance tests (optional)
- `unittest.mock` - For mocking I/O operations (standard library)

## Contributing

When adding new functionality to treelib:

1. Add corresponding tests to the appropriate test module
2. Ensure tests cover both success and failure cases
3. Include edge cases and boundary conditions
4. Add performance tests for operations that could be slow
5. Update this documentation if adding new test modules

## Test Quality Guidelines

- **Comprehensive**: Test all code paths and edge cases
- **Isolated**: Each test should be independent
- **Deterministic**: Tests should produce consistent results
- **Fast**: Individual tests should complete quickly
- **Readable**: Test code should be clear and well-documented
- **Maintainable**: Tests should be easy to update as code evolves

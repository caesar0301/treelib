#!/usr/bin/env python
"""
Folder Tree Scanner - Real file system tree visualization

This example demonstrates how to:
- Scan real file system directories
- Create trees from existing folder structures
- Filter files by patterns
- Handle large directory structures efficiently
- Export file system trees to various formats

Usage:
    python folder_tree.py [path] [pattern] [options]

Examples:
    python folder_tree.py /home/user "*.py" --max-depth 3
    python folder_tree.py ./documents "*.pdf" --export json
    python folder_tree.py . "*" --limit 100

Author: treelib contributors (originally by holger)
"""

import argparse
import fnmatch
import hashlib
import sys
import time
from pathlib import Path
from typing import Optional

from treelib import Tree


class FileSystemScanner:
    """
    A class to scan file system directories and create tree representations.
    """

    def __init__(
        self,
        max_depth: Optional[int] = None,
        max_files: Optional[int] = None,
        show_hidden: bool = False,
        show_sizes: bool = False,
    ):
        """
        Initialize the scanner with configuration options.

        Args:
            max_depth: Maximum depth to scan (None for unlimited)
            max_files: Maximum number of files to include (None for unlimited)
            show_hidden: Whether to include hidden files/directories
            show_sizes: Whether to calculate and show file sizes
        """
        self.max_depth = max_depth
        self.max_files = max_files
        self.show_hidden = show_hidden
        self.show_sizes = show_sizes

        # Statistics tracking
        self.file_count = 0
        self.dir_count = 0
        self.total_size = 0
        self.errors = []

        # Performance tracking
        self.start_time = None
        self.end_time = None

    def _create_node_id(self, path: str) -> str:
        """
        Create a unique node identifier for a path.

        Args:
            path: File system path

        Returns:
            Unique identifier string
        """
        return hashlib.md5(path.encode("utf-8")).hexdigest()[:12]

    def _should_include(self, path: Path) -> bool:
        """
        Determine if a path should be included in the tree.

        Args:
            path: Path to check

        Returns:
            True if path should be included
        """
        if not self.show_hidden and path.name.startswith("."):
            return False

        return True

    def _get_file_info(self, path: Path) -> dict:
        """
        Get file information including size if requested.

        Args:
            path: File path

        Returns:
            Dictionary with file information
        """
        info = {"name": path.name, "is_dir": path.is_dir(), "path": str(path)}

        if self.show_sizes:
            try:
                if path.is_file():
                    info["size"] = path.stat().st_size
                    self.total_size += info["size"]
                elif path.is_dir():
                    info["size"] = 0  # Directories don't have meaningful size
            except (OSError, PermissionError) as e:
                info["size"] = 0
                self.errors.append(f"Cannot get size for {path}: {e}")

        return info

    def _format_size(self, size_bytes: int) -> str:
        """
        Format file size in human-readable format.

        Args:
            size_bytes: Size in bytes

        Returns:
            Formatted size string
        """
        if size_bytes == 0:
            return "0 B"

        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0

        return f"{size_bytes:.1f} PB"

    def scan_directory(self, root_path: str, pattern: str = "*") -> Tree:
        """
        Scan a directory and create a tree structure.

        Args:
            root_path: Root directory to scan
            pattern: File pattern to match (e.g., "*.py", "*.pdf")

        Returns:
            Tree object representing the directory structure
        """
        self.start_time = time.time()

        root_path = Path(root_path).resolve()

        if not root_path.exists():
            raise FileNotFoundError(f"Path does not exist: {root_path}")

        if not root_path.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {root_path}")

        # Create tree with root node
        tree = Tree()
        root_info = self._get_file_info(root_path)
        root_id = self._create_node_id(str(root_path))

        display_name = root_info["name"] or str(root_path)
        if self.show_sizes:
            display_name = f"📁 {display_name}"

        tree.create_node(tag=display_name, identifier=root_id, data=root_info)

        self.dir_count += 1

        # Scan directory recursively
        self._scan_recursive(tree, root_path, root_id, pattern, 0)

        self.end_time = time.time()
        return tree

    def _scan_recursive(self, tree: Tree, current_path: Path, parent_id: str, pattern: str, depth: int) -> None:
        """
        Recursively scan directories and add nodes to tree.

        Args:
            tree: Tree object to add nodes to
            current_path: Current directory being scanned
            parent_id: Parent node identifier
            pattern: File pattern to match
            depth: Current depth in directory hierarchy
        """
        if self.max_depth is not None and depth >= self.max_depth:
            return

        if self.max_files is not None and self.file_count >= self.max_files:
            return

        try:
            # Get all items in current directory
            items = list(current_path.iterdir())

            # Sort items: directories first, then files, both alphabetically
            directories = []
            files = []

            for item in items:
                if not self._should_include(item):
                    continue

                if item.is_dir():
                    directories.append(item)
                elif item.is_file() and fnmatch.fnmatch(item.name, pattern):
                    files.append(item)

            directories.sort(key=lambda x: x.name.lower())
            files.sort(key=lambda x: x.name.lower())

            # Add directories first
            for directory in directories:
                dir_info = self._get_file_info(directory)
                dir_id = self._create_node_id(str(directory))

                display_name = f"📁 {directory.name}"

                tree.create_node(tag=display_name, identifier=dir_id, parent=parent_id, data=dir_info)

                self.dir_count += 1

                # Recursively scan subdirectory
                self._scan_recursive(tree, directory, dir_id, pattern, depth + 1)

            # Add files
            for file in files:
                if self.max_files is not None and self.file_count >= self.max_files:
                    break

                file_info = self._get_file_info(file)
                file_id = self._create_node_id(str(file))

                display_name = f"📄 {file.name}"
                if self.show_sizes and "size" in file_info:
                    size_str = self._format_size(file_info["size"])
                    display_name = f"📄 {file.name} ({size_str})"

                tree.create_node(
                    tag=display_name,
                    identifier=file_id,
                    parent=parent_id,
                    data=file_info,
                )

                self.file_count += 1

        except PermissionError as e:
            self.errors.append(f"Permission denied: {current_path} - {e}")
        except OSError as e:
            self.errors.append(f"OS error scanning {current_path}: {e}")

    def print_statistics(self) -> None:
        """Print scanning statistics."""
        duration = self.end_time - self.start_time if self.end_time and self.start_time else 0

        print("\n" + "=" * 50)
        print("📊 SCAN STATISTICS")
        print("=" * 50)
        print(f"📁 Directories found: {self.dir_count}")
        print(f"📄 Files found: {self.file_count}")

        if self.show_sizes:
            print(f"💾 Total size: {self._format_size(self.total_size)}")

        print(f"⏱️  Scan time: {duration:.2f} seconds")
        print(f"❌ Errors: {len(self.errors)}")

        if self.errors:
            print("\n🚨 Errors encountered:")
            for error in self.errors[:5]:  # Show first 5 errors
                print(f"   • {error}")
            if len(self.errors) > 5:
                print(f"   ... and {len(self.errors) - 5} more errors")


def demonstrate_scanning():
    """Demonstrate file system scanning with current directory."""
    print("🌳 Welcome to the File System Tree Scanner!")
    print("This example scans real directories and creates tree visualizations.")

    current_dir = Path.cwd()
    print(f"\n📂 Scanning current directory: {current_dir}")

    # Basic scan
    print("\n" + "=" * 50)
    print("📋 BASIC DIRECTORY SCAN")
    print("=" * 50)

    scanner = FileSystemScanner(max_depth=2, max_files=20)
    tree = scanner.scan_directory(str(current_dir), "*.py")

    print(f"🌳 Python files in {current_dir.name} (max depth 2):")
    tree.show(line_type="ascii-em")

    scanner.print_statistics()

    # Enhanced scan with sizes
    print("\n" + "=" * 50)
    print("📋 ENHANCED SCAN WITH FILE SIZES")
    print("=" * 50)

    scanner_with_sizes = FileSystemScanner(max_depth=1, max_files=10, show_sizes=True)
    tree_with_sizes = scanner_with_sizes.scan_directory(str(current_dir), "*")

    print(f"🌳 All files in {current_dir.name} (with sizes, depth 1):")
    tree_with_sizes.show(line_type="ascii-em")

    scanner_with_sizes.print_statistics()


def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(
        description="Scan directories and create tree visualizations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /home/user "*.py" --max-depth 3
  %(prog)s ./documents "*.pdf" --export json
  %(prog)s . "*" --limit 100 --show-sizes
        """,
    )

    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Directory path to scan (default: current directory)",
    )

    parser.add_argument(
        "pattern",
        nargs="?",
        default="*",
        help="File pattern to match (default: all files)",
    )

    parser.add_argument("--max-depth", type=int, help="Maximum depth to scan")

    parser.add_argument("--limit", type=int, help="Maximum number of files to include")

    parser.add_argument(
        "--show-hidden",
        action="store_true",
        help="Include hidden files and directories",
    )

    parser.add_argument("--show-sizes", action="store_true", help="Show file sizes")

    parser.add_argument(
        "--export",
        choices=["json", "txt", "dot"],
        help="Export format (json, txt, or dot)",
    )

    parser.add_argument("--output", help="Output file path (default: print to console)")

    parser.add_argument("--demo", action="store_true", help="Run demonstration with current directory")

    args = parser.parse_args()

    if args.demo:
        demonstrate_scanning()
        return

    # Create scanner with specified options
    scanner = FileSystemScanner(
        max_depth=args.max_depth,
        max_files=args.limit,
        show_hidden=args.show_hidden,
        show_sizes=args.show_sizes,
    )

    try:
        print(f"🔍 Scanning {args.path} for {args.pattern}...")
        tree = scanner.scan_directory(args.path, args.pattern)

        # Display tree
        if not args.export or not args.output:
            print(f"\n🌳 Directory tree for {args.path}:")
            tree.show(line_type="ascii-em")

        # Export if requested
        if args.export:
            output_file = args.output or f"tree_export.{args.export}"

            if args.export == "json":
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(tree.to_json())
                print(f"📄 Exported to JSON: {output_file}")

            elif args.export == "txt":
                tree.save2file(output_file, line_type="ascii-em")
                print(f"📄 Exported to text: {output_file}")

            elif args.export == "dot":
                tree.to_graphviz(filename=output_file, shape="box")
                print(f"📄 Exported to DOT: {output_file}")

        scanner.print_statistics()

    except (FileNotFoundError, NotADirectoryError, PermissionError) as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  Scan interrupted by user")
        sys.exit(1)


if __name__ == "__main__":
    main()

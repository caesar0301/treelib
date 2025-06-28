.PHONY: help install install-dev test test-coverage lint autofix autofix-imports autofix-pep8 autofix-unused format format-check clean build docs
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
POETRY := poetry
DIRS := examples treelib tests

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	$(POETRY) install --only main

install-dev: ## Install development dependencies
	$(POETRY) install

test: install-dev ## Run tests with pytest
	$(POETRY) run pytest

run-examples: install ## Run all example scripts to verify they work correctly
	@echo "Running all example scripts..."
	@echo "🚀 Running getting_started.py..."
	@$(POETRY) run python examples/getting_started.py > /dev/null
	@echo "✅ getting_started.py completed successfully"
	@echo "👨‍👩‍👧‍👦 Running family_tree.py..."
	@$(POETRY) run python examples/family_tree.py > /dev/null
	@echo "✅ family_tree.py completed successfully"
	@echo "💾 Running save_tree2file.py..."
	@$(POETRY) run python examples/save_tree2file.py > /dev/null
	@echo "✅ save_tree2file.py completed successfully"
	@echo "📁 Running folder_tree.py..."
	@$(POETRY) run python examples/folder_tree.py --demo > /dev/null
	@echo "✅ folder_tree.py completed successfully"
	@echo "📄 Running json_trees.py..."
	@$(POETRY) run python examples/json_trees.py > /dev/null
	@echo "✅ json_trees.py completed successfully"
	@echo "🌳 Running recursive_dirtree.py..."
	@$(POETRY) run python examples/recursive_dirtree.py > /dev/null
	@echo "✅ recursive_dirtree.py completed successfully"
	@echo "🧮 Running tree_algorithms.py..."
	@$(POETRY) run python examples/tree_algorithms.py > /dev/null
	@echo "✅ tree_algorithms.py completed successfully"
	@echo "🎉 All examples completed successfully!"

lint: install-dev ## Run linting checks (flake8)
	$(POETRY) run flake8 $(DIRS) --count --select=E9,F63,F7,F82 --ignore=E231 --max-line-length=120 --show-source --statistics

autofix-unused: install-dev ## Remove unused imports and variables
	$(POETRY) run autoflake --remove-all-unused-imports --remove-unused-variables --in-place --recursive $(DIRS)

autofix-imports: install-dev ## Sort and organize imports
	$(POETRY) run isort $(DIRS) --profile black

autofix-pep8: install-dev ## Fix PEP 8 style issues
	$(POETRY) run autopep8 --in-place --recursive --aggressive --aggressive $(DIRS)

autofix: autofix-unused autofix-imports autofix-pep8 format

format: install-dev ## Format code with black
	$(POETRY) run black $(DIRS)

format-check: install-dev ## Check code formatting with black
	$(POETRY) run black --check $(DIRS)

check: lint format-check ## Run all checks (lint + format check)

clean: ## Clean build artifacts and cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: ## Build the package
	$(POETRY) build

docs: ## Build documentation
	@if [ -d "docs" ]; then \
		cd docs && make html; \
	else \
		echo "No docs directory found"; \
	fi
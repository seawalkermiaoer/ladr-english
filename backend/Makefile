# Makefile for common development tasks

# Variables
PYTHON = python
PIP = pip
TEST_DIR = tests

# Default target
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  install     - Install dependencies"
	@echo "  dev-install - Install development dependencies"
	@echo "  run         - Run the application"
	@echo "  test        - Run tests"
	@echo "  coverage    - Run tests with coverage"
	@echo "  clean       - Clean up generated files"

# Install dependencies
.PHONY: install
install:
	$(PIP) install -r requirements/base.txt

# Install development dependencies
.PHONY: dev-install
dev-install:
	$(PIP) install -r requirements/dev.txt

# Run the application
.PHONY: run
run:
	$(PYTHON) -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
.PHONY: test
test:
	$(PYTHON) -m pytest $(TEST_DIR) -v

# Run tests with coverage
.PHONY: coverage
coverage:
	$(PYTHON) -m pytest $(TEST_DIR) --cov=app --cov-report=html --cov-report=term

# Clean up generated files
.PHONY: clean
clean:
	rm -rf __pycache__/
	rm -rf app/__pycache__/
	rm -rf tests/__pycache__/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
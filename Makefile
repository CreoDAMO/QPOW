# Define variables
PYTHON := python3
VENV := qpow-venv
ACTIVATE := . $(VENV)/bin/activate
REQUIREMENTS := requirements.txt
FLAKE8 := flake8
PYTEST := pytest
PYNGUIN := pynguin
DOXYGEN_CONFIG := Doxyfile
COVERAGE_DIR := coverage_html
TEST_OUTPUT_DIR := tests/generated
BLACK := black
ISORT := isort

# Default target
.DEFAULT_GOAL := help

# Help
help:
	@echo "Usage: make <target>"
	@echo ""
	@awk '/^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, substr($$0, index($$0, "## ") + 3)}' $(MAKEFILE_LIST)

# Create virtual environment
venv:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV) || (echo "Error creating virtual environment" && exit 1)

# Ensure virtual environment exists
check-env:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Virtual environment not found. Run 'make venv' first."; \
		exit 1; \
	fi

# Install dependencies
install: venv check-env
	@echo "Installing dependencies..."
	$(ACTIVATE) && pip install -r $(REQUIREMENTS) || (echo "Error installing dependencies" && exit 1)

# Install formatting tools
install-formatters: check-env
	@echo "Installing Black and Isort..."
	$(ACTIVATE) && pip install $(BLACK) $(ISORT) || (echo "Error installing formatters" && exit 1)

# Lint the codebase
lint: check-env install
	@echo "Linting the codebase with flake8..."
	$(ACTIVATE) && $(FLAKE8) . --max-line-length=88 --statistics --verbose || (echo "Linting failed" && exit 1)

# Format code
format: check-env install-formatters
	@echo "Formatting code with Black and Isort..."
	$(ACTIVATE) && $(BLACK) --workers 4 . || (echo "Black formatting failed" && exit 1)
	$(ACTIVATE) && $(ISORT) . || (echo "Isort formatting failed" && exit 1)

# Run tests
test: check-env install
	@echo "Running tests with pytest..."
	$(ACTIVATE) && $(PYTEST) --max-workers=4 tests --disable-warnings --verbose || (echo "Tests failed" && exit 1)

# Generate tests using Pynguin
generate-tests: check-env install
	@echo "Generating unit tests with Pynguin..."
	$(ACTIVATE) && $(PYNGUIN) --project-path ./src --output-path $(TEST_OUTPUT_DIR) || (echo "Pynguin failed" && exit 1)

# Generate coverage report
coverage: check-env install test
	@echo "Generating test coverage report..."
	$(ACTIVATE) && $(PYTEST) --cov=src --cov-report=term-missing --cov-report=html --cov-report=html:$(COVERAGE_DIR) || (echo "Coverage generation failed" && exit 1)

# Generate documentation using Doxygen
docs:
	@echo "Generating documentation with Doxygen..."
	@if [ ! -f "$(DOXYGEN_CONFIG)" ]; then \
		echo "Doxygen configuration file ($(DOXYGEN_CONFIG)) not found. Please create it."; \
		exit 1; \
	else \
		doxygen $(DOXYGEN_CONFIG) || (echo "Doxygen failed" && exit 1); \
	fi

# Clean temporary files
clean:
	@echo "Cleaning up temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf $(COVERAGE_DIR)
	rm -rf .coverage
	rm -rf $(TEST_OUTPUT_DIR)
	killall -9 python || true

# Clean virtual environment
clean-venv:
	@echo "Removing the virtual environment..."
	rm -rf $(VENV)

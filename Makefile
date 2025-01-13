# Variables
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
	@echo "Available targets:"
	@awk '/^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, substr($$0, index($$0, "## ") + 3)}' $(MAKEFILE_LIST)
	@echo "  venv                Create the virtual environment"
	@echo "  install             Install project dependencies"
	@echo "  check-env           Ensure virtual environment exists"
	@echo "  run-app             Run the Flask application"
	@echo "  run-node            Run the Quantum Node"
	@echo "  lint                Lint the codebase using flake8"
	@echo "  format              Format code with Black and Isort"
	@echo "  test                Run tests with pytest"
	@echo "  generate-tests      Generate unit tests using Pynguin"
	@echo "  coverage            Generate test coverage report"
	@echo "  docs                Generate documentation using Doxygen"
	@echo "  clean               Remove temporary files and directories"
	@echo "  clean-venv          Remove the virtual environment"
	@echo "  clean-docs          Remove generated documentation"

# Virtual environment
venv:  ## Create the virtual environment
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV) || (echo "Error creating virtual environment" && exit 1)

check-env:  ## Ensure virtual environment exists
	@if [ ! -d "$(VENV)" ]; then \
		echo "Virtual environment not found. Run 'make venv' first."; \
		exit 1; \
	fi

# Install dependencies
install: venv check-env  ## Install project dependencies
	@echo "Installing dependencies..."
	$(ACTIVATE) && pip install --upgrade pip setuptools wheel && pip install -r $(REQUIREMENTS) || (echo "Error installing dependencies" && exit 1)

install-formatters: check-env  ## Install Black and Isort for formatting
	@echo "Installing formatters (Black and Isort)..."
	$(ACTIVATE) && pip install $(BLACK) $(ISORT) || (echo "Error installing formatters" && exit 1)

# Run Flask application
run-app: check-env install  ## Run the Flask application
	@echo "Starting the Flask application..."
	$(ACTIVATE) && python src/app.py

# Run Quantum Node
run-node: check-env install  ## Run the Quantum Node
	@echo "Starting the Quantum Node..."
	$(ACTIVATE) && python src/quantum_node.py

# Code linting
lint: check-env install  ## Lint the codebase using flake8
	@echo "Linting the codebase with flake8..."
	$(ACTIVATE) && $(FLAKE8) . --max-line-length=88 --statistics --verbose || (echo "Linting failed" && exit 1)

# Code formatting
format: check-env install-formatters  ## Format code with Black and Isort
	@echo "Formatting code with Black and Isort..."
	$(ACTIVATE) && $(BLACK) . && $(ISORT) . || (echo "Formatting failed" && exit 1)

# Run tests
test: check-env install  ## Run tests with pytest
	@echo "Running tests with pytest..."
	$(ACTIVATE) && $(PYTEST) tests --disable-warnings --verbose || (echo "Tests failed" && exit 1)

# Generate tests using Pynguin
generate-tests: check-env install  ## Generate unit tests using Pynguin
	@echo "Generating unit tests with Pynguin..."
	$(ACTIVATE) && $(PYNGUIN) --project-path ./src --output-path $(TEST_OUTPUT_DIR) || (echo "Test generation failed" && exit 1)

# Test coverage
coverage: check-env install test  ## Generate test coverage report
	@echo "Generating test coverage report..."
	$(ACTIVATE) && $(PYTEST) tests --cov=src --cov-report=term-missing --cov-report=html:$(COVERAGE_DIR) || (echo "Coverage generation failed" && exit 1)

# Documentation generation
docs:  ## Generate documentation using Doxygen
	@echo "Generating documentation with Doxygen..."
	@if [ ! -f "$(DOXYGEN_CONFIG)" ]; then \
		echo "Doxygen configuration file ($(DOXYGEN_CONFIG)) not found. Please create it."; \
		exit 1; \
	else \
		doxygen $(DOXYGEN_CONFIG) || (echo "Documentation generation failed" && exit 1); \
		echo "Documentation generated in the 'docs' directory."; \
	fi

# Clean up
clean:  ## Remove temporary files and directories
	@echo "Cleaning up temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf $(COVERAGE_DIR)
	rm -rf .coverage
	rm -rf $(TEST_OUTPUT_DIR)

clean-venv:  ## Remove the virtual environment
	@echo "Removing the virtual environment..."
	rm -rf $(VENV)

clean-docs:  ## Remove generated documentation
	@echo "Cleaning up generated documentation..."
	rm -rf docs

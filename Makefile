# Define variables
PYTHON := python3
VENV := .venv  # Updated to a common virtual environment folder
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

# Create virtual environment
venv: ## Create the virtual environment
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV) || (echo "Error creating virtual environment" && exit 1)

# Ensure virtual environment exists
check-env: ## Check if virtual environment exists
	@if [ ! -d "$(VENV)" ]; then \
		echo "Virtual environment not found. Run 'make venv' first."; \
		exit 1; \
	fi

# Install dependencies
install: venv check-env ## Install project dependencies
	@echo "Installing dependencies..."
	$(ACTIVATE) && pip install -r $(REQUIREMENTS) || (echo "Error installing dependencies" && exit 1)

# Install formatting tools
install-formatters: check-env ## Install formatting tools
	@echo "Installing Black and Isort..."
	$(ACTIVATE) && pip install $(BLACK) $(ISORT) || (echo "Error installing formatters" && exit 1)

# Run Flask application
run-app: check-env install ## Run the Flask application
	@echo "Starting the Flask application..."
	$(ACTIVATE) && python src/app.py

# Run Quantum Node
run-node: check-env install ## Run the Quantum Node
	@echo "Starting the Quantum Node..."
	$(ACTIVATE) && python src/quantum_node.py

# Lint the codebase
lint: check-env install ## Lint the codebase using flake8
	@echo "Linting the codebase with flake8..."
	$(ACTIVATE) && $(FLAKE8) . --max-line-length=88 --statistics --verbose || (echo "Linting failed" && exit 1)

# Format Code
format: check-env install-formatters ## Format code with Black and Isort
	@echo "Formatting code with Black and Isort..."
	$(ACTIVATE) && $(BLACK) . --workers=1 || (echo "Black formatting failed" && exit 1)
	$(ACTIVATE) && $(ISORT) . || (echo "Isort formatting failed" && exit 1)

# Run tests
test: check-env install ## Run tests with pytest
	@echo "Running tests with pytest..."
	$(ACTIVATE) && $(PYTEST) tests --disable-warnings || (echo "Tests failed" && exit 1)

# Generate tests using Pynguin
generate-tests: check-env install ## Generate unit tests using Pynguin
	@echo "Generating unit tests with Pynguin..."
	$(ACTIVATE) && $(PYNGUIN) --project-path ./src --output-path $(TEST_OUTPUT_DIR) || (echo "Pynguin failed" && exit 1)

# Generate coverage report
coverage: check-env install test ## Generate test coverage report
	@echo "Generating test coverage report..."
	$(ACTIVATE) && $(PYTEST) tests --cov=src --cov-report=term-missing --cov-report=html --cov-report html:$(COVERAGE_DIR) || (echo "Coverage generation failed" && exit 1)

# Generate documentation using Doxygen
docs: ## Generate documentation using Doxygen
	@echo "Generating documentation with Doxygen..."
	@if [ ! -f "$(DOXYGEN_CONFIG)" ]; then \
		echo "Doxygen configuration file ($(DOXYGEN_CONFIG)) not found. Please create it."; \
		exit 1; \
	else \
		doxygen $(DOXYGEN_CONFIG) || (echo "Doxygen failed" && exit 1); \
		echo "Documentation generated in the 'docs' directory."; \
	fi

# Clean temporary files
clean: ## Remove temporary files and directories
	@echo "Cleaning up temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf $(COVERAGE_DIR)
	rm -rf .coverage
	rm -rf $(TEST_OUTPUT_DIR)

# Clean virtual environment
clean-venv: ## Remove the virtual environment
	@echo "Removing the virtual environment..."
	rm -rf $(VENV)

# Clean documentation
clean-docs: ## Remove generated documentation
	@echo "Cleaning up generated documentation..."
	rm -rf docs

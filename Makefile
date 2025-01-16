# Define variables
PYTHON := python3
VENV := qpow-venv
ACTIVATE := . $(VENV)/bin/activate
REQUIREMENTS := requirements.txt
FLAKE8 := flake8
BLACK := black
ISORT := isort
PYTEST := pytest
PYNGUIN := pynguin
DOXYGEN_CONFIG := Doxyfile
COVERAGE_DIR := coverage_html
TEST_OUTPUT_DIR := tests/generated

# Default target
.DEFAULT_GOAL := help

# Help
help:  ## Show available Makefile targets
	@echo "Usage: make <target>"
	@echo ""
	@echo "Available targets:"
	@awk '/^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, substr($$0, index($$0, "## ") + 3)}' $(MAKEFILE_LIST)

# Create virtual environment
venv:  ## Create the virtual environment
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV)

# Ensure virtual environment exists
check-env:  ## Ensure virtual environment exists
	@if [ ! -d "$(VENV)" ]; then \
		echo "Virtual environment not found. Run 'make venv' first."; \
		exit 1; \
	fi

# Upgrade pip
upgrade-pip: check-env  ## Upgrade pip in the virtual environment
	@echo "Upgrading pip..."
	$(ACTIVATE) && pip install --upgrade pip

# Install dependencies
install: upgrade-pip  ## Install project dependencies
	@echo "Installing dependencies..."
	$(ACTIVATE) && pip install -r $(REQUIREMENTS)

# Install formatting tools
install-formatters: upgrade-pip  ## Install Black and Isort
	@echo "Installing Black and Isort..."
	$(ACTIVATE) && pip install $(BLACK) $(ISORT)

# Run Flask application
run-app: check-env install  ## Run the Flask application
	@echo "Starting the Flask application..."
	$(ACTIVATE) && python src/app.py

# Run Quantum Node
run-node: check-env install  ## Run the Quantum Node
	@echo "Starting the Quantum Node..."
	$(ACTIVATE) && python src/quantum_node.py

# Lint the codebase
lint: check-env install  ## Lint the codebase using flake8
	@echo "Linting the codebase with flake8..."
	$(ACTIVATE) && $(FLAKE8) src tests --max-line-length=88 --statistics --verbose

# Format code
format: check-env install-formatters  ## Format code with Black and Isort
	@echo "Formatting code with Black and Isort..."
	$(ACTIVATE) && $(BLACK) src tests
	$(ACTIVATE) && $(ISORT) src tests

# Run tests
test: check-env install  ## Run tests with pytest
	@echo "Running tests with pytest..."
	$(ACTIVATE) && $(PYTEST) tests --disable-warnings

# Generate tests using Pynguin
generate-tests: check-env install  ## Generate unit tests using Pynguin
	@echo "Generating unit tests with Pynguin..."
	$(ACTIVATE) && PYTHONPATH=./src PYNGUIN_DANGER_AWARE=1 $(PYNGUIN) \
		--project-path ./src \
		--output-path $(TEST_OUTPUT_DIR)

# Generate coverage report
coverage: check-env install test  ## Generate test coverage report
	@echo "Generating test coverage report..."
	$(ACTIVATE) && $(PYTEST) tests --cov=src --cov-report=term-missing --cov-report=html --cov-report html:$(COVERAGE_DIR)

# Generate documentation using Doxygen
docs:  ## Generate documentation using Doxygen
	@echo "Generating documentation with Doxygen..."
	@if [ ! -f "$(DOXYGEN_CONFIG)" ]; then \
		echo "Doxygen configuration file ($(DOXYGEN_CONFIG)) not found. Please create it."; \
		exit 1; \
	else \
		doxygen $(DOXYGEN_CONFIG); \
	fi

# Clean temporary files
clean:  ## Remove temporary files and directories
	@echo "Cleaning up temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf $(COVERAGE_DIR)
	rm -rf .coverage
	rm -rf $(TEST_OUTPUT_DIR)

# Clean virtual environment
clean-venv:  ## Remove the virtual environment
	@echo "Removing the virtual environment..."
	rm -rf $(VENV)

# Clean documentation
clean-docs:  ## Remove generated documentation
	@echo "Cleaning up generated documentation..."
	rm -rf docs

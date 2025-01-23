# Define variables
PYTHON := python3
VENV := qpow-venv
ACTIVATE := . $(VENV)/bin/activate
REQUIREMENTS := requirements.txt
FLAKE8 := flake8
BLACK := black
ISORT := isort
PYTEST := pytest
DOXYGEN := doxygen
DOXYGEN_CONFIG := Doxyfile
COVERAGE_DIR := coverage_html

# Default target
.DEFAULT_GOAL := help

# Help
help: ## Show available Makefile targets
	@echo "Usage: make <target>"
	@echo ""
	@echo "Available targets:"
	@awk '/^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, substr($$0, index($$0, "## ") + 3)}' $(MAKEFILE_LIST)

# Create virtual environment
venv: ## Create the virtual environment
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV)

# Ensure virtual environment exists
check-env: ## Ensure virtual environment exists
	@if [ ! -d "$(VENV)" ]; then \
		echo "Virtual environment not found. Run 'make venv' first."; \
		exit 1; \
	fi

# Upgrade pip
upgrade-pip: check-env ## Upgrade pip in the virtual environment
	$(ACTIVATE) && pip install --upgrade pip

# Install dependencies
install: upgrade-pip ## Install project dependencies
	$(ACTIVATE) && pip install -r $(REQUIREMENTS)

# Install formatting tools
install-formatters: upgrade-pip ## Install Black and Isort
	$(ACTIVATE) && pip install $(BLACK) $(ISORT)

# Install quantcrypt
install-quantcrypt: check-env ## Install the quantcrypt library
	$(ACTIVATE) && pip install quantcrypt

# Clear pip cache
clear-cache: check-env ## Clear pip cache
	@echo "Clearing pip cache..."
	$(ACTIVATE) && pip cache purge || pip cache clear

# Run Flask application
run-app: check-env install ## Run the Flask application
	$(ACTIVATE) && FLASK_APP=src/app.py flask run

# Lint the codebase
lint: check-env install ## Lint the codebase using flake8
	$(ACTIVATE) && $(FLAKE8) src tests --max-line-length=88 --statistics --verbose

# Format code
format: check-env install-formatters ## Format code with Black and Isort
	$(ACTIVATE) && $(BLACK) src tests
	$(ACTIVATE) && $(ISORT) src tests

# Run tests with pytest
test: check-env install ## Run tests using pytest
	$(ACTIVATE) && $(PYTEST) tests --verbose

# Generate coverage report
coverage: check-env install ## Generate test coverage report
	$(ACTIVATE) && $(PYTEST) tests --cov=src --cov-report=term-missing --cov-report=html:$(COVERAGE_DIR)

# Generate documentation using Doxygen
docs: ## Generate documentation using Doxygen
	@if [ ! -f "$(DOXYGEN_CONFIG)" ]; then \
		echo "Doxygen configuration file ($(DOXYGEN_CONFIG)) not found. Skipping documentation generation."; \
	else \
		$(DOXYGEN) $(DOXYGEN_CONFIG); \
	fi

# Clean temporary files
clean: ## Remove temporary files and directories
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf $(COVERAGE_DIR)
	rm -rf .coverage
	rm -rf htmlcov

# Clean virtual environment
clean-venv: ## Remove the virtual environment
	rm -rf $(VENV)

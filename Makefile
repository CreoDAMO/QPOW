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

venv: ## Create the virtual environment
        $(PYTHON) -m venv $(VENV)

check-env: ## Ensure virtual environment exists
        @if [ ! -d "$(VENV)" ]; then \
                echo "Virtual environment not found. Run 'make venv' first."; \
                exit 1; \
        fi

upgrade-pip: check-env ## Upgrade pip in the virtual environment
        $(ACTIVATE) && pip install --upgrade pip

clear-cache: check-env ## Clear pip cache
        @echo "Clearing pip cache..."
        $(ACTIVATE) && pip cache purge || pip cache clear

install: clear-cache upgrade-pip ## Install project dependencies
        $(ACTIVATE) && pip install -r $(REQUIREMENTS) quantcrypt

install-formatters: upgrade-pip ## Install Black and Isort
        $(ACTIVATE) && pip install $(BLACK) $(ISORT)

run-app: check-env install ## Run the Flask application
        $(ACTIVATE) && FLASK_APP=src/app.py flask run

lint: check-env install ## Lint the codebase using flake8
        $(ACTIVATE) && $(FLAKE8) src tests --max-line-length=88 --statistics --verbose

format: check-env install-formatters ## Format code with Black and Isort
        $(ACTIVATE) && $(BLACK) src tests
        $(ACTIVATE) && $(ISORT) src tests

test: check-env install ## Run tests using pytest
        $(ACTIVATE) && $(PYTEST) tests --verbose

coverage: check-env install ## Generate test coverage report
        $(ACTIVATE) && $(PYTEST) tests --cov=src --cov-report=term-missing --cov-report=html:$(COVERAGE_DIR)

docs: ## Generate documentation using Doxygen
        @if [ ! -f "$(DOXYGEN_CONFIG)" ]; then \
                echo "Doxygen configuration file ($(DOXYGEN_CONFIG)) not found. Skipping documentation generation."; \
        else \
                $(DOXYGEN) $(DOXYGEN_CONFIG); \
        fi

clean: ## Remove temporary files and directories
        find . -type d -name "__pycache__" -exec rm -rf {} +
        find . -type f -name "*.pyc" -delete
        rm -rf .pytest_cache
        rm -rf $(COVERAGE_DIR)
        rm -rf .coverage
        rm -rf htmlcov

clean-venv: ## Remove the virtual environment
        rm -rf $(VENV)
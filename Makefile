# Define variables
PYTHON := python3
VENV := qpow-venv
ACTIVATE := source $(VENV)/bin/activate
REQUIREMENTS := requirements.txt

# Default target
.DEFAULT_GOAL := help

# Help
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Available targets:"
	@echo "  venv                Create the virtual environment"
	@echo "  install             Install project dependencies"
	@echo "  run-app             Run the Flask application"
	@echo "  run-node            Run the Quantum Node"
	@echo "  lint                Lint the codebase using flake8"
	@echo "  test                Run tests with pytest"
	@echo "  generate-tests      Generate unit tests using Pynguin"
	@echo "  coverage            Generate test coverage report"
	@echo "  clean               Remove temporary files and directories"
	@echo "  clean-venv          Remove the virtual environment"
	@echo "  docs                Generate documentation using Doxygen"
	@echo "  clean-docs          Remove generated documentation"

# Create virtual environment
venv:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV)

# Install dependencies
install: venv
	@echo "Installing dependencies..."
	$(ACTIVATE) && pip install --upgrade pip setuptools wheel && pip install -r $(REQUIREMENTS)

# Run Flask application
run-app: install
	@echo "Starting the Flask application..."
	$(ACTIVATE) && python src/app.py

# Run Quantum Node
run-node: install
	@echo "Starting the Quantum Node..."
	$(ACTIVATE) && python src/quantum_node.py

# Lint the codebase
lint:
	@echo "Linting the codebase with flake8..."
	$(ACTIVATE) && flake8 . --max-line-length=88 --statistics

# Run tests
test:
	@echo "Running tests with pytest..."
	$(ACTIVATE) && pytest tests --disable-warnings

# Generate tests using Pynguin
generate-tests: install
	@echo "Generating unit tests with Pynguin..."
	$(ACTIVATE) && pynguin \
		--project-path ./src \
		--output-path ./tests/generated \
		--module-name your.module.name
	@echo "Generated tests are saved in ./tests/generated."

# Generate coverage report
coverage:
	@echo "Generating test coverage report..."
	$(ACTIVATE) && pytest tests --cov=src --cov-report=term-missing --cov-report=html

# Generate documentation using Doxygen
docs:
	@echo "Generating documentation with Doxygen..."
ifndef DOXYGEN_CONFIG
	@echo "Doxygen configuration file not found. Please create a 'Doxyfile'."
else
	doxygen $(DOXYGEN_CONFIG)
	@echo "Documentation generated in the 'docs' directory."
endif

# Clean temporary files
clean:
	@echo "Cleaning up temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf coverage_html
	rm -rf .coverage
	rm -rf tests/generated

# Clean virtual environment
clean-venv:
	@echo "Removing the virtual environment..."
	rm -rf $(VENV)

# Clean documentation
clean-docs:
	@echo "Cleaning up generated documentation..."
	rm -rf docs

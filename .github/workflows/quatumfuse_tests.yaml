# QuantumFuse Blockchain Tests Workflow
# This workflow runs tests with pytest

name: QuantumFuse Tests

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python 3.10
      uses: actions/setup-python@v3
      with:
        python-version: "3.10"

    - name: Create Virtual Environment
      run: |
        python -m venv venv
        . venv/bin/activate

    - name: Install dependencies
      run: |
        pip install --upgrade pip
        pip install pytest
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

    - name: Set PYTHONPATH
      run: echo "PYTHONPATH=$(pwd)" >> $GITHUB_ENV

    - name: Test with pytest
      env:
        IPFS_PATH: "/tmp/ipfs"
      run: pytest --maxfail=5 --disable-warnings --junitxml=results.xml

#!/bin/bash
# Script to set up the QuantumFuse Blockchain environment locally

# Update and install Python dependencies
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv libssl-dev

# Set up a virtual environment
echo "Creating a Python virtual environment..."
python3 -m venv qfuse_env
source qfuse_env/bin/activate

# Install required Python packages
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations (if applicable)
# echo "Running database setup..."
# python manage.py migrate  # Uncomment if using Django or Flask with migrations

# Initialize blockchain state if needed
echo "Initializing blockchain state..."
python src/blockchain/blockchain.py --init

echo "Local setup complete. Activate the environment with 'source qfuse_env/bin/activate'."

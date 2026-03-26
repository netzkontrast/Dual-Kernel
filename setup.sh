#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting setup process..."

# Create necessary directories
echo "Creating required directories..."
mkdir -p tools/output/diffs
mkdir -p tools/fixtures
echo "Directories created."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.10 or higher."
    return 1 2>/dev/null || true
fi

# Set up virtual environment
echo "Setting up Python virtual environment in .venv..."
python3 -m venv .venv

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Download spaCy model
echo "Downloading spaCy model (de_core_news_lg)..."
python -m spacy download de_core_news_lg

echo ""
echo "Setup complete!"
echo "To activate the virtual environment, run: source .venv/bin/activate"

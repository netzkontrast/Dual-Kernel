#!/bin/bash
set -e

echo "Checking Python version..."
python3 -c "import sys; assert sys.version_info >= (3, 10), 'Python 3.10+ required'"

echo "Updating pip..."
python3 -m pip install --upgrade pip

echo "Installing requirements globally..."
python3 -m pip install -r tools/requirements.txt

echo "Downloading SpaCy model..."
python3 -m spacy download de_core_news_lg

echo "Setup complete!"

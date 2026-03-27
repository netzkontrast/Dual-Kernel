#!/bin/bash
set -euo pipefail

# SessionStart hook for Kohärenz Protokoll (Dual-Kernel)
# Installs Python dependencies and downloads NLP model for remote sessions

# Only run in Claude Code on the web
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

echo "🚀 Setting up Kohärenz Protokoll environment..."

# Create necessary directories if they don't exist
mkdir -p tools/output/diffs tools/fixtures

# Check Python 3 is available
if ! command -v python3 &>/dev/null; then
  echo "❌ Python 3 is required but not installed"
  exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
  echo "📦 Creating Python virtual environment..."
  python3 -m venv .venv
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "📌 Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies from requirements.txt
echo "📚 Installing dependencies (spacy, PyYAML, rich, click)..."
pip install -r requirements.txt --quiet

# Download German language model for spaCy (required for ETL pipeline)
echo "🔤 Downloading German language model (de_core_news_lg)..."
python -m spacy download de_core_news_lg --quiet

# Export environment variables for the session (idempotent)
echo "🔧 Setting up environment variables..."
if ! grep -q "PYTHONPATH" "${CLAUDE_ENV_FILE}" 2>/dev/null; then
  echo "export PYTHONPATH=\".:\$PYTHONPATH\"" >> "${CLAUDE_ENV_FILE}"
fi
if ! grep -q "VIRTUAL_ENV" "${CLAUDE_ENV_FILE}" 2>/dev/null; then
  echo "export VIRTUAL_ENV=\"${VIRTUAL_ENV}\"" >> "${CLAUDE_ENV_FILE}"
fi

echo "✅ Setup complete! Virtual environment ready."
echo "   Run: source .venv/bin/activate"
echo "   Then: python tools/source_scanner.py Markdown-docs/"

#!/bin/bash
# Setup script for BleedRate development environment

set -e

echo "🚀 BleedRate Development Setup"
echo "================================"
echo ""

# Check Python version
echo "📋 Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

echo "Found Python $PYTHON_VERSION"

if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 11 ]); then
    echo ""
    echo "❌ ERROR: Python 3.11 or higher is required"
    echo "   Current version: $PYTHON_VERSION"
    echo ""
    echo "To install Python 3.11:"
    echo "   brew install python@3.11"
    echo ""
    echo "Then create a virtual environment:"
    echo "   python3.11 -m venv .venv"
    echo "   source .venv/bin/activate"
    echo "   ./setup.sh"
    exit 1
fi

echo "✅ Python version is compatible"
echo ""

# Check if in virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  WARNING: Not in a virtual environment"
    echo ""
    echo "It's recommended to use a virtual environment:"
    echo "   python3.11 -m venv .venv"
    echo "   source .venv/bin/activate"
    echo "   ./setup.sh"
    echo ""
    read -p "Continue without virtual environment? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ Virtual environment detected: $VIRTUAL_ENV"
fi

echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "🧪 Running tests..."
pytest tests/ -v

echo ""
echo "✅ Setup complete!"
echo ""
echo "Available commands:"
echo "  make dev           - Run development server"
echo "  make test          - Run tests"
echo "  make test-coverage - Run tests with coverage report"
echo "  make lint          - Check code quality"
echo "  make format        - Format code"
echo ""
echo "Happy coding! 🎉"

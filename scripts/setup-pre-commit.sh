#!/bin/bash
set -euo pipefail

# Setup script for pre-commit hooks
# This script installs and configures pre-commit hooks for the project

echo "🔧 Setting up pre-commit hooks..."

# Check if pre-commit is installed
if ! command -v pre-commit &> /dev/null; then
    echo "❌ pre-commit is not installed. Installing..."
    python3 -m pip install pre-commit --break-system-packages
else
    echo "✅ pre-commit is already installed"
fi

# Install pre-commit hooks
echo "📦 Installing pre-commit hooks..."
pre-commit install

# Update hooks to latest versions
echo "🔄 Updating hooks to latest versions..."
pre-commit autoupdate

# Run hooks on all files to test
echo "🧪 Testing pre-commit hooks..."
pre-commit run --all-files || echo "⚠️  Some hooks failed - this is normal for the first run"

echo "✅ Pre-commit hooks setup complete!"
echo ""
echo "📋 Available commands:"
echo "  make pre-commit-run    - Run hooks on all files"
echo "  make pre-commit-update - Update hooks to latest versions"
echo "  git commit            - Hooks will run automatically on commit"
echo ""
echo "💡 Tips:"
echo "  - Hooks run automatically on every commit"
echo "  - Black and isort will auto-fix formatting issues"
echo "  - flake8 will check for linting issues (manual fixes required)"
echo "  - Run 'make pre-commit-run' to test all files before committing"

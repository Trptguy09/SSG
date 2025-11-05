#!/bin/bash
set -e

# Ensure clean build
rm -rf docs
mkdir docs

# Run Python builder
python3 src/main.py

# Add .nojekyll to bypass Jekyll processing
touch docs/.nojekyll

echo "✅ Site built successfully into docs/"

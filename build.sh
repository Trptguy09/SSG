#!/bin/bash
# Clean previous build
rm -rf docs

# Recreate docs folder
mkdir -p docs

# Copy static assets
cp -r static docs/static

# Generate HTML pages
python3 src/main.py

# Prevent GitHub Pages from ignoring files starting with _
touch docs/.nojekyll

echo "Build complete. Open docs/index.html to preview locally."

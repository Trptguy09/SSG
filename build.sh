#!/bin/bash
# Build production site for GitHub Pages

REPO_NAME="SSG"  # Replace with your GitHub repo name
rm -rf docs
mkdir -p docs

# Copy static assets
cp -r static docs/static

# Generate pages with GitHub Pages basepath
python3 src/main.py "/$REPO_NAME/"

# Prevent Jekyll from ignoring files
touch docs/.nojekyll

echo "Production build complete in docs/ directory."

#!/bin/bash
# Build the site for GitHub Pages

REPO_NAME="SSG"  # replace with your repo name
rm -rf docs
mkdir -p docs
cp -r static docs/static

# Run the generator with basepath pointing to GitHub Pages project site
python3 src/main.py "/$REPO_NAME/"

# Prevent Jekyll from ignoring files
touch docs/.nojekyll

echo "Production build complete in docs/ directory."

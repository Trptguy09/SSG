#!/bin/bash
set -e

# Remove old docs directory
rm -rf docs
mkdir docs

# Build site for GitHub Pages (replace REPO_NAME with your repo name)
python3 src/main.py "/SSG/"

# Add .nojekyll to avoid Jekyll processing
touch docs/.nojekyll

echo "✅ Site built successfully into docs/"

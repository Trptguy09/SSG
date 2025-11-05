#!/usr/bin/env bash
# Exit immediately if a command fails
set -e

# --- CONFIGURATION ---
CONTENT_DIR="content"
OUTPUT_DIR="docs"
STATIC_DIR="static"
BASE_PATH="/SSG"   # <-- Change if your repo name changes

# --- CLEAN OLD BUILD ---
echo "🧹 Cleaning old build..."
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# --- COPY STATIC FILES ---
if [ -d "$STATIC_DIR" ]; then
  echo "📂 Copying static files..."
  cp -r "$STATIC_DIR"/* "$OUTPUT_DIR"/
else
  echo "⚠️  No static directory found. Skipping."
fi

# --- GENERATE SITE ---
echo "⚙️  Generating site..."
python3 src/main.py "$BASE_PATH"

# --- OPTIONAL: CREATE .nojekyll (for GitHub Pages) ---
# Prevent GitHub Pages from ignoring files that start with underscores
echo "🧩 Creating .nojekyll..."
touch "$OUTPUT_DIR/.nojekyll"

# --- OPTIONAL: ADD AND COMMIT CHANGES ---
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "📤 Committing updated site to Git..."
  git add "$OUTPUT_DIR"
  git commit -m "Build site"
  # Uncomment this line if you want to push automatically
  # git push
else
  echo "⚠️  Not inside a Git repository. Skipping commit."
fi

echo "✅ Build complete! Site ready in '$OUTPUT_DIR/'."
echo "🌐 When pushed, it will be live at: https://trptguy09.github.io$BASE_PATH/"

import os
import shutil

from converter import markdown_to_html_node

CONTENT_DIR = "content"
OUTPUT_DIR = "docs"
STATIC_DIR = "static"
TEMPLATE_FILE = "template.html"


def copy_static():
    """Copy static assets to the docs directory."""
    static_dest = os.path.join(OUTPUT_DIR)
    if os.path.exists(STATIC_DIR):
        shutil.copytree(STATIC_DIR, os.path.join(static_dest, ""), dirs_exist_ok=True)
        print("Copied static files to docs")
    else:
        print("No static directory found; skipping static copy.")


def generate_html_from_md(md_path, html_path):
    """Convert a Markdown file to an HTML page using the template."""
    with open(md_path, "r", encoding="utf-8") as f:
        markdown_text = f.read()

    html_node = markdown_to_html_node(markdown_text)
    html_body = html_node.to_html()

    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template = f.read()

    full_html = template.replace("{{ Content }}", html_body)

    os.makedirs(os.path.dirname(html_path), exist_ok=True)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"Generated {html_path} from {md_path}")


def generate_site():
    """Recursively build all Markdown files under CONTENT_DIR into OUTPUT_DIR."""
    copy_static()

    for root, _, files in os.walk(CONTENT_DIR):
        for filename in files:
            if not filename.endswith(".md"):
                continue

            md_path = os.path.join(root, filename)

            # Compute relative path inside content/
            rel_path = os.path.relpath(md_path, CONTENT_DIR)

            # Remove .md extension and make an index.html inside its folder
            rel_dir = os.path.splitext(rel_path)[0]
            output_dir = os.path.join(OUTPUT_DIR, rel_dir)
            html_path = os.path.join(output_dir, "index.html")

            generate_html_from_md(md_path, html_path)


if __name__ == "__main__":
    generate_site()

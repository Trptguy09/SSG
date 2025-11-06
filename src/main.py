import os
import shutil

from converter import markdown_to_html_node

CONTENT_DIR = "content"
OUTPUT_DIR = "docs"
STATIC_DIR = "static"
TEMPLATE_FILE = "template.html"


def copy_static():
    """Copy static assets to the docs directory."""
    if os.path.exists(STATIC_DIR):
        shutil.copytree(STATIC_DIR, OUTPUT_DIR, dirs_exist_ok=True)
        print("Copied static files to docs")
    else:
        print("No static directory found; skipping static copy.")


def generate_page(md_path, html_path, basepath="/"):
    """Generate a single HTML page from Markdown."""
    with open(md_path, "r", encoding="utf-8") as f:
        markdown_text = f.read()

    html_node = markdown_to_html_node(markdown_text)
    html_body = html_node.to_html()

    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template = f.read()

    # Replace placeholders
    title = os.path.splitext(os.path.basename(md_path))[0].title()
    full_html = template.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_body)

    os.makedirs(os.path.dirname(html_path), exist_ok=True)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Generated {html_path} from {md_path}")


def generate_site():
    copy_static()
    for root, dirs, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(".md"):
                md_path = os.path.join(root, file)
                rel_path = os.path.relpath(md_path, CONTENT_DIR)
                html_path = os.path.join(
                    OUTPUT_DIR, os.path.splitext(rel_path)[0], "index.html"
                )
                generate_page(md_path, html_path)


if __name__ == "__main__":
    generate_site()

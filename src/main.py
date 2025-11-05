import os
import sys

from converter import markdown_to_html_node  # your markdown parser

# Get basepath from CLI argument, default to ''
# For GitHub Pages project sites, use "/SSG"
basepath = sys.argv[1] if len(sys.argv) > 1 else ""

CONTENT_DIR = "content"
OUTPUT_DIR = "docs"


def write_html(path, html_content):
    """Write HTML content to a file, creating directories as needed."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html_content)


def generate_site():
    """Walk through content/, convert markdown to HTML, and write to docs/."""
    for root, _, files in os.walk(CONTENT_DIR):
        for file in files:
            if not file.endswith(".md"):
                continue

            # Markdown source path
            md_path = os.path.join(root, file)
            rel_path = os.path.relpath(md_path, CONTENT_DIR)
            name, _ = os.path.splitext(rel_path)

            # Determine output HTML path
            if name.lower() == "index":
                output_path = os.path.join(OUTPUT_DIR, "index.html")
            else:
                output_path = os.path.join(OUTPUT_DIR, name, "index.html")

            # Read Markdown content
            with open(md_path, "r", encoding="utf-8") as f:
                md_text = f.read()

            # Convert Markdown to an HTML node tree
            root_node = markdown_to_html_node(md_text)
            html_body = root_node.to_html()  # ✅ convert to HTML string

            # Load the template
            with open("template.html", "r", encoding="utf-8") as tf:
                template = tf.read()

            # Insert title and content
            title = os.path.basename(name).capitalize() or "Index"
            html_output = template.replace("{{ Title }}", title)
            html_output = html_output.replace("{{ Content }}", html_body)

            # Fix asset paths to respect basepath (important for GitHub Pages)
            html_output = html_output.replace('href="/', f'href="{basepath}/')
            html_output = html_output.replace('src="/', f'src="{basepath}/')

            # Write output file
            write_html(output_path, html_output)
            print(f"✅ Generated {output_path}")


if __name__ == "__main__":
    generate_site()

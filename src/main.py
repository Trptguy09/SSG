import os
import sys

from converter import markdown_to_html_node  # your parser

# Get basepath from CLI argument, default to '/'
basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

CONTENT_DIR = "content"
OUTPUT_DIR = "docs"


def write_html(path, html_content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(html_content)


def nodes_to_html(nodes):
    """
    Convert a list of nodes returned by markdown_to_html_node to a single HTML string.
    Assumes each node has a __str__ method that outputs HTML.
    """
    return "".join(str(node) for node in nodes)


def generate_site():
    for root, _, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(".md"):
                md_path = os.path.join(root, file)
                rel_path = os.path.relpath(md_path, CONTENT_DIR)
                output_path = os.path.join(
                    OUTPUT_DIR, os.path.splitext(rel_path)[0], "index.html"
                )

                # Read Markdown
                with open(md_path) as f:
                    md_text = f.read()

                # Convert Markdown to HTML nodes
                nodes = markdown_to_html_node(md_text)
                html_body = nodes_to_html(nodes)

                # Load template
                with open("template.html") as tf:
                    template = tf.read()

                # Replace placeholders
                html_output = template.replace("{{ Title }}", os.path.splitext(file)[0])
                html_output = html_output.replace("{{ Content }}", html_body)

                # Fix absolute asset paths to respect basepath
                html_output = html_output.replace('href="/', f'href="{basepath}')
                html_output = html_output.replace('src="/', f'src="{basepath}')

                # Write HTML
                write_html(output_path, html_output)
                print(f"Generated {output_path}")


if __name__ == "__main__":
    generate_site()

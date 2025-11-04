import os

from converter import markdown_to_html_node

# Base folder for GitHub Pages project site
BASE = "/SSG/"  # <-- important for links if served at github.io/SSG/

CONTENT_DIR = "content"
OUTPUT_DIR = "docs"


def write_html(path, html_content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(html_content)


def relative_path(asset_path, page_path):
    """
    Returns the relative path from page_path to asset_path
    """
    return os.path.relpath(asset_path, os.path.dirname(page_path))


def generate_site():
    for root, _, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(".md"):
                md_path = os.path.join(root, file)
                # compute output path
                rel_path = os.path.relpath(md_path, CONTENT_DIR)
                output_path = os.path.join(
                    OUTPUT_DIR, os.path.splitext(rel_path)[0], "index.html"
                )

                # read markdown and generate HTML
                with open(md_path, "r") as f:
                    md_text = f.read()

                html_body = markdown_to_html_node(md_text)  # returns full HTML string

                # adjust asset paths for relative linking
                html_body = html_body.replace(
                    "/static/", relative_path("docs/static/", output_path) + "/"
                )

                # write to output folder
                write_html(output_path, html_body)
                print(f"Generated {output_path}")


if __name__ == "__main__":
    generate_site()

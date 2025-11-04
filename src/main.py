import os
import shutil

from converter import markdown_to_html_node
from markdown_utils import generate_page

# Clean public
public_dir = "public"
if os.path.exists(public_dir):
    shutil.rmtree(public_dir)
os.makedirs(public_dir, exist_ok=True)

# Copy static
if os.path.exists("static"):
    shutil.copytree("static", "public", dirs_exist_ok=True)

# Generate index.html
generate_page(
    from_path="content/index.md",
    template_path="template.html",
    dest_path="public/index.html",
    markdown_to_html_node=markdown_to_html_node,
)

import os
import shutil

from .converter import markdown_to_html_node
from .markdown_utils import generate_page
from .parser import code_block_node, text_to_children


def block_to_html_node(block, block_type):
    if block_type == "code":
        return code_block_node(block)
    elif block_type == "paragraph":
        return ParentNode("div", text_to_children(block))  # Or wrap <p> individually
    # handle headings, lists, etc. as before


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

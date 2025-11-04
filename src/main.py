import os
import shutil

from converter import markdown_to_html_node
from markdown_utils import generate_page
from nodes import ParentNode
from parser import code_block_node, text_to_children


def block_to_html_node(block, block_type):
    if block_type == "code":
        return code_block_node(block)
    elif block_type == "paragraph":
        return ParentNode("div", text_to_children(block))
    # You can extend this to handle headings, lists, etc.


def generate_pages_recursive(content_dir, template_path, dest_dir):
    """
    Recursively generate HTML pages from Markdown files in content_dir.
    """
    for root, dirs, files in os.walk(content_dir):
        # Compute relative path to maintain structure
        rel_path = os.path.relpath(root, content_dir)
        current_dest_dir = os.path.join(dest_dir, rel_path)
        os.makedirs(current_dest_dir, exist_ok=True)

        for file in files:
            src_file_path = os.path.join(root, file)
            if file.endswith(".md"):
                html_file_name = file[:-3] + ".html"
                dest_file_path = os.path.join(current_dest_dir, html_file_name)
                print(f"Generating {dest_file_path} from {src_file_path}")
                generate_page(
                    from_path=src_file_path,
                    template_path=template_path,
                    dest_path=dest_file_path,
                    markdown_to_html_node=markdown_to_html_node,
                )
            else:
                # Copy other non-Markdown files
                dest_file_path = os.path.join(current_dest_dir, file)
                shutil.copy2(src_file_path, dest_file_path)
                print(f"Copied {src_file_path} to {dest_file_path}")


def main():
    public_dir = "public"
    content_dir = "content"
    template_file = "template.html"
    static_dir = "static"

    # Clean public folder
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    os.makedirs(public_dir, exist_ok=True)

    # Copy static assets
    if os.path.exists(static_dir):
        shutil.copytree(static_dir, public_dir, dirs_exist_ok=True)
        print(f"Copied static files to {public_dir}")

    # Generate all pages recursively
    generate_pages_recursive(content_dir, template_file, public_dir)


if __name__ == "__main__":
    main()

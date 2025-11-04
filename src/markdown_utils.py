import os

from nodes import ParentNode


def extract_title(markdown_content):
    """
    Extracts the first H1 (# ) title from the markdown content.
    Raises an exception if no H1 is found.
    """
    for line in markdown_content.splitlines():
        if line.strip().startswith("# "):
            return line.strip("# ").strip()
    raise ValueError("No H1 title found in markdown content.")


def render_node(node):
    """
    Recursively render a ParentNode or LeafNode (or list) to HTML string.
    """
    if isinstance(node, list):
        return "".join(render_node(child) for child in node)
    elif hasattr(node, "children"):  # ParentNode
        inner_html = "".join(render_node(child) for child in node.children)
        return f"<{node.tag}>{inner_html}</{node.tag}>"
    else:  # LeafNode
        # Try common attribute names for text content
        if hasattr(node, "text"):
            return str(node.text)
        elif hasattr(node, "content"):
            return str(node.content)
        elif hasattr(node, "value"):
            return str(node.value)
        else:
            return str(node)  # fallback to str(node)


def generate_page(
    from_path, template_path, dest_path, markdown_to_html_node, basepath="/"
):
    # Read markdown
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    # Convert markdown to HTML nodes and render
    nodes = markdown_to_html_node(markdown_content)
    html_from_markdown = render_node(ParentNode("div", nodes))

    # Read template
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    # Replace placeholders
    html_content = template_content
    html_content = html_content.replace("{{ Title }}", extract_title(markdown_content))
    html_content = html_content.replace("{{ Content }}", html_from_markdown)

    # Replace absolute paths with basepath
    html_content = html_content.replace('href="/', f'href="{basepath}')
    html_content = html_content.replace('src="/', f'src="{basepath}')

    # Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write final HTML
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(html_content)

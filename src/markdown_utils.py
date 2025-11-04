import os


def extract_title(markdown_text):
    """
    Extract H1 header from markdown.
    """
    for line in markdown_text.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No H1 header found")


def generate_page(from_path, template_path, dest_path, markdown_to_html_node):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        markdown_text = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    html_nodes = markdown_to_html_node(markdown_text)
    html_content = "".join(node.to_html() for node in html_nodes)

    title = extract_title(markdown_text)

    final_html = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_content
    )

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_html)

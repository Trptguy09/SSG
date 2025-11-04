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


def generate_page(
    from_path, template_path, dest_path, markdown_to_html_node, basepath="/"
):
    # Read markdown content
    with open(from_path, "r") as f:
        markdown_content = f.read()

    # Convert markdown to HTML
    html_content = markdown_to_html_node(markdown_content).render()

    # Read template
    with open(template_path, "r") as f:
        template_content = f.read()

    # Replace placeholders
    html_content = template_content.replace(
        "{{ Title }}", extract_title(markdown_content)
    )
    html_content = html_content.replace("{{ Content }}", html_content)

    # Replace absolute root paths with basepath
    html_content = html_content.replace('href="/', f'href="{basepath}')
    html_content = html_content.replace('src="/', f'src="{basepath}')

    # Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write final HTML
    with open(dest_path, "w") as f:
        f.write(html_content)

import os
import re


def extract_title(markdown_text):
    """
    Extracts the first H1 header (# Heading) from markdown_text.
    Returns a string like 'Heading Title' or 'Untitled' if none found.
    """
    match = re.search(r"^# (.+)$", markdown_text, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "Untitled"


def generate_page(html_body, template_path, output_path, markdown_text=None):
    """
    Generates a full HTML page by inserting the HTML body into the template.
    If markdown_text is provided, the <title> tag will be replaced with the H1 title.
    """

    # Load template
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file not found: {template_path}")
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # Replace content placeholder
    html_output = template.replace("{{ Content }}", html_body)

    # Replace title placeholder (optional)
    if markdown_text and "{{ Title }}" in template:
        title = extract_title(markdown_text)
        html_output = html_output.replace("{{ Title }}", title)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Write final HTML
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_output)

    return output_path

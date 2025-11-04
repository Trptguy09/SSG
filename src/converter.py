import re

from nodes import LeafNode, ParentNode


def markdown_to_html_node(markdown_text):
    """
    Convert markdown to HTML nodes.
    Supports:
    - Paragraphs
    - Headings
    - Blockquotes
    - Lists (ordered/unordered)
    - Code blocks
    - Images
    """
    nodes = []
    lines = markdown_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        # Heading
        if line.startswith("#"):
            level = len(line.split(" ")[0])
            content = line[level + 1 :].strip() if len(line) > level else ""
            nodes.append(LeafNode(f"h{level}", value=content))
            i += 1
            continue

        # Blockquote
        if line.startswith(">"):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_lines.append(lines[i].strip()[1:].strip())
                i += 1
            nodes.append(LeafNode("blockquote", value="<br>".join(quote_lines)))
            continue

        # Unordered list
        if line.startswith("- "):
            items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(LeafNode("li", value=lines[i].strip()[2:]))
                i += 1
            nodes.append(ParentNode("ul", children=items))
            continue

        # Ordered list
        if re.match(r"^\d+\.", line):
            items = []
            while i < len(lines) and re.match(r"^\d+\.", lines[i].strip()):
                items.append(
                    LeafNode("li", value=re.sub(r"^\d+\.\s*", "", lines[i].strip()))
                )
                i += 1
            nodes.append(ParentNode("ol", children=items))
            continue

        # Code block
        if line.startswith("```"):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # Skip closing ```
            nodes.append(LeafNode("pre", value="\n".join(code_lines)))
            continue

        # Image inline ![alt](url)
        img_match = re.match(r"!\[(.*?)\]\((.*?)\)", line)
        if img_match:
            alt, src = img_match.groups()
            nodes.append(LeafNode("img", props={"src": src, "alt": alt}))
            i += 1
            continue

        # Paragraph
        nodes.append(LeafNode("p", value=line))
        i += 1

    return nodes

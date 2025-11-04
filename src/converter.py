import re

from nodes import ParentNode
from parser import (
    code_block_node,
    paragraphs_from_text,
    parse_inline,
    text_to_children,
)


def markdown_to_html_node(markdown_text):
    """
    Convert full markdown text into a list of HTML nodes.
    Handles:
      - Headings (# to ######)
      - Paragraphs
      - Code blocks (```...```)
      - Ordered and unordered lists
      - Blockquotes (>)
    """
    nodes = []
    blocks = markdown_text.split("\n\n")

    for block in blocks:
        block = block.rstrip()
        if not block:
            continue

        # Code block
        if block.startswith("```") and block.endswith("```"):
            code_text = "\n".join(block.strip("`").splitlines())
            nodes.append(code_block_node(code_text))
            continue

        # Headings
        heading_match = re.match(r"^(#{1,6})\s+(.*)", block)
        if heading_match:
            level = len(heading_match.group(1))
            content = heading_match.group(2).strip()
            nodes.append(ParentNode(f"h{level}", parse_inline(content)))
            continue

        # Blockquote
        if block.startswith("> "):
            content = block[2:].strip()
            child_nodes = text_to_children(content)
            nodes.append(ParentNode("blockquote", child_nodes))
            continue

        # Ordered list
        if re.match(r"^(\d+\.)\s+", block):
            list_items = []
            for line in block.splitlines():
                m = re.match(r"^\d+\.\s+(.*)", line)
                if m:
                    item_nodes = text_to_children(m.group(1))
                    list_items.append(ParentNode("li", item_nodes))
            nodes.append(ParentNode("ol", list_items))
            continue

        # Unordered list
        if re.match(r"^-\s+", block):
            list_items = []
            for line in block.splitlines():
                m = re.match(r"^-\s+(.*)", line)
                if m:
                    item_nodes = text_to_children(m.group(1))
                    list_items.append(ParentNode("li", item_nodes))
            nodes.append(ParentNode("ul", list_items))
            continue

        # Paragraph
        nodes.extend(paragraphs_from_text(block))

    return nodes


def render_node(node):
    """
    Recursively render nodes to HTML.
    """
    if hasattr(node, "value") and node.value is not None:
        return node.value
    elif hasattr(node, "children"):
        inner = "".join(render_node(c) for c in node.children)
        if hasattr(node, "tag") and node.tag:
            return f"<{node.tag}>{inner}</{node.tag}>"
        return inner
    return ""

import re

from nodes import LeafNode, ParentNode


def parse_inline(text):
    """
    Parse inline Markdown elements and return a list of HTML nodes.
    Supports:
      - Bold: **text**
      - Italic: *text*
      - Inline code: `code`
      - Links: [label](url)
      - Images: ![alt](url)
    """
    nodes = []
    pos = 0

    patterns = [
        (
            r"!\[([^\]]+)\]\(([^)]+)\)",
            lambda m: LeafNode("img", "", {"src": m.group(2), "alt": m.group(1)}),
        ),
        (
            r"\[([^\]]+)\]\(([^)]+)\)",
            lambda m: ParentNode(
                "a", [LeafNode(None, m.group(1))], {"href": m.group(2)}
            ),
        ),
        (r"\*\*([^*]+)\*\*", lambda m: ParentNode("b", [LeafNode(None, m.group(1))])),
        (r"\*([^*]+)\*", lambda m: ParentNode("i", [LeafNode(None, m.group(1))])),
        (r"`([^`]+)`", lambda m: ParentNode("code", [LeafNode(None, m.group(1))])),
    ]

    while pos < len(text):
        match = None
        for pattern, handler in patterns:
            match = re.search(pattern, text[pos:])
            if match:
                start, end = match.span()
                start += pos
                end += pos
                # Plain text before match
                if start > pos:
                    nodes.append(LeafNode(None, text[pos:start]))
                nodes.append(handler(match))
                pos = end
                break
        if not match:
            nodes.append(LeafNode(None, text[pos:]))
            break

    return nodes


def text_to_children(text):
    """Convert plain text into inline nodes."""
    return parse_inline(text.strip())


def paragraphs_from_text(text):
    """Split text into paragraphs and wrap each in <p> tags."""
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    return [ParentNode("p", parse_inline(p)) for p in paragraphs]


def code_block_node(code):
    """Wrap code block text inside <pre><code> tags."""
    return ParentNode("pre", [ParentNode("code", [LeafNode(None, code.strip())])])

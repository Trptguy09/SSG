import re

from nodes import LeafNode, ParentNode


def parse_inline(text):
    """
    Parse inline Markdown and return a list of nodes.
    Supports:
      - Bold: **text**
      - Italic: *text* or _text_
      - Link: [label](url)
      - Inline code: `code`
      - Image: ![alt](url)
    """
    if not text:
        return []

    patterns = [
        (
            r"!\[(.*?)\]\((.*?)\)",
            lambda m: LeafNode("img", {"src": m[1], "alt": m[0]}, void=True),
        ),
        (r"\*\*(.*?)\*\*", lambda m: ParentNode("b", [LeafNode(None, m[0])])),
        (r"\*(.*?)\*", lambda m: ParentNode("i", [LeafNode(None, m[0])])),
        (r"_(.*?)_", lambda m: ParentNode("i", [LeafNode(None, m[0])])),
        (
            r"\[(.*?)\]\((.*?)\)",
            lambda m: ParentNode("a", [LeafNode(None, m[0])], href=m[1]),
        ),
        (r"`(.*?)`", lambda m: LeafNode("code", m[0])),
    ]

    def split_text(t):
        for pattern, constructor in patterns:
            match = re.search(pattern, t)
            if match:
                start, end = match.span()
                before = t[:start]
                matched_node = constructor(match.groups())
                after = t[end:]
                return split_text(before) + [matched_node] + split_text(after)
        return [LeafNode(None, t)]

    nodes = split_text(text)

    # Remove empty nodes
    def is_non_empty_node(node):
        if isinstance(node, LeafNode):
            return node.value not in (None, "")
        elif isinstance(node, ParentNode):
            return bool(node.children)
        return False

    return [n for n in nodes if is_non_empty_node(n)]


def text_to_children(text):
    """
    Returns inline nodes only (no <p> wrappers).
    """
    return parse_inline(text)


def paragraphs_from_text(text):
    """
    Wraps each non-empty line in a <p> node (for real paragraphs).
    """
    children = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            children.append(ParentNode("p", parse_inline(line)))
    return children


def code_block_node(code_text):
    """
    Converts code block text into <pre><code>…</code></pre>
    """
    return ParentNode("pre", [ParentNode("code", [LeafNode(None, code_text)])])

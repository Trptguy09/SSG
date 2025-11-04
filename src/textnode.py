from enum import Enum

from htmlnode import LeafNode, ParentNode


class TextType(Enum):
    TEXT = "text"
    CODE = "code"
    BOLD = "bold"
    ITALIC = "italic"
    LINK = "link"


class TextNode:
    def __init__(self, text, text_type=TextType.TEXT):
        self.text = text
        self.text_type = text_type


def text_node_to_html_node(node):
    """
    Convert a TextNode to an HTML node.
    Returns None if the TextNode is empty, to prevent LeafNode errors.
    """
    if not node.text or node.text.strip() == "":
        return None

    if node.text_type == TextType.TEXT:
        return LeafNode(node.text)
    elif node.text_type == TextType.CODE:
        return LeafNode(node.text)
    elif node.text_type == TextType.BOLD:
        return ParentNode("<strong>", [LeafNode(node.text)])
    elif node.text_type == TextType.ITALIC:
        return ParentNode("<em>", [LeafNode(node.text)])
    elif node.text_type == TextType.LINK:
        url, label = ("#", node.text)
        if "|" in node.text:
            url, label = node.text.split("|", 1)
        return ParentNode(f'<a href="{url}">', [LeafNode(label)])
    else:
        return LeafNode(node.text)

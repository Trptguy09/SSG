from delimiter import split_nodes_delimiter
from textnode import TextNode, TextType


def text_to_textnodes(text):
    node_list = [TextNode(text, TextType.TEXT)]

    # Bold (**text**)
    node_list = split_nodes_delimiter(node_list, "**", TextType.BOLD)

    # Italic (*text*)
    node_list = split_nodes_delimiter(node_list, "*", TextType.ITALIC)

    # Inline code (`code`)
    node_list = split_nodes_delimiter(node_list, "`", TextType.CODE)

    # You can add more inline types (links, etc.) here

    return node_list

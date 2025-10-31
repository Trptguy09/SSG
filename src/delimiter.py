from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_node = []
    for old in old_nodes:
        pieces = []
        if old is not TextType.TEXT:
            new_node.append(old)
            continue
        parts = old.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception("Invalid Markdown Syntax")
        for i, chunk in enumerate(parts):
            node_type = TextType.TEXT if i % 2 == 0 else text_type
            pieces.append((TextNode(chunk, node_type)))
        new_node.extend(pieces)
    return new_node

from extract_links import extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType


def split_nodes_image(old_nodes):
    new_node = []
    for old in old_nodes:
        if old.text_type is not TextType.TEXT:
            new_node.append(old)
            continue

        text = old.text
        images = extract_markdown_images(text)

        if not images:
            new_node.append(old)
            continue

        pieces = []
        for alt, url in images:
            image_syntax = f"![{alt}]({url})"
            parts = text.split(image_syntax, 1)
            if len(parts) > 1:
                if parts[0]:
                    pieces.append(TextNode(parts[0], TextType.TEXT))
                pieces.append(TextNode(alt, TextType.IMAGE, url))
                text = parts[1]
        if text:
            pieces.append(TextNode(text, TextType.TEXT))

        new_node.extend(pieces)
    return new_node


def split_nodes_link(old_nodes):
    new_node = []
    for old in old_nodes:
        if old.text_type is not TextType.TEXT:
            new_node.append(old)
            continue

        text = old.text
        links = extract_markdown_links(text)

        if not links:
            new_node.append(old)
            continue

        pieces = []
        for label, url in links:
            link_syntax = f"[{label}]({url})"
            parts = text.split(link_syntax, 1)
            if len(parts) > 1:
                if parts[0]:
                    pieces.append(TextNode(parts[0], TextType.TEXT))
                pieces.append(TextNode(label, TextType.LINK, url))
                text = parts[1]
        if text:
            pieces.append(TextNode(text, TextType.TEXT))

        new_node.extend(pieces)
    return new_node

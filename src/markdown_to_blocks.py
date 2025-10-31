import re
from enum import Enum

from htmlnode import ParentNode
from text_textnode_list import text_to_textnodes
from textnode import TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    final = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        stripped = block.strip()
        if stripped != "":
            final.append(stripped)
    return final


def block_to_block_type(block):
    lines = block.splitlines()
    first_line = lines[0]
    last_line = lines[-1]

    if re.match(r"^#{1,6} .+$", first_line):
        return BlockType.HEADING

    if first_line.startswith("```") and last_line.endswith("```"):
        return BlockType.CODE

    if all(re.match(r"^> .*$", line) for line in lines):
        return BlockType.QUOTE

    if all(re.match(r"^- .+$", line) for line in lines):
        return BlockType.UNORDERED_LIST

    if all(re.match(r"^\d+\. .+$", line) for line in lines):
        numbers = [int(re.match(r"^(\d+)\. ", line).group(1)) for line in lines]
        if numbers == list(range(1, len(lines) + 1)):
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = [text_to_textnodes(node) for node in text_nodes]
    return html_nodes


def markdown_to_html_node(markdown):

    blocks = markdown_to_blocks(markdown)

    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            children = text_to_children(block)
            block_nodes.append(ParentNode("<p>", children))

        elif block_type is BlockType.HEADING:
            hash_count = len(block.split(" ")[0])
            text = block[hash_count + 1 :]
            children = text_to_children(text)
            block_nodes.append(ParentNode(f"<h{hash_count}>", children))

        elif block_type is BlockType.QUOTE:
            quote_text = "\n".join(
                line.lstrip("> ").rstrip() for line in block.splitlines()
            )
            children = text_to_children(quote_text)
            block_nodes.append(ParentNode("<blockquote>", children))

        elif block_type is BlockType.ORDERED_LIST:
            list_items = []
            for line in block.splitlines():
                item_text = line.split(". ", 1)[1]
                children = text_to_children(item_text)
                list_items.append(ParentNode("li", children))
            block_nodes.append(ParentNode("ol", list_items))

        elif block_type is BlockType.UNORDERED_LIST:
            list_items = []
            for line in block.splitlines():
                item_text = line.lstrip("- ").rstrip()
                children = text_to_children(item_text)
                list_items.append(ParentNode("<li>", children))
            block_nodes.append(ParentNode("<ol>", list_items))

        elif block_type is BlockType.CODE:
            code_text = block.strip("`").strip()
            text_node = TextNode(code_text, TextType.CODE)
            code_child = text_node_to_html_node(text_node)
            block_nodes.append(
                ParentNode("<pre>", [ParentNode("<code>", [code_child])])
            )

        return ParentNode("<div>", block_nodes)

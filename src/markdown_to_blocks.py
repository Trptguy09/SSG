import re
from enum import Enum


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


def markdown_to_html_node(markdown):
    blocks = markdown.split()
    for block in blocks:
        block_type = block_to_block_type(block)

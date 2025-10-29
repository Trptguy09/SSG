import unittest

from delimiter import split_nodes_delimiter
from markdown_to_blocks import BlockType, block_to_block_type, markdown_to_blocks
from split_nodes import split_nodes_image, split_nodes_link
from text_textnode_list import text_to_textnodes
from textnode import TextNode, TextType


class TestTextToTextNodes(unittest.TestCase):

    def test_plain_text(self):
        text = "Hello world"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 1
        assert nodes[0] == TextNode("Hello world", TextType.TEXT)

    def test_bold_text(self):
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        assert nodes == [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

    def test_italic_text(self):
        text = "This is *italic* text"
        nodes = text_to_textnodes(text)
        assert nodes == [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]

    def test_code_text(self):
        text = "Here is some `code` sample"
        nodes = text_to_textnodes(text)
        assert nodes == [
            TextNode("Here is some ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" sample", TextType.TEXT),
        ]

    def test_image_parsing(self):
        text = "Look at this ![alt text](image.png)"
        nodes = text_to_textnodes(text)
        assert nodes == [
            TextNode("Look at this ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "image.png"),
        ]

    def test_link_parsing(self):
        text = "Visit [Boot.dev](https://boot.dev) for learning"
        nodes = text_to_textnodes(text)
        assert nodes == [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
            TextNode(" for learning", TextType.TEXT),
        ]

    def test_combined_markdown(self):
        text = "Check *this* **out** `code` [Boot.dev](https://boot.dev)"
        nodes = text_to_textnodes(text)
        assert nodes == [
            TextNode("Check ", TextType.TEXT),
            TextNode("this", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("out", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
        ]

    def text_to_textnodes(text):
        node_list = [TextNode(text, TextType.TEXT)]
        node_list = split_nodes_delimiter(node_list, "**", TextType.BOLD)
        node_list = split_nodes_delimiter(node_list, "*", TextType.ITALIC)
        node_list = split_nodes_delimiter(node_list, "`", TextType.CODE)
        node_list = split_nodes_image(node_list)
        node_list = split_nodes_link(node_list)
        return node_list

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):

    def test_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code_block(self):
        block = "```\nprint('Hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> this is a quote\n> with two lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- item 1\n- item 2\n- item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list_valid(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_invalid_numbers(self):
        block = "1. first\n3. second\n4. third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph(self):
        block = "This is a simple paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_mixed_invalid_quote(self):
        block = "> valid line\nno marker line"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_not_heading(self):
        block = "####### too many hashes"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()

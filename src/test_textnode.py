import unittest

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


if __name__ == "__main__":
    unittest.main()

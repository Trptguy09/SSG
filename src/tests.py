import unittest

from markdown_to_blocks import markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):

    def test_paragraph(self):
        md = "This is *italic* and **bold** text."
        root = markdown_to_html_node(md)
        self.assertEqual(root.tag, "<div>")
        self.assertEqual(root.children[0].tag, "<p>")

    def test_heading(self):
        md = "# Hello World"
        root = markdown_to_html_node(md)
        self.assertEqual(root.children[0].tag, "<h1>")

    def test_code_block(self):
        md = "```\nprint('hi')\n```"
        root = markdown_to_html_node(md)
        code_node = root.children[0]
        self.assertEqual(code_node.tag, "<pre>")
        self.assertEqual(code_node.children[0].tag, "<code>")

    def test_quote_block(self):
        md = "> Quoted text"
        root = markdown_to_html_node(md)
        self.assertEqual(root.children[0].tag, "<blockquote>")

    def test_unordered_list(self):
        md = "- Item 1\n- Item 2"
        root = markdown_to_html_node(md)
        ul = root.children[0]
        self.assertEqual(ul.tag, "<ul>")
        self.assertEqual(len(ul.children), 2)
        self.assertEqual(ul.children[0].tag, "<li>")

    def test_ordered_list(self):
        md = "1. First\n2. Second"
        root = markdown_to_html_node(md)
        ol = root.children[0]
        self.assertEqual(ol.tag, "<ol>")
        self.assertEqual(len(ol.children), 2)
        self.assertEqual(ol.children[1].tag, "<li>")


if __name__ == "__main__":
    unittest.main()

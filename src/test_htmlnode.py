import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("<p>", "this is the text inside a paragraph")
        node2 = HTMLNode("<p>", "this is the text inside a paragraph")
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()

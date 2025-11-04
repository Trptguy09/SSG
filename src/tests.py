import unittest

from src.markdown_utils import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_basic_h1(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_h1_with_spaces(self):
        self.assertEqual(extract_title("#   Hello World  "), "Hello World")

    def test_no_h1(self):
        with self.assertRaises(Exception):
            extract_title("No header here")


if __name__ == "__main__":
    unittest.main()

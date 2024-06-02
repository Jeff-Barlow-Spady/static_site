import unittest
from markdown_blocks import (block_to_block_type,
                             markdown_to_blocks, 
                             block_type_quote,
                             block_type_code,
                             block_type_unordered_list,
                             block_type_ordered_list,
                             block_type_heading,
                             block_type_paragraph,
                             ) 


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )
class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        block = "# Heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)

    def test_code_block(self):
        block = "```\nCode block\n```"
        self.assertEqual(block_to_block_type(block), block_type_code)

    def test_quote_block(self):
        block = "> Quote block"
        self.assertEqual(block_to_block_type(block), block_type_quote)

    def test_unordered_list(self):
        block = "- Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(block), block_type_unordered_list)

    def test_ordered_list(self):
        block = "1. Item 1\n2. Item 2"
        self.assertEqual(block_to_block_type(block), block_type_ordered_list)

    def test_paragraph(self):
        block = "This is a paragraph."
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

    def test_empty_block(self):
        block = ""
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

    def test_whitespace_block(self):
        block = "   \n\n   "
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

if __name__ == "__main__":
    unittest.main()
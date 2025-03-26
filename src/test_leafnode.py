import unittest
from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_initialization_with_valid_parameters(self):
        node = LeafNode(tag="p", value="Sample text")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Sample text")
        self.assertIsNone(node.children)

    def test_initialization_with_none_value(self):
        with self.assertRaises(ValueError):
            leaf_node = LeafNode(tag="p", value=None)
            leaf_node.to_html()  # Should raise ValueError

    def test_to_html_with_tag(self):
        node = LeafNode(tag="p", value="Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_without_tag(self):
        node = LeafNode(tag=None, value="Just text")
        self.assertEqual(node.to_html(), "Just text")

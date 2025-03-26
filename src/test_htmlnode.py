import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_default_initialization(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def initialization_with_values(self):
        node = HTMLNode(
            tag="div", value="Hello", children=[], props={"class": "container"}
        )
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "container"})

    def test_props_to_html(self):
        node = HTMLNode(props={"class": "btn", "id": "submit-btn"})
        self.assertEqual(node.props_to_html(), ' class="btn" id="submit-btn"')

    def test_props_to_html_empty(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_to_html_not_implemented(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node = HTMLNode(
            tag="p", value="Hello", children=[], props={"style": "color:red;"}
        )
        expected_repr = "HTMLNode(p, Hello, [], {'style': 'color:red;'})"
        self.assertEqual(repr(node), expected_repr)

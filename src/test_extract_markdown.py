import unittest
from utils import extract_markdown_images, extract_markdown_links


class TestExtractMarkdownImage(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "This is a text with a ![rick roll](https://i.imgur.com/aKa0qIh.gif)"
            " and ![obi van](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertEqual(
            [
                ("rick roll", "https://i.imgur.com/aKa0qIh.gif"),
                ("obi van", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_no_images(self):
        matches = extract_markdown_images("This is a plain text with no images")
        self.assertEqual([], matches)

    def test_malformed_image_markdown(self):
        matches = extract_markdown_images(
            "This is broken ![no_url] and ![incomplete](missing_parent)"
        )
        self.assertEqual([], matches)


class TestExtractMarkdownLink(unittest.TestCase):
    def test_extract_markdown_url(self):
        matches = extract_markdown_links(
            "This is a text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdev)"
        )
        self.assertEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdev"),
            ],
            matches,
        )

    def test_no_links(self):
        matches = extract_markdown_links("This is plain text with no links.")
        self.assertEqual([], matches)

    def test_malformed_links(self):
        matches = extract_markdown_links(
            "This is broken [no_url] and [incomplete](missing_parent)"
        )
        self.assertEqual([], matches)

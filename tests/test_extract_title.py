import unittest
from src.markdown_blocks import extract_title


class TestExtractTitle(unittest.TestCase):

    def test_valid_title(self):
        got = extract_title("# Hello")
        want = "Hello"

        self.assertEqual(got, want)

    def test_title_with_extra_spaces(self):
        got = extract_title("   # Trimmed  ")
        want = "Trimmed"

        self.assertEqual(got, want)

    def test_multiline_markdown(self):
        markdown = """
        # My title 
        Some content here 
        ## Subtitle
        """
        got = extract_title(markdown)
        want = "My title"

        self.assertEqual(got, want)

    def test_title_with_speciaal_characters(self):
        markdown = "# @Special_Char!"
        got = extract_title(markdown)
        want = "@Special_Char!"

        self.assertEqual(got, want)

    def test_missing_h1_title(self):
        with self.assertRaises(ValueError):
            extract_title("## No H1 title here")

    def test_embedded_h1_title(self):
        markdown = """
        # First Title 
        Some paragraph 
        # Second Title
        """
        got = extract_title(markdown)
        want = "First Title"
        self.assertEqual(got, want)

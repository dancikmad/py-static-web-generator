from enum import Enum
from typing import List

from src.htmlnode import ParentNode
from src.textnode import TextNode, TextType, text_node_to_html_node
from src.utils import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> List[str]:
    """
    Splits a raw Markdownn into a list of block strings.

    Parameters:
    ----------
    markdown: str
        A block of raw Markdown text.
    Returns:
    --------
    block_strings: List[str]
        A list of "block" strings containing inline texts.
    """
    blocks = []
    for block in markdown.split("\n\n"):
        stripped_lines = [line.strip() for line in block.split("\n") if line.strip()]
        if stripped_lines:
            blocks.append("\n".join(stripped_lines))
    return blocks


def extract_title(markdown):
    for line in markdown.split("\n"):  # Check each line
        if line.strip().startswith("# "):  # Find first H1 header
            return line.strip()[2:].strip()  # Remove '# ' and extra spaces

    raise ValueError("The markdown doesn't contain an H1 title")


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    # Check for code block(```at start and end)
    if lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE

    # Check for heading (# followed by space)
    if lines[0].startswith("# "):
        return BlockType.HEADING

    if any(lines[0].startswith(f"{'#' * i} ") for i in range(1, 7)):
        return BlockType.HEADING

    # Check for quote block (every line starts with ">")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Check for unordered list (every line starts with "- ")
    if all(line.startswith("- ") for line in lines):
        return BlockType.ULIST

    # Check for ordered list (lines start with "1. ", "2. ", "3. ", etc.)
    if all(line.split(". ")[0].isdigit() and line.split(". ")[1:] for line in lines):
        numbers = [int(line.split(". ")[0]) for line in lines]
        if numbers == list(range(1, len(numbers) + 1)):
            return BlockType.OLIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

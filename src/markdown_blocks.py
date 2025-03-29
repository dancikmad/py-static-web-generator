from enum import Enum
from typing import List


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

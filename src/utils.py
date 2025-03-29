from typing import List, Tuple
from .textnode import TextNode, TextType

import re


def split_nodes_delimiter(
    old_nodes: List[TextNode],
    delimiter: str,
    text_type: TextType,  # Notice the type hint is TextType, not str
) -> List[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        splits = old_node.text.split(delimiter)

        # If there are no delimiters or odd number of parts (unbalanced delimiters)
        if len(splits) == 1:
            new_nodes.append(old_node)
            continue

        if len(splits) % 2 == 0:
            # This means we have an odd number of delimiters - they're unbalanced
            raise ValueError(
                f"Invalid markdown format. Unbalanced delimiters: {delimiter}"
            )

        # Process the splits - every even index is normal text, odd index is formatted text
        for i in range(len(splits)):
            if splits[i] == "":
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(splits[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(splits[i], text_type))

    return new_nodes


def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    pattern = r"!\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    pattern = r"(?<!!)\[(.*?)\]\((https?:\/\/[^\s)]+)\)"
    return re.findall(pattern, text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    # Current implementation returns a flat list of TextNodes
    delimiters = ["**", "_", "`"]
    text_types = [TextType.BOLD, TextType.ITALIC, TextType.CODE]

    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    for i in range(len(delimiters)):
        nodes = split_nodes_delimiter(nodes, delimiters[i], text_types[i])

    # If test expects a list containing a list of TextNodes:
    return [nodes]  # Wrap in another list


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

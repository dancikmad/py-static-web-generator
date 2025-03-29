from typing import List, Tuple
from textnode import TextNode, TextType
import re


def split_nodes_delimiter(
    old_nodes: List[TextNode],
    delimiter: str,
    text_type: str,
) -> List[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            split_parts = node.text.split(delimiter)

            if len(split_parts) % 2 == 0:
                raise ValueError(f"Unmatched delimiter '{delimiter}' in: {node.text}")

            for index, part in enumerate(split_parts):
                if part:  # Ignore empty strings
                    if index % 2 == 0:
                        new_nodes.append(TextNode(part, TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(part, text_type))
        else:
            new_nodes.append(node)

    return new_nodes


def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    pattern = r"!\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    pattern = r"(?<!!)\[(.*?)\]\((https?:\/\/[^\s)]+)\)"
    return re.findall(pattern, text)

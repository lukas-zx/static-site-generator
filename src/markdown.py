import re
from textnode import TextNode, TextType, text_node_to_html_node


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    res: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            res.append(old_node)

        parts = old_node.text.split(delimiter)
        if len(parts) < 3:
            raise Exception(f"invalid markdown syntax: {old_node.text}")

        node1 = TextNode(parts[0], TextType.TEXT)
        node2 = TextNode(parts[1], text_type)
        node3 = TextNode(parts[2], TextType.TEXT)

        res.append(node1)
        res.append(node2)
        res.append(node3)
    return res

def extract_markdown_images(text: str) -> list[tuple]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

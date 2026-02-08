import re
from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    res: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            res.append(old_node)
            continue

        parts = old_node.text.split(delimiter)
        if len(parts) != 3:
            res.append(old_node)
            continue

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


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    res: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            res.append(old_node)
            continue

        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            res.append(old_node)
            continue

        remaining_text = old_node.text
        for image in images:
            parts = remaining_text.split(f"![{image[0]}]({image[1]})", 1)
            res.append(TextNode(parts[0], TextType.TEXT))
            res.append(TextNode(image[0], TextType.IMAGE, image[1]))
            remaining_text = parts[1]

        if remaining_text != "":
            res.append(TextNode(remaining_text, TextType.TEXT))

    return res


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    res: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            res.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)
        if len(links) == 0:
            res.append(old_node)
            continue

        remaining_text = old_node.text
        for link in links:
            parts = remaining_text.split(f"[{link[0]}]({link[1]})", 1)
            res.append(TextNode(parts[0], TextType.TEXT))
            res.append(TextNode(link[0], TextType.LINK, link[1]))
            remaining_text = parts[1]

        if remaining_text != "":
            res.append(TextNode(remaining_text, TextType.TEXT))

    return res


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

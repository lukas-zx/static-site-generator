import re
from htmlnode import HTMLNode
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


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


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    res = []
    for block in blocks:
        block = block.strip()
        if block != "":
            res.append(block)
    return res


def block_to_block_type(block: str) -> BlockType:
    if bool(re.match(r"^#{1,6} ", block)):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith("> "):
        return BlockType.QUOTE

    is_ul = True
    lines = block.split("\n")
    for line in lines:
        if not line.startswith("- "):
            is_ul = False
            break
    if is_ul:
        return BlockType.UNORDERED_LIST

    is_ol = True
    OL_REGEX = re.compile(r"^\d+\. ")
    for line in lines:
        if not OL_REGEX.match(line):
            is_ol = False
            break
    if is_ol:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(text: str) -> list[HTMLNode]:
    textnodes = text_to_textnodes(text)
    res = []
    for textnode in textnodes:
        res.append(text_node_to_html_node(textnode))
    return res


def block_to_html_node(block: str) -> HTMLNode:
    match block_to_block_type(block):
        case BlockType.PARAGRAPH:
            parent = ParentNode("p", None)
            children = text_to_children(block.replace("\n", " "))
            parent.children = children
            return parent
        case BlockType.HEADING:
            level = 0
            while level < len(block) and block[level] == "#":
                level += 1
            parent = ParentNode(f"h{level}", None)
            children = text_to_children(block[level + 1 :])
            parent.children = children
            return parent
        case BlockType.CODE:
            code = ParentNode("code", None)
            pre = ParentNode("pre", [code])
            child = TextNode(block.strip("```").lstrip(), TextType.TEXT)
            child = text_node_to_html_node(child)
            code.children = [child]
            return pre
        case BlockType.QUOTE:
            parent = ParentNode("blockquote", None)
            children = text_to_children(block.lstrip("> "))
            parent.children = children
            return parent
        case BlockType.UNORDERED_LIST:
            ul = ParentNode("ul", None)
            lis: list[HTMLNode] = []
            lines = block.split("\n")
            for line in lines:
                li = ParentNode("li", None)
                children = text_to_children(line.lstrip("- "))
                li.children = children
                lis.append(li)
            ul.children = lis
            return ul
        case BlockType.ORDERED_LIST:
            ol = ParentNode("ol", None)
            lis: list[HTMLNode] = []
            lines = block.split("\n")
            for line in lines:
                line = line[3:]
                li = ParentNode("li", None)
                children = text_to_children(line)
                li.children = children
                lis.append(li)
            ol.children = lis
            return ol


def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    parent = ParentNode("div", [], None)
    for block in blocks:
        if parent.children is None:
            parent.children = block_to_html_node(block)
        else:
            parent.children.append(block_to_html_node(block))
    return parent

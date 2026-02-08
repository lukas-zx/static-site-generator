import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.PLAIN)
        node2 = TextNode("This is a different text node", TextType.PLAIN)
        self.assertNotEqual(node, node2)

    def test_url_neq(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://self.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "http://other.dev")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()

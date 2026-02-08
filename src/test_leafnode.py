import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_props_a(self):
        href = "http://some-url.com"
        target = "_blank"
        value = "This is a link node"

        expected = f"<a href={href} target={target}>{value}</a>"
        actual = LeafNode(
            "a",
            "This is a link node",
            {
                "href": href,
                "target": target,
            },
        ).to_html()

        self.assertEqual(actual, expected)

    def test_plain_text(self):
        value = "This is plain text"

        actual = LeafNode(
            None,
            value,
        ).to_html()

        self.assertEqual(actual, value)


if __name__ == "__main__":
    unittest.main()

import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_a(self):
        href = "http://some-url.com"
        target = "_blank"

        expected = f" href={href} target={target}"
        actual = HTMLNode(
            "a",
            "This is a link node",
            None,
            {
                "href": href,
                "target": target,
            },
        ).props_to_html()

        self.assertEqual(actual, expected)

    def test_props_img(self):
        src = "http://some-img.com"
        alt = "some image"

        expected = f" src={src} alt={alt}"
        actual = HTMLNode(
            "img",
            "This is an image node",
            None,
            {
                "src": src,
                "alt": alt,
            },
        ).props_to_html()

        self.assertEqual(actual, expected)

    def test_props_class(self):
        class_name = "container"

        expected = f" class={class_name}"
        actual = HTMLNode(
            "div",
            "This is a container node",
            None,
            {
                "class": class_name,
            },
        ).props_to_html()

        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()

from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        children: list[HTMLNode] | None,
        props: dict | None = None,
    ) -> None:
        super().__init__(tag, None, children, props)


    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("tag must be set")

        if not self.children:
            raise ValueError("children must not be empty")

        res = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            res += child.to_html()
        res += f"</{self.tag}>"
        
        return res



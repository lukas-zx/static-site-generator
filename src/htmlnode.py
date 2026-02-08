from __future__ import annotations


class HTMLNode:
    def __init__(
        self,
        tag: str | None,
        value: str | None,
        children: list[HTMLNode] | None,
        props: dict | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        res = ""
        if self.props is None:
            return res

        for key in self.props:
            res += f" {key}={self.props[key]}"
        return res

    def __repr__(self) -> str:
        return f"HTMLNode(Tags: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props})"

from typing import Optional


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[list["HTMLNode"]] = None,
        props: Optional[dict[str, str]] = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self) -> str:
        html_text = ""
        for key, value in self.props.items():
            html_text += f' {key}="{value}"'

        return html_text

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        props: Optional[dict[str, str]] = None,
    ):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self) -> str:
        if self.value == None:
            raise ValueError()

        if self.tag == None:
            return self.value

        return f"<{self.tag}>{self.value}</{self.tag}>"

class HTMLNode:
    """Base class for HTML nodes."""

    def __init__(self, tag=None, children=None, text=None, props=None):
        self.tag = tag
        self.children = children or []
        self.text = text or ""
        self.props = props or {}

    def props_to_html(self):
        """Convert props dictionary to HTML attributes."""
        if not self.props:
            return ""
        return " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())

    def to_html(self):
        """Render node to HTML string. Must be overridden."""
        raise NotImplementedError("Subclasses must implement to_html().")


class LeafNode(HTMLNode):
    """Represents an HTML element with no children (text or self-closing)."""

    def __init__(self, tag=None, text="", props=None):
        super().__init__(tag, None, text, props)

    def to_html(self):
        if self.tag is None:
            # plain text node
            return self.text
        elif self.tag == "img":
            # self-closing tag
            return f"<{self.tag}{self.props_to_html()}>"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.text}</{self.tag}>"


class ParentNode(HTMLNode):
    """Represents an HTML element that wraps child nodes."""

    def __init__(self, tag, children, props=None):
        super().__init__(tag, children, None, props)

    def to_html(self):
        if self.tag is None:
            # should not happen for ParentNode
            return "".join(child.to_html() for child in self.children)
        inner_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{inner_html}</{self.tag}>"

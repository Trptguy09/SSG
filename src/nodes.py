class LeafNode:
    """
    Represents a leaf HTML node (text, inline code, or void elements like <img>)
    """

    def __init__(self, tag, value=None, void=False):
        """
        :param tag: HTML tag name (e.g., "code", "img"), or None for plain text
        :param value: Text content or dictionary of attributes for void elements
        :param void: True if this is a void element (e.g., <img />)
        """
        self.tag = tag
        self.value = value
        self.void = void

    def to_html(self):
        if self.void:
            # Void element: value is expected to be a dict of attributes
            if isinstance(self.value, dict):
                attrs = " ".join(f'{k}="{v}"' for k, v in self.value.items())
                return f"<{self.tag} {attrs} />"
            else:
                return f"<{self.tag} />"
        elif self.tag:
            # Inline element with text content
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            # Plain text node
            return self.value or ""


class ParentNode:
    """
    Represents a parent HTML node with children (e.g., <p>, <div>, <a>)
    """

    def __init__(self, tag, children=None, **attrs):
        """
        :param tag: HTML tag name (e.g., "p", "a", "div")
        :param children: List of child nodes (LeafNode or ParentNode)
        :param attrs: Optional HTML attributes (e.g., href="url")
        """
        self.tag = tag
        self.children = children or []
        self.attrs = attrs  # HTML attributes like href

    def to_html(self):
        # Build attribute string
        attr_str = " ".join(f'{k}="{v}"' for k, v in self.attrs.items())
        if attr_str:
            attr_str = " " + attr_str
        # Render children recursively
        inner_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{attr_str}>{inner_html}</{self.tag}>"

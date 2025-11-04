class LeafNode:
    def __init__(self, tag, value="", props=None):
        self.tag = tag
        self.value = value or ""
        self.props = props or {}

    def _render_props(self):
        return (
            " ".join(f'{k}="{v}"' for k, v in self.props.items()) if self.props else ""
        )

    def to_html(self):
        void_tags = {
            "area",
            "base",
            "br",
            "col",
            "embed",
            "hr",
            "img",
            "input",
            "link",
            "meta",
            "param",
            "source",
            "track",
            "wbr",
        }

        props_str = self._render_props()
        if self.tag in void_tags:
            return f"<{self.tag} {props_str} />" if props_str else f"<{self.tag} />"
        else:
            return (
                f"<{self.tag} {props_str}>{self.value}</{self.tag}>"
                if props_str
                else f"<{self.tag}>{self.value}</{self.tag}>"
            )


class ParentNode:
    def __init__(self, tag, children=None, props=None):
        self.tag = tag
        self.children = children or []
        self.props = props or {}

    def _render_props(self):
        return (
            " ".join(f'{k}="{v}"' for k, v in self.props.items()) if self.props else ""
        )

    def to_html(self):
        inner_html = "".join(child.to_html() for child in self.children)
        props_str = self._render_props()
        return (
            f"<{self.tag} {props_str}>{inner_html}</{self.tag}>"
            if props_str
            else f"<{self.tag}>{inner_html}</{self.tag}>"
        )

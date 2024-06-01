class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop, value in self.props.items():
            if prop is not None and value is not None:
                props_html += f' {prop}="{value}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("Leaf nodes require a value.")
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf nodes require a value.")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


  
class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        self.tag = tag
        self.children = children
        self.props = props


    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent nodes require a tag.")
        if self.children is None:
            raise ValueError("Parent nodes require children.")
        children = ""
        for child in self.children:
            children += child.to_html()
        if self.props is None:
            return f"<{self.tag}>{children}</{self.tag}>"
        props_html = ""
        for props in self.props:
            props_html += f' {props}="{self.props[props]}"'
        return f"<{self.tag}{props_html}>{children}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"

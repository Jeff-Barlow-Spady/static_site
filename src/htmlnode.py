class HTMLNode:
    """
    Base class for HTML nodes.

    Attributes:
        tag (str): The HTML tag for the node.
        value (str): The value or content of the node.
        children (list): A list of child nodes.
        props (dict): A dictionary of HTML attributes and their values.
    """
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """
        Convert the node to an HTML string.

        Raises:
            NotImplementedError: This method should be implemented by subclasses.
        """
        raise NotImplementedError

    def props_to_html(self):
        """
        Convert the props dictionary to an HTML attribute string.

        Returns:
            str: A string representing the HTML attributes.

        Raises:
            InvalidPropsError: If the props dictionary contains invalid keys or values.
        """
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
    """
    A leaf node in the HTML tree, representing a self-closing or text node.

    Attributes:
        tag (str): The HTML tag for the node.
        value (str): The value or content of the node.
        props (dict): A dictionary of HTML attributes and their values.
    """
    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("Leaf nodes require a value.")
        super().__init__(tag, value, None, props)

    def to_html(self):
        """
        Convert the leaf node to an HTML string.

        Returns:
            str: The HTML string representation of the leaf node.

        Raises:
            ValueError: If the leaf node has no value.
        """
        if self.value is None:
            raise ValueError("Leaf nodes require a value.")
        if self.tag is None:
            return self.value
        if self.tag in ["img", "br", "hr", "input", "meta", "link"]:  # Add more self-closing tags as needed
            return f"<{self.tag}{self.props_to_html()} />"
        if self.tag in [
            "img",
            "br",
            "hr",
            "input",
            "meta",
            "link",
        ]:  # Add more self-closing tags as needed
            return f"<{self.tag}{self.props_to_html()} />"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


  
class ParentNode(HTMLNode):
    """
    A parent node in the HTML tree, containing child nodes.

    Attributes:
        tag (str): The HTML tag for the node.
        children (list): A list of child nodes.
        props (dict): A dictionary of HTML attributes and their values.
    """
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

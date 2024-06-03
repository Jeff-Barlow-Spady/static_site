from htmlnode import LeafNode

# Define text types
text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TextNode:
    def __init__(self, text, text_type, url=None, src=None, alt=None):
        """
        Initializes a new instance of the TextNode class.

        Args:
            text (str): The text content of the node.
            text_type (str): The type of text node.
            url (str, optional): The URL associated with the text node. Defaults to None.
            src (str, optional): The source of the text node. Defaults to None.
            alt (str, optional): The alternative text for the text node. Defaults to None.
        """
        self.text = text
        self.text_type = text_type
        self.url = url
        self.src = src
        self.alt = alt

    # Return True if all properties of two TextNode instances are identical
    def __eq__(self, other):
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
            and self.src == other.src
            and self.alt == other.alt
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url}, {self.src}, {self.alt})"
        
def text_node_to_html_node(text_node):
    """
    Converts a TextNode instance to an HTMLNode instance based on the text type.

    Args:
        text_node (TextNode): The TextNode instance to be converted.

    Returns:
        HTMLNode: The corresponding HTMLNode instance.

    Raises:
        Exception: If the text type is unknown.

    This function takes a TextNode instance and converts it to an HTMLNode instance based on the text type. If the text type is text_type_text, it returns a LeafNode with the text content. If the text type is text_type_bold, it returns a LeafNode with the text content wrapped in a <b> tag. If the text type is text_type_italic, it returns a LeafNode with the text content wrapped in an <i> tag. If the text type is text_type_code, it returns a LeafNode with the text content wrapped in a <code> tag. If the text type is text_type_link, it returns a LeafNode with the text content wrapped in an <a> tag with the href attribute set to the URL. If the text type is text_type_image, it returns a LeafNode with the text content wrapped in an <img> tag with the src and alt attributes set. If the text type is unknown, it raises an exception.
    """
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == text_type_image:
        return LeafNode("img", "", {"src": text_node.src, "alt": text_node.alt})
    else:
        raise Exception('Unknown text type')

def split_nodes_delimiter(nodes, delimiter, new_type):
    """
    Split a list of TextNode objects into a new list of TextNode objects based on a given delimiter and text type.

    Args:
        nodes (list): List of TextNode objects representing the original text.
        delimiter (str): Delimiter used to split the text into sections.
        new_type (str): Text type to assign to the sections that are split.

    Returns:
        list: New list of TextNode objects representing the split text with different formatting.

    Raises:
        ValueError: If delimiter is empty or new_type is empty.
    """
    if not nodes:
        return []
    if not delimiter:
        raise ValueError("Delimiter cannot be empty")
    if not new_type:
        raise ValueError("New type cannot be empty")

    split_nodes = []
    for node in nodes:
        if node.text_type == new_type:
            text = node.text
            start_pos = 0
            while start_pos < len(text):
                end_pos = text.find(delimiter, start_pos)
                if end_pos == -1:
                    end_pos = len(text)
                split_nodes.append(TextNode(text[start_pos:end_pos], new_type))
                start_pos = end_pos + len(delimiter)
        else:
            split_nodes.append(node)
    return split_nodes

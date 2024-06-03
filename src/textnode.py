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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not old_nodes:
        return []
    if not delimiter:
        raise ValueError("delimiter cannot be empty")
    if not text_type:
        raise ValueError("text_type cannot be empty")

    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type == text_type:
            text = old_node.text
            if delimiter in text:
                start_pos = 0
                while start_pos < len(text):
                    end_pos = text.find(delimiter, start_pos)
                    if end_pos == -1:
                        end_pos = len(text)
                    new_nodes.append(TextNode(text[start_pos:end_pos], text_type))
                    start_pos = end_pos + len(delimiter)
            else:
                new_nodes.append(old_node)
        else:
            new_nodes.append(old_node)
    return new_nodes

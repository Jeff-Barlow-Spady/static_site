import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)

def text_to_textnodes(text):
    """
    Convert a given text into a list of TextNode objects representing the text with different formatting.
    
    Args:
        text (str): The input text to be converted.
        
    Returns:
        list: A list of TextNode objects representing the text with different formatting.
        
    This function takes a given text as input and converts it into a list of TextNode objects. It first creates a single TextNode object with the input text and the text_type_text. Then, it applies different formatting delimiters such as "**" (bold), "*" (italic), and "`" (code) to the text by calling the split_nodes_delimiter function. It also splits the text into image and link nodes by calling the split_nodes_image and split_nodes_link functions respectively. Finally, it returns the list of TextNode objects representing the text with different formatting.
    """
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split a list of TextNode objects into a new list of TextNode objects based on a given delimiter and text type.

    Args:
        old_nodes (list): A list of TextNode objects representing the original text.
        delimiter (str): The delimiter used to split the text into sections.
        text_type (str): The text type to assign to the sections that are split.

    Returns:
        list: A new list of TextNode objects representing the split text with different formatting.

    Raises:
        ValueError: If the number of sections after splitting is even, indicating an invalid markdown format.

    This function takes a list of TextNode objects representing the original text and splits it into a new list of TextNode objects based on a given delimiter and text type. It iterates over each TextNode object in the old_nodes list and checks if its text_type is not equal to text_type_text. If it is not, the TextNode object is appended to the new_nodes list without modification. If it is, the text of the TextNode object is split into sections using the delimiter. If the number of sections after splitting is even, indicating an invalid markdown format, a ValueError is raised. The function then iterates over the sections and creates new TextNode objects with the appropriate text and text_type. The new TextNode objects are appended to the split_nodes list. Finally, the split_nodes list is extended into the new_nodes list and returned.
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_image(old_nodes):
    """
    Split a list of TextNode objects into a new list of TextNode objects based on image markdown.

    Args:
        old_nodes (list): A list of TextNode objects representing the original text.

    Returns:
        list: A new list of TextNode objects representing the split text with image markdown.

    Raises:
        ValueError: If the image section in the markdown is not closed.

    This function takes a list of TextNode objects representing the original text and splits it into a new list of TextNode objects based on image markdown. It iterates over each TextNode object in the old_nodes list and checks if its text_type is not equal to text_type_text. If it is not, the TextNode object is appended to the new_nodes list without modification. If it is, the text of the TextNode object is checked for image markdown. If no image markdown is found, the TextNode object is appended to the new_nodes list. If image markdown is found, the text is split into sections using the image markdown. If the number of sections after splitting is not equal to 2, indicating an invalid markdown format, a ValueError is raised. The function then iterates over the sections and creates new TextNode objects with the appropriate text and text_type. The new TextNode objects are appended to the new_nodes list. Finally, the new_nodes list is returned.
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(
                TextNode(
                    image[0],
                    text_type_image,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes


def split_nodes_link(old_nodes):
    """
    Split a list of TextNode objects into a new list of TextNode objects based on link markdown.

    Args:
        old_nodes (list): A list of TextNode objects representing the original text.

    Returns:
        list: A new list of TextNode objects representing the split text with link markdown.

    Raises:
        ValueError: If the link section in the markdown is not closed.

    This function takes a list of TextNode objects representing the original text and splits it into a new list of TextNode objects based on link markdown. It iterates over each TextNode object in the old_nodes list and checks if its text_type is not equal to text_type_text. If it is not, the TextNode object is appended to the new_nodes list without modification. If it is, the text of the TextNode object is checked for link markdown. If no link markdown is found, the TextNode object is appended to the new_nodes list. If link markdown is found, the text is split into sections using the link markdown. If the number of sections after splitting is not equal to 2, indicating an invalid markdown format, a ValueError is raised. The function then iterates over the sections and creates new TextNode objects with the appropriate text and text_type. The new TextNode objects are appended to the new_nodes list. Finally, the new_nodes list is returned.
"""
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes


def extract_markdown_images(text):
    """
    Extracts markdown images from the given text.

    Args:
        text (str): The text to extract markdown images from.

    Returns:
        List[Tuple[str, str]]: A list of tuples containing the alt text and the URL of each markdown image found in the text.

    Raises:
        None

    Example:
        >>> extract_markdown_images("![alt text](https://example.com/image.jpg)")
        [('alt text', 'https://example.com/image.jpg')]
    """
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    """
    Extracts markdown links from the given text.

    Args:
        text (str): The text to extract markdown links from.

    Returns:
        List[Tuple[str, str]]: A list of tuples containing the link text and the URL of each markdown link found in the text.

    Raises:
        None

    Example:
        >>> extract_markdown_links("[link text](https://example.com)")
        [('link text', 'https://example.com')]
    """
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches
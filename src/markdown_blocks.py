import re
from htmlnode import ParentNode
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes
block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ulist = "unordered_list"
block_type_olist = "ordered_list"
block_type_image = "image"

def markdown_to_blocks(markdown):
    """
    Splits a markdown text into blocks.

    Args:
        markdown (str): The markdown text to split into blocks.

    Returns:
        List[str]: A list of blocks, where each block is a string.

    This function takes a markdown text as input and splits it into blocks. Each block is a string. The function first splits the markdown text into blocks using the double newline character as the delimiter. It then filters out any empty blocks and strips any leading or trailing whitespace from each block. The filtered blocks are returned as a list.

    Example:
        >>> markdown_text = "This is a markdown text.\n\nIt has two blocks.\n\n\n\nThis is the second block."
        >>> markdown_to_blocks2(markdown_text)
        ['This is a markdown text.', 'It has two blocks.', 'This is the second block.']
    """
    if not markdown:
        raise ValueError("Input string cannot be empty")
    try:
        blocks = markdown.split("\n\n")
        filtered_blocks = []
        for block in blocks:
            if block.strip():
                filtered_blocks.append(block.strip())
        return filtered_blocks
    except AttributeError:
        raise ValueError("Input string cannot be None")

def markdown_to_blocks2(markdown):
    """
    Splits a markdown text into blocks.

    Args:
        markdown (str): The markdown text to split into blocks.

    Returns:
        List[str]: A list of blocks, where each block is a string.

    This function takes a markdown text as input and splits it into blocks. Each block is a string. The function first splits the markdown text into blocks using the double newline character as the delimiter. It then filters out any empty blocks and strips any leading or trailing whitespace from each block. The filtered blocks are returned as a list.

    Example:
        >>> markdown_text = "This is a markdown text.\n\nIt has two blocks.\n\n\n\nThis is the second block."
        >>> markdown_to_blocks2(markdown_text)
        ['This is a markdown text.', 'It has two blocks.', 'This is the second block.']
    """
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    """
    Determines the type of a block of text based on its format.

    Args:
        block (str): The block of text to analyze.

    Returns:
        str: The type of the block. Possible values are:
            - "heading" if the block is a heading.
            - "code" if the block is a code block.
            - "quote" if the block is a quote block.
            - "unordered_list" if the block is an unordered list.
            - "ordered_list" if the block is an ordered list.
            - "paragraph" if the block is a regular paragraph.
            - "image" if the block is an image

    This function takes a block of text and checks its format to determine its type. It uses regular expressions to match the block against different patterns for headings, code blocks, quote blocks, unordered lists, and ordered lists. If none of these patterns match, it assumes the block is a regular paragraph.

    Example:
        >>> block = "# Heading"
        >>> block_to_block_type(block)
        'heading'
    """
    # Check for headings
    heading_match = re.match(r'^#{1,6}\s+\S', block)
    if heading_match:
        return block_type_heading

    # Check for code blocks
    code_match = re.match(r'^```.*?```$', block, re.DOTALL)
    if code_match:
        return block_type_code

    # Check for quote blocks
    quote_match = re.match(r'^>\s+.*', block, re.MULTILINE)
    if quote_match:
        return block_type_quote

    # Check for unordered list blocks
    unordered_list_match = re.match(r'^[\*\-]\s+.*', block, re.MULTILINE)
    if unordered_list_match:
        return block_type_ulist
    
    image_match = re.match(r'!\[.*?\]\((.*?)\)', block, re.MULTILINE)
    if image_match:
        return block_type_image

    # Check for ordered list blocks
    ordered_list_match = re.match(r'^1\.\s+.*', block, re.MULTILINE)
    if ordered_list_match:
        lines = block.split('\n')
        for i, line in enumerate(lines):
            if not re.match(rf'^{i+1}\.\s+.*', line):
                break
        else:
            return block_type_olist

    # If none of the above conditions are met, it's a paragraph
    return block_type_paragraph

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    elif block_type == block_type_heading:
        return heading_to_html_node(block)
    elif block_type == block_type_code:
        return code_to_html_node(block)
    elif block_type == block_type_quote:
        return quote_to_html_node(block)
    elif block_type == block_type_ulist:
        return ulist_to_html_node(block)
    elif block_type == block_type_olist:
        return olist_to_html_node(block)
    elif block_type == "image":
        return image_to_html_node(block)
    else:
        raise ValueError(f"Invalid block type: {block_type}")


def image_to_html_node(block):
    """
    Convert an image block to an HTML img node.

    Args:
        block (str): The image block to convert.

    Returns:
        ParentNode: The HTML img node representing the image block.

    Raises:
        ValueError: If the image block is invalid or does not match the pattern.
    """
    pattern = r'!\[.*?\]\((.*?)\)'
    match = re.match(pattern, block)
    if not match:
        raise ValueError("Invalid image block")

    src = match.group(1)
    if not src:
        raise ValueError("Invalid image block: no src attribute")

    return ParentNode("img", [], {"src": src})



    

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    """
    Convert a quote block to an HTML blockquote node.

    Args:
        block (str): The quote block to convert.

    Returns:
        ParentNode: The HTML blockquote node representing the quote block.

    Raises:
        ValueError: If the quote block is invalid.

    """
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
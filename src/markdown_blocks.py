import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


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
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block.strip():
            filtered_blocks.append(block.strip())
    return filtered_blocks

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
        return block_type_unordered_list

    # Check for ordered list blocks
    ordered_list_match = re.match(r'^1\.\s+.*', block, re.MULTILINE)
    if ordered_list_match:
        lines = block.split('\n')
        for i, line in enumerate(lines):
            if not re.match(rf'^{i+1}\.\s+.*', line):
                break
        else:
            return block_type_ordered_list

    # If none of the above conditions are met, it's a paragraph
    return block_type_paragraph
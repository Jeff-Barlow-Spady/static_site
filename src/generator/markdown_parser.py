# src/generator/markdown_converter.py
import re
import yaml
from markdown_blocks import markdown_to_html_node

def parse_markdown(markdown_content):
    front_matter = {}
    content = markdown_content

    front_matter_match = re.match(r'^---\n(.*?)\n---\n(.*)', markdown_content, re.DOTALL)
    if front_matter_match:
        front_matter = yaml.safe_load(front_matter_match.group(1))
        content = front_matter_match.group(2)

    html_content = markdown_to_html_node(content).to_html()

    return front_matter, html_content

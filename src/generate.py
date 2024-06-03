import os
import re
from markdown_blocks import markdown_to_html_node
from pathlib import Path
# Define directories for static and public files
dir_static = "./static"
dir_public = "./public"

# Define paths for content, template, and destination
FROM_PATH = "./content/index.md"
TEMPLATE_PATH = 'template.html'
DEST_PATH = "public/index.html"
CONTENT_DIR = "./content"
# Function to extract the title from markdown content
def extract_title(markdown):
    """
    Extracts the title from a markdown string.

    Args:
        markdown (str): The markdown string to extract the title from.

    Returns:
        str: The extracted title.

    Raises:
        ValueError: If the markdown content does not contain a title.

    This function uses a regular expression to match the markdown title in the given string. It searches for a line starting with '# ' followed by one or more non-space characters. If a match is found, it removes the '# ' prefix and returns the title. If no match is found, it raises a ValueError.

    Example:
        >>> extract_title("# My Title")
        'My Title'
    """
    header_pattern = r"^#\s+(.+)$"  # Regular expression to match the markdown title
    match = re.search(header_pattern, markdown, re.MULTILINE)
    if match:
        title = match.group().lstrip('# ')
        print(f"Extracted title: {title}")
        return title
    else:
        raise ValueError("Markdown content does not contain a title.")

# Function to generate the HTML page from markdown and template
# Recursive function to generate HTML pages from markdown files and traverse directories
def generate_and_traverse(src_dir, dest_dir, template_path):
    """
    Recursively generates HTML pages from markdown files and copies them to the destination directory.

    Args:
        src_dir (str): The directory containing the markdown files.
        dest_dir (str): The destination directory where the generated HTML files will be copied.
        template_path (str): The path to the template file used to generate the HTML pages.

    Returns:
        None

    This function traverses the source directory and its subdirectories using `os.walk()`. For each markdown file found, it generates an HTML page by reading the markdown content, reading the template file, converting the markdown to HTML, extracting the title from the markdown content, replacing placeholders in the template with the title and HTML content, and writing the output HTML to the destination directory.

    If any error occurs during the process, it is printed to the console and the function continues to the next file.

    Example:
        >>> generate_and_traverse("./content", "./public", "template.html")
        ================================================================================
        Generating page from ./content/index.md to ./public/index.html using template.html
        ================================================================================
        ================================================================================
        PAGE GENERATED SUCCESSFULLY
        ================================================================================
    """
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".md"):
                markdown_path = os.path.join(root, file)
                relative_path = os.path.relpath(markdown_path, src_dir)
                dest_path = os.path.join(dest_dir, os.path.splitext(relative_path)[0] + ".html")

                print("=" * 94)
                print(f"Generating page from {markdown_path} to {dest_path} using {template_path}")
                print("=" * 94)

                # Read the markdown file content
                try:
                    with open(markdown_path, encoding="utf-8") as source_file:
                        markdown_content = source_file.read()
                except Exception as e:
                    print(f"Error: Unable to read file '{markdown_path}'. {e}")
                    continue

                # Read the template file content
                try:
                    with open(template_path, encoding="utf-8") as template_file:
                        template = template_file.read()
                except Exception as e:
                    print(f"Error: Unable to read file '{template_path}'. {e}")
                    continue

                # Convert markdown to HTML
                try:
                    html_content = markdown_to_html_node(markdown_content).to_html()
                except Exception as e:
                    print(f"Error: Unable to convert markdown in file '{markdown_path}' to HTML. {e}")
                    continue

                # Extract the title from the markdown content
                try:
                    title = extract_title(markdown_content)
                except ValueError as e:
                    print(f"Error: {e}")
                    continue

                # Replace placeholders in the template with title and HTML content
                try:
                    template = template.replace("{{ Title }}", title)
                    template = template.replace("{{ Content }}", html_content)
                except Exception as e:
                    print(f"Error: Unable to replace placeholders in template '{template_path}'. {e}")
                    continue

                # Write the output HTML to the destination path
                try:
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    with open(dest_path, "w", encoding="utf-8") as dest_file:
                        dest_file.write(template)
                except Exception as e:
                    print(f"Error: Unable to write file '{dest_path}'. {e}")
                    continue

                print("=" * 94)
                print("PAGE GENERATED SUCCESSFULLY")
                print("=" * 94)

# Function to generate the HTML page from markdown and template
def generate_page(FROM_PATH, TEMPLATE_PATH, DEST_PATH):
    """
    Generates an HTML page from a markdown file and a template file, and writes it to a destination path.

    Args:
        FROM_PATH (str): The path to the markdown file.
        TEMPLATE_PATH (str): The path to the template file.
        DEST_PATH (str): The path to the destination file.

    Returns:
        None

    This function reads the content of the markdown file, reads the content of the template file, converts the markdown to HTML, extracts the title from the markdown content, replaces placeholders in the template with the title and HTML content, and writes the output HTML to the destination file. If any error occurs during the process, an error message is printed to the console.

    Example:
        >>> generate_page("./content/index.md", "template.html", "public/index.html")
        ================================================================================
        Generating page from ./content/index.md to public/index.html using template.html
        ================================================================================
        ================================================================================
        PAGE GENERATED SUCCESSFULLY
        ================================================================================
    """
    print("=" * 94)
    print(f"Generating page from {FROM_PATH} to {DEST_PATH} using {TEMPLATE_PATH}")
    print("=" * 94)

    # Read the markdown file content
    try:
        with open(FROM_PATH, encoding="utf-8") as source_file:
            markdown_content = source_file.read()
    except Exception as e:
        print(f"Error: Unable to read file '{FROM_PATH}'. {e}")
        return

    # Read the template file content
    try:
        with open(TEMPLATE_PATH, encoding="utf-8") as template_file:
            template = template_file.read()
    except Exception as e:
        print(f"Error: Unable to read file '{TEMPLATE_PATH}'. {e}")
        return

    # Convert markdown to HTML
    try:
        html_content = markdown_to_html_node(markdown_content).to_html()
    except Exception as e:
        print(f"Error: Unable to convert markdown in file '{FROM_PATH}' to HTML. {e}")
        return

    # Extract the title from the markdown content
    try:
        title = extract_title(markdown_content)
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Replace placeholders in the template with title and HTML content
    try:
        template = template.replace("{{ Title }}", title)
        template = template.replace("{{ Content }}", html_content)
    except Exception as e:
        print(f"Error: Unable to replace placeholders in template '{TEMPLATE_PATH}'. {e}")
        return

    # Write the output HTML to the destination path
    try:
        os.makedirs(os.path.dirname(DEST_PATH), exist_ok=True)
        with open(DEST_PATH, "w", encoding="utf-8") as dest_file:
            dest_file.write(template)
    except Exception as e:
        print(f"Error: Unable to write file '{DEST_PATH}'. {e}")
        return

    print("=" * 94)
    print("PAGE GENERATED SUCCESSFULLY")
    print("=" * 94)


def traverse_and_generate(src_dir, dest_dir, template_path):
    """
    Traverses the given source directory and generates HTML pages from markdown files.

    Args:
        src_dir (str): The directory containing the markdown files.
        dest_dir (str): The destination directory where the generated HTML files will be copied.
        template_path (str): The path to the template file used to generate the HTML pages.

    Returns:
        None

    This function recursively traverses the source directory and its subdirectories using `os.walk()`. For each markdown file found, it generates an HTML page by calling the `generate_page()` function with the markdown file path, template path, and destination path.

    The markdown file path is obtained by joining the root directory of the current iteration with the file name. The relative path of the markdown file is obtained by removing the source directory path from the markdown file path. The destination path is obtained by joining the destination directory with the base name of the relative path (without the file extension) and appending the ".html" extension.

    The `generate_page()` function is called with the markdown file path, template path, and destination path to generate the HTML page.

    If any error occurs during the process, it is printed to the console and the function continues to the next file.

    Example:
        >>> traverse_and_generate("./content", "./public", "template.html")
        # Generates HTML pages from markdown files in the "./content" directory and copies them to the "./public" directory using the "template.html" template.
    """
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".md"):
                markdown_path = os.path.join(root, file)
                relative_path = os.path.relpath(markdown_path, src_dir)
                dest_path = os.path.join(dest_dir, os.path.splitext(relative_path)[0] + ".html")
                generate_page(markdown_path, template_path, dest_path)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Generate HTML pages recursively from markdown files in the given directory and copy them to the destination directory using the specified template.

    Args:
        dir_path_content (str): The path to the directory containing the markdown files.
        template_path (str): The path to the template file.
        dest_dir_path (str): The path to the destination directory where the generated HTML pages will be copied.

    Returns:
        None

    Raises:
        None

    This function iterates over the files in the given directory and its subdirectories. For each file, it checks if it is a markdown file. If it is, it generates an HTML page from the markdown file using the specified template and copies it to the destination directory. If the file is not a markdown file, it recursively calls itself with the file path as the directory path and the same template and destination paths.

    Example:
        >>> generate_pages_recursive("./content", "template.html", "./public")
        # Generates HTML pages from markdown files in the "./content" directory and copies them to the "./public" directory using the "template.html" template.
    """
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)
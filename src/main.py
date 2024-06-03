import os
import shutil
from pathlib import Path
import re
from copy_static import copy_files_recursive
from markdown_blocks import markdown_to_html_node
#from generate import generate_page, traverse_and_generate, extract_title
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
    header_pattern = r"^#\s+(.+)$"  # Regular expression to match the markdown title
    match = re.search(header_pattern, markdown, re.MULTILINE)
    if match:
        title = match.group().lstrip('# ')
        print(f"Extracted title: {title}")
        return title
    else:
        raise ValueError("Markdown content does not contain a title.")

# Function to generate the HTML page from markdown and template
def generate_page(FROM_PATH, TEMPLATE_PATH, DEST_PATH):
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
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".md"):
                markdown_path = os.path.join(root, file)
                relative_path = os.path.relpath(markdown_path, src_dir)
                dest_path = os.path.join(dest_dir, os.path.splitext(relative_path)[0] + ".html")
                generate_page(markdown_path, template_path, dest_path)
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)

# Main function to delete and recreate public directory, copy static files, and generate the page
def main():
    print("Deleting Public Directory")
    if os.path.exists(dir_public):
        shutil.rmtree(dir_public)
    os.makedirs(dir_public, exist_ok=True)

    print("Copying Static Files")
    copy_files_recursive(dir_static, dir_public)

    generate_pages_recursive(CONTENT_DIR, TEMPLATE_PATH, dir_public)
    #generate_page(FROM_PATH, TEMPLATE_PATH, DEST_PATH)
    #traverse_and_generate(CONTENT_DIR, dir_public, TEMPLATE_PATH)
if __name__ == "__main__":
    main()


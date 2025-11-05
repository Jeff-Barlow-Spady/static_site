import os
import shutil
from copy_static import copy_files_recursive
from generate import generate_pages_recursive#, generate_and_traverse, generate_page
from sys import argv
# Define directories for static and public files
basepath = os.path.dirname(argv[0])
dir_static = os.path.join(basepath, "static")
dir_public = os.path.join(basepath, "public")
# Define paths for content, template, and destination
FROM_PATH = os.path.join(basepath, "content", "index.md")
TEMPLATE_PATH = os.path.join(basepath, "template.html")
CONTENT_DIR = os.path.join(basepath, "content")
# Function to extract the title from markdown content


# Main function to delete and recreate public directory, copy static files, and generate the page
def main():
    """
    Deletes the public directory, recreates it, and copies static files to it.
    Then generates HTML pages from markdown files using the specified template.

    This function does not take any parameters.

    This function does not return anything.
    """
    print("Deleting Public Directory")
    if os.path.exists(dir_public):
        shutil.rmtree(dir_public)
    os.makedirs(dir_public, exist_ok=True)

    print("Copying Static Files")
    copy_files_recursive(dir_static, dir_public)

    generate_pages_recursive(basepath, TEMPLATE_PATH, dir_public)

if __name__ == "__main__":
    main()

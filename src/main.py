import os
import shutil
import sys
from copy_static import copy_files_recursive
from generate import generate_pages_recursive

# Define directories for static and docs files
dir_static = "./static"
dir_docs = "./docs"
# Define paths for content, template, and destination
CONTENT_DIR = "./content"
TEMPLATE_PATH = 'template.html'

# Main function to delete and recreate docs directory, copy static files, and generate the page
def main():
    """
    Deletes the docs directory, recreates it, and copies static files to it.
    Then generates HTML pages from markdown files using the specified template.

    Gets basepath from CLI argument (defaults to /).
    """
    # Get basepath from CLI argument, default to /
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    print("Deleting Docs Directory")
    if os.path.exists(dir_docs):
        shutil.rmtree(dir_docs)
    os.makedirs(dir_docs, exist_ok=True)

    print("Copying Static Files")
    copy_files_recursive(dir_static, dir_docs)

    generate_pages_recursive(CONTENT_DIR, TEMPLATE_PATH, dir_docs, basepath)

if __name__ == "__main__":
    main()

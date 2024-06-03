import os
import shutil
from copy_static import copy_files_recursive
from generate import generate_pages_recursive#, generate_and_traverse, generate_page
# Define directories for static and public files
dir_static = "./static"
dir_public = "./public"

# Define paths for content, template, and destination
FROM_PATH = "./content/index.md"
TEMPLATE_PATH = 'template.html'
DEST_PATH = "public/index.html"
CONTENT_DIR = "./content"
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

    generate_pages_recursive(CONTENT_DIR, TEMPLATE_PATH, dir_public)
    #generate_page(FROM_PATH, TEMPLATE_PATH, DEST_PATH)
    #traverse_and_generate(CONTENT_DIR, dir_public, TEMPLATE_PATH)
if __name__ == "__main__":
    main()


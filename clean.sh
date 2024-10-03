# Move static files
mv static src/

# Move generator-related scripts
mv src/copy_static.py src/generator/
mv src/generate.py src/generator/page_generator.py
mv src/htmlnode.py src/generator/
mv src/inline_markdown.py src/generator/
mv src/markdown_blocks.py src/generator/
mv src/textnode.py src/generator/
mv src/test_htmlnode.py tests/
mv src/test_inline_markdown.py tests/
mv src/test_markdown_blocks.py tests/
mv src/test_textnode.py tests/

# Move server-related script
mv server.py src/server/

# Move templates
mkdir src/templates
mv template.html src/templates/base.html

# Move utility scripts or create them if they don't exist
touch src/utils/__init__.py
touch src/generator/__init__.py
touch src/server/__init__.py

# Remove any empty directories if necessary

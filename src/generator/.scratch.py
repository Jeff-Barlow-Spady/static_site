# src/generator/page_generator.py
# src/generator/page_generator.py
from src.config import Config
from src.generator.copy_static import copy_static_files
from src.generator.markdown_converter import parse_markdown
from src.utils.logger import logger
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

def generate_all(config: Config):
    logger.info("Starting site generation...")
    copy_static_files(config.static_dir, config.output_dir / 'static')
    generate_site(config)
    logger.info("Site generation completed.")



def generate_site(config: Config):
    env = Environment(loader=FileSystemLoader(config.templates_dir))

    for markdown_file in config.source_dir.rglob("*.md"):
        relative_path = markdown_file.relative_to(config.source_dir)
        output_file = config.output_dir / relative_path.with_suffix('.html')
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with markdown_file.open('r', encoding='utf-8') as f:
            markdown_content = f.read()

        front_matter, html_content = parse_markdown(markdown_content)
        title = front_matter.get('title', 'Untitled Page')
        template_name = front_matter.get('template', config.template)

        try:
            template = env.get_template(template_name)
        except Exception as e:
            logger.error(f"Template {template_name} not found. Using default template. Error: {e}")
            template = env.get_template(config.template)

        rendered_html = template.render(title=title, content=html_content, **front_matter)

        with output_file.open('w', encoding='utf-8') as f:
            f.write(rendered_html)

        logger.info(f"Generated {output_file}")

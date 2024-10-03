# src/config.py
import yaml
from pathlib import Path

class Config:
    def __init__(self, config_file='config.yaml'):
        self.config_file = Path(config_file)
        self.load_config()

    def load_config(self):
        if not self.config_file.exists():
            raise FileNotFoundError(f"Configuration file {self.config_file} not found.")
        with open(self.config_file, 'r') as f:
            cfg = yaml.safe_load(f)
        self.source_dir = Path(cfg.get('source_dir', './content'))
        self.output_dir = Path(cfg.get('output_dir', './public'))
        self.templates_dir = Path(cfg.get('templates_dir', './src/templates'))
        self.static_dir = Path(cfg.get('static_dir', './src/static'))
        self.template = cfg.get('template', 'base.html')
        self.port = cfg.get('port', 8888)

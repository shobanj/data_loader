import os
import yaml
from importlib import import_module
from registry import registry

def load_config(path="config.yaml"):
    with open(path) as f:
        raw = f.read()
    # Replace env vars like ${OPENAI_API_KEY}
    for key, val in os.environ.items():
        raw = raw.replace(f"${{{key}}}", val)
    return yaml.safe_load(raw)

def get_component(config_section):
    type_ = config_section["type"]
    cls_path = registry[type_]
    module, cls_name = cls_path.rsplit(".", 1)
    cls = getattr(import_module(module), cls_name)
    kwargs = {k: v for k, v in config_section.items() if k != "type"}
    return cls(**kwargs)
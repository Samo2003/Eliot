from jinja2 import Environment
from jinja2.exceptions import TemplateError
from typing import Dict, Any
import os

def generate_to_file(env: Environment, template_name: str, output_path: str, context: Dict[str, Any] = {}) -> None:
    try:
        template = env.get_template(template_name)
        rendered = template.render(context)
    except TemplateError as e:
        raise RuntimeError(f"ERROR: {type(e).__name__} in {template_name}: {e}") from e
    except Exception as e:
        raise RuntimeError(f"ERROR: unecxepcted error in {template_name}") from e
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(rendered)

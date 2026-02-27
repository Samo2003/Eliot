from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, ClassVar
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateError
from src.generator.config import GeneratorContext, TEMPLATE_DIR

class GeneratorBase(ABC):
    registry: ClassVar[List[GeneratorBase]] = []
    env: ClassVar[Environment] = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),      # Initialize template loader
        trim_blocks=True,                           # Strip new lines after generated line
        lstrip_blocks=True                          # Strip white spaces from the beginning of the line
    )

    def __init_subclass__(cls):
        GeneratorBase.registry.append(cls())

    @abstractmethod
    def generate(self, context: GeneratorContext) -> None:
        pass

    def _generate_to_file(
        self, 
        template_name: str, 
        output_path: Path,
        context_data: Dict[str, Any] | None = None
    ) -> None:
        """Generates template to output path with given context"""
        if context_data is None:
            context_data = {}

        try:
            template = self.env.get_template(template_name)
            rendered = template.render(context_data)
        except TemplateError as e:
            raise RuntimeError(f"ERROR: {type(e).__name__} in {template_name}: {e}") from e
        except Exception as e:
            raise RuntimeError(f"ERROR: unexpected error in {template_name}") from e
        
        # Create output directories
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(rendered)
